from __future__ import annotations

import re
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Iterator
from zoneinfo import ZoneInfo


DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "bontempo_demo.sqlite3"
CLINIC_TIMEZONE = ZoneInfo("America/Sao_Paulo")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

CONSULTATION_STATUSES = (
    ("agendada", "Agendada", 1),
    ("confirmada", "Confirmada", 1),
    ("realizada", "Realizada", 0),
    ("cancelada", "Cancelada", 0),
    ("nao_compareceu", "Não compareceu", 0),
)
ACTIVE_STATUS_CODES = ("agendada", "confirmada")

SCHEMA = """
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL CHECK (length(trim(nome)) > 0),
    telefone TEXT NOT NULL CHECK (length(trim(telefone)) > 0),
    email TEXT
);

CREATE TABLE IF NOT EXISTS profissionais (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL CHECK (length(trim(nome)) > 0),
    telefone TEXT NOT NULL CHECK (length(trim(telefone)) > 0),
    email TEXT
);

CREATE TABLE IF NOT EXISTS especialidades (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL CHECK (length(trim(nome)) > 0),
    nome_normalizado TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS profissional_especialidade (
    profissional_id INTEGER NOT NULL REFERENCES profissionais(id) ON DELETE RESTRICT,
    especialidade_id INTEGER NOT NULL REFERENCES especialidades(id) ON DELETE RESTRICT,
    PRIMARY KEY (profissional_id, especialidade_id)
);

CREATE TABLE IF NOT EXISTS status_consulta (
    id INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL UNIQUE,
    ocupa_horario INTEGER NOT NULL CHECK (ocupa_horario IN (0, 1))
);

CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id) ON DELETE RESTRICT,
    profissional_id INTEGER NOT NULL REFERENCES profissionais(id) ON DELETE RESTRICT,
    especialidade_id INTEGER NOT NULL REFERENCES especialidades(id) ON DELETE RESTRICT,
    status_consulta_id INTEGER NOT NULL REFERENCES status_consulta(id) ON DELETE RESTRICT,
    inicio_em TEXT NOT NULL,
    fim_em TEXT NOT NULL,
    CHECK (fim_em > inicio_em)
);

CREATE INDEX IF NOT EXISTS idx_consultas_profissional_inicio
    ON consultas (profissional_id, inicio_em);
"""


class DatabaseError(Exception):
    """Erro de persistência ou regra de negócio do banco local."""


class ValidationError(DatabaseError):
    """Entrada inválida para uma operação do sistema."""


class DuplicateSpecialtyError(DatabaseError):
    """Já existe uma especialidade com esse nome normalizado."""


class ScheduleConflictError(DatabaseError):
    """O médico já possui consulta ativa sobreposta nesse intervalo."""


class DemoDataRequiresEmptyDatabaseError(DatabaseError):
    """Dados de demonstração só podem ser criados em um banco funcional vazio."""


@contextmanager
def _connect(db_path: str | Path | None = None) -> Iterator[sqlite3.Connection]:
    path = Path(db_path) if db_path is not None else DATABASE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def _transaction(connection: sqlite3.Connection) -> Iterator[None]:
    connection.execute("BEGIN IMMEDIATE")
    try:
        yield
        connection.execute("COMMIT")
    except Exception:
        connection.execute("ROLLBACK")
        raise


def initialize_database(db_path: str | Path | None = None) -> None:
    with _connect(db_path) as connection:
        connection.executescript(SCHEMA)
        connection.executemany(
            """
            INSERT INTO status_consulta (codigo, nome, ocupa_horario)
            VALUES (?, ?, ?)
            ON CONFLICT (codigo) DO NOTHING
            """,
            CONSULTATION_STATUSES,
        )


def list_patients(db_path: str | Path | None = None) -> list[dict[str, object]]:
    with _connect(db_path) as connection:
        rows = connection.execute(
            "SELECT id, nome, telefone, email FROM pacientes ORDER BY nome, id"
        ).fetchall()
    return [dict(row) for row in rows]


def create_patient(
    nome: str,
    telefone: str,
    email: str | None,
    db_path: str | Path | None = None,
) -> int:
    name, phone, clean_email = _validate_contact(nome, telefone, email)
    with _connect(db_path) as connection, _transaction(connection):
        cursor = connection.execute(
            "INSERT INTO pacientes (nome, telefone, email) VALUES (?, ?, ?)",
            (name, phone, clean_email),
        )
        return int(cursor.lastrowid)


def list_professionals(db_path: str | Path | None = None) -> list[dict[str, object]]:
    with _connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT p.id, p.nome, p.telefone, p.email,
                   group_concat(e.nome, ', ') AS especialidades
            FROM profissionais AS p
            LEFT JOIN profissional_especialidade AS pe ON pe.profissional_id = p.id
            LEFT JOIN especialidades AS e ON e.id = pe.especialidade_id
            GROUP BY p.id
            ORDER BY p.nome, p.id
            """
        ).fetchall()
    return [dict(row) for row in rows]


def create_professional(
    nome: str,
    telefone: str,
    email: str | None,
    specialty_ids: list[int] | tuple[int, ...] = (),
    db_path: str | Path | None = None,
) -> int:
    name, phone, clean_email = _validate_contact(nome, telefone, email)
    with _connect(db_path) as connection, _transaction(connection):
        _ensure_specialties_exist(connection, specialty_ids)
        cursor = connection.execute(
            "INSERT INTO profissionais (nome, telefone, email) VALUES (?, ?, ?)",
            (name, phone, clean_email),
        )
        professional_id = int(cursor.lastrowid)
        connection.executemany(
            """
            INSERT INTO profissional_especialidade (profissional_id, especialidade_id)
            VALUES (?, ?)
            """,
            [(professional_id, specialty_id) for specialty_id in set(specialty_ids)],
        )
        return professional_id


def set_professional_specialties(
    professional_id: int,
    specialty_ids: list[int] | tuple[int, ...],
    db_path: str | Path | None = None,
) -> None:
    with _connect(db_path) as connection, _transaction(connection):
        exists = connection.execute(
            "SELECT 1 FROM profissionais WHERE id = ?", (professional_id,)
        ).fetchone()
        if exists is None:
            raise ValidationError("Profissional não encontrado.")
        _ensure_specialties_exist(connection, specialty_ids)
        connection.execute(
            "DELETE FROM profissional_especialidade WHERE profissional_id = ?",
            (professional_id,),
        )
        connection.executemany(
            """
            INSERT INTO profissional_especialidade (profissional_id, especialidade_id)
            VALUES (?, ?)
            """,
            [(professional_id, specialty_id) for specialty_id in set(specialty_ids)],
        )


def list_specialties(db_path: str | Path | None = None) -> list[dict[str, object]]:
    with _connect(db_path) as connection:
        rows = connection.execute(
            "SELECT id, nome FROM especialidades ORDER BY nome, id"
        ).fetchall()
    return [dict(row) for row in rows]


def create_specialty(nome: str, db_path: str | Path | None = None) -> int:
    clean_name = nome.strip() if isinstance(nome, str) else ""
    if not clean_name:
        raise ValidationError("Informe o nome da especialidade.")
    normalized_name = clean_name.casefold()
    try:
        with _connect(db_path) as connection, _transaction(connection):
            cursor = connection.execute(
                """
                INSERT INTO especialidades (nome, nome_normalizado)
                VALUES (?, ?)
                """,
                (clean_name, normalized_name),
            )
            return int(cursor.lastrowid)
    except sqlite3.IntegrityError as error:
        if "especialidades.nome_normalizado" in str(error):
            raise DuplicateSpecialtyError(
                "Já existe uma especialidade com esse nome."
            ) from error
        raise DatabaseError("Não foi possível salvar a especialidade.") from error


def list_professional_specialties(
    professional_id: int,
    db_path: str | Path | None = None,
) -> list[int]:
    with _connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT especialidade_id
            FROM profissional_especialidade
            WHERE profissional_id = ?
            ORDER BY especialidade_id
            """,
            (professional_id,),
        ).fetchall()
    return [int(row["especialidade_id"]) for row in rows]


def list_appointments(db_path: str | Path | None = None) -> list[dict[str, object]]:
    with _connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT c.id, c.inicio_em, c.fim_em, c.paciente_id, c.profissional_id,
                   c.especialidade_id, c.status_consulta_id,
                   p.nome AS paciente_nome, pr.nome AS profissional_nome,
                   e.nome AS especialidade_nome, s.codigo AS status_codigo,
                   s.nome AS status_nome
            FROM consultas AS c
            JOIN pacientes AS p ON p.id = c.paciente_id
            JOIN profissionais AS pr ON pr.id = c.profissional_id
            JOIN especialidades AS e ON e.id = c.especialidade_id
            JOIN status_consulta AS s ON s.id = c.status_consulta_id
            ORDER BY c.inicio_em, c.id
            """
        ).fetchall()
    return [dict(row) for row in rows]


def create_appointment(
    patient_id: int,
    professional_id: int,
    specialty_id: int,
    appointment_date: date,
    start_time: time,
    end_time: time,
    db_path: str | Path | None = None,
) -> int:
    if end_time <= start_time:
        raise ValidationError("O horário final deve ser posterior ao inicial.")
    start_local = datetime.combine(appointment_date, start_time, CLINIC_TIMEZONE)
    end_local = datetime.combine(appointment_date, end_time, CLINIC_TIMEZONE)
    start_utc = start_local.astimezone(timezone.utc).isoformat(timespec="seconds")
    end_utc = end_local.astimezone(timezone.utc).isoformat(timespec="seconds")

    with _connect(db_path) as connection, _transaction(connection):
        status = connection.execute(
            "SELECT id FROM status_consulta WHERE codigo = ?",
            ("agendada",),
        ).fetchone()
        if status is None:
            raise DatabaseError("O catálogo de status da consulta não foi inicializado.")

        linked_specialty = connection.execute(
            """
            SELECT 1
            FROM profissional_especialidade
            WHERE profissional_id = ? AND especialidade_id = ?
            """,
            (professional_id, specialty_id),
        ).fetchone()
        if linked_specialty is None:
            raise ValidationError(
                "A especialidade selecionada não está vinculada ao profissional."
            )

        _ensure_no_schedule_conflict(
            connection, professional_id, start_utc, end_utc
        )
        cursor = connection.execute(
            """
            INSERT INTO consultas (
                paciente_id, profissional_id, especialidade_id,
                status_consulta_id, inicio_em, fim_em
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                professional_id,
                specialty_id,
                int(status["id"]),
                start_utc,
                end_utc,
            ),
        )
        return int(cursor.lastrowid)


def update_appointment_status(
    appointment_id: int,
    status_code: str,
    db_path: str | Path | None = None,
) -> None:
    with _connect(db_path) as connection, _transaction(connection):
        status = connection.execute(
            "SELECT id, ocupa_horario FROM status_consulta WHERE codigo = ?",
            (status_code,),
        ).fetchone()
        if status is None:
            raise ValidationError("O status selecionado não é válido.")
        appointment = connection.execute(
            """
            SELECT profissional_id, inicio_em, fim_em
            FROM consultas
            WHERE id = ?
            """,
            (appointment_id,),
        ).fetchone()
        if appointment is None:
            raise ValidationError("Consulta não encontrada.")
        if status["ocupa_horario"]:
            _ensure_no_schedule_conflict(
                connection,
                int(appointment["profissional_id"]),
                str(appointment["inicio_em"]),
                str(appointment["fim_em"]),
                exclude_appointment_id=appointment_id,
            )
        connection.execute(
            "UPDATE consultas SET status_consulta_id = ? WHERE id = ?",
            (int(status["id"]), appointment_id),
        )


def seed_demo_data(db_path: str | Path | None = None) -> int:
    patients = (
        ("Ana Demonstração", "(11) 90000-0001", "ana@example.invalid"),
        ("Bruno Exemplo", "(11) 90000-0002", "bruno@example.invalid"),
    )
    professionals = (
        ("Dra. Marina Fictícia", "(11) 90000-0011", "marina@example.invalid"),
        ("Dr. Caio Demonstração", "(11) 90000-0012", "caio@example.invalid"),
    )
    specialties = ("Cardiologia", "Dermatologia", "Pediatria")
    appointments = (
        (0, 0, 0, time(9, 0), time(9, 30), "agendada"),
        (1, 0, 0, time(9, 30), time(10, 0), "confirmada"),
        (0, 1, 2, time(10, 0), time(10, 30), "agendada"),
    )

    with _connect(db_path) as connection, _transaction(connection):
        counts = connection.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM pacientes) +
                (SELECT COUNT(*) FROM profissionais) +
                (SELECT COUNT(*) FROM especialidades) +
                (SELECT COUNT(*) FROM profissional_especialidade) +
                (SELECT COUNT(*) FROM consultas) AS total
            """
        ).fetchone()
        if int(counts["total"]) != 0:
            raise DemoDataRequiresEmptyDatabaseError(
                "O banco já contém dados. Os exemplos não foram inseridos nem "
                "alteraram os registros existentes."
            )

        patient_ids = [
            int(
                connection.execute(
                    "INSERT INTO pacientes (nome, telefone, email) VALUES (?, ?, ?)",
                    patient,
                ).lastrowid
            )
            for patient in patients
        ]
        professional_ids = [
            int(
                connection.execute(
                    """
                    INSERT INTO profissionais (nome, telefone, email)
                    VALUES (?, ?, ?)
                    """,
                    professional,
                ).lastrowid
            )
            for professional in professionals
        ]
        specialty_ids = [
            int(
                connection.execute(
                    """
                    INSERT INTO especialidades (nome, nome_normalizado)
                    VALUES (?, ?)
                    """,
                    (name, name.casefold()),
                ).lastrowid
            )
            for name in specialties
        ]

        connection.executemany(
            """
            INSERT INTO profissional_especialidade (profissional_id, especialidade_id)
            VALUES (?, ?)
            """,
            (
                (professional_ids[0], specialty_ids[0]),
                (professional_ids[0], specialty_ids[1]),
                (professional_ids[1], specialty_ids[2]),
            ),
        )

        today = datetime.now(CLINIC_TIMEZONE).date()
        status_ids = {
            row["codigo"]: int(row["id"])
            for row in connection.execute(
                "SELECT id, codigo FROM status_consulta"
            ).fetchall()
        }
        for patient_index, professional_index, specialty_index, start, end, status_code in appointments:
            start_local = datetime.combine(today, start, CLINIC_TIMEZONE)
            end_local = datetime.combine(today, end, CLINIC_TIMEZONE)
            connection.execute(
                """
                INSERT INTO consultas (
                    paciente_id, profissional_id, especialidade_id,
                    status_consulta_id, inicio_em, fim_em
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    patient_ids[patient_index],
                    professional_ids[professional_index],
                    specialty_ids[specialty_index],
                    status_ids[status_code],
                    start_local.astimezone(timezone.utc).isoformat(timespec="seconds"),
                    end_local.astimezone(timezone.utc).isoformat(timespec="seconds"),
                ),
            )
        return len(patients) + len(professionals) + len(specialties) + len(appointments)


def get_statuses(db_path: str | Path | None = None) -> list[dict[str, object]]:
    with _connect(db_path) as connection:
        rows = connection.execute(
            "SELECT id, codigo, nome FROM status_consulta ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


def format_local_timestamp(value: str) -> str:
    timestamp = datetime.fromisoformat(value).astimezone(CLINIC_TIMEZONE)
    return timestamp.strftime("%d/%m/%Y %H:%M")


def _validate_contact(
    nome: str,
    telefone: str,
    email: str | None,
) -> tuple[str, str, str | None]:
    name = nome.strip() if isinstance(nome, str) else ""
    phone = telefone.strip() if isinstance(telefone, str) else ""
    clean_email = email.strip() if isinstance(email, str) else ""
    if not name:
        raise ValidationError("Informe o nome.")
    if not phone:
        raise ValidationError("Informe o telefone.")
    if clean_email and not EMAIL_PATTERN.fullmatch(clean_email):
        raise ValidationError("Informe um e-mail válido ou deixe o campo vazio.")
    return name, phone, clean_email or None


def _ensure_specialties_exist(
    connection: sqlite3.Connection,
    specialty_ids: list[int] | tuple[int, ...],
) -> None:
    distinct_ids = set(specialty_ids)
    if not distinct_ids:
        return
    placeholders = ", ".join("?" for _ in distinct_ids)
    rows = connection.execute(
        f"SELECT id FROM especialidades WHERE id IN ({placeholders})",
        tuple(distinct_ids),
    ).fetchall()
    if len(rows) != len(distinct_ids):
        raise ValidationError("Uma ou mais especialidades não existem.")


def _ensure_no_schedule_conflict(
    connection: sqlite3.Connection,
    professional_id: int,
    start_utc: str,
    end_utc: str,
    exclude_appointment_id: int | None = None,
) -> None:
    parameters: list[object] = [
        professional_id,
        end_utc,
        start_utc,
        *ACTIVE_STATUS_CODES,
    ]
    exclude_clause = ""
    if exclude_appointment_id is not None:
        exclude_clause = " AND c.id != ?"
        parameters.append(exclude_appointment_id)
    conflict = connection.execute(
        f"""
        SELECT 1
        FROM consultas AS c
        JOIN status_consulta AS s ON s.id = c.status_consulta_id
        WHERE c.profissional_id = ?
          AND c.inicio_em < ?
          AND c.fim_em > ?
          AND s.codigo IN (?, ?)
          {exclude_clause}
        LIMIT 1
        """,
        tuple(parameters),
    ).fetchone()
    if conflict is not None:
        raise ScheduleConflictError(
            "Já existe uma consulta Agendada ou Confirmada sobreposta para esse profissional."
        )
