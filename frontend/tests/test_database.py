import sqlite3
import tempfile
import unittest
from datetime import date, time
from pathlib import Path

from services import database


class TestLocalDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.sqlite3"
        database.initialize_database(self.db_path)
        self.patient_id = database.create_patient(
            "Paciente fictício", "(11) 90000-1000", "paciente@example.invalid", self.db_path
        )
        self.specialty_id = database.create_specialty("Cardiologia", self.db_path)
        self.professional_id = database.create_professional(
            "Médica fictícia",
            "(11) 90000-2000",
            "medica@example.invalid",
            [self.specialty_id],
            self.db_path,
        )
        self.appointment_date = date(2030, 5, 20)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_patient_validation_and_persistence(self) -> None:
        with self.assertRaises(database.ValidationError):
            database.create_patient(" ", "123", "", self.db_path)
        with self.assertRaises(database.ValidationError):
            database.create_patient("Nome", "123", "email-invalido", self.db_path)

        patient_id = database.create_patient("  Outra pessoa  ", " 123 ", "", self.db_path)
        database.initialize_database(self.db_path)

        patients = database.list_patients(self.db_path)
        self.assertEqual(len(patients), 2)
        created = next(patient for patient in patients if patient["id"] == patient_id)
        self.assertEqual(created["nome"], "Outra pessoa")
        self.assertIsNone(created["email"])

    def test_specialty_uniqueness_ignores_outer_spaces_and_case(self) -> None:
        database.create_specialty("  NEUROLOGIA ", self.db_path)

        with self.assertRaises(database.DuplicateSpecialtyError):
            database.create_specialty("Neurologia", self.db_path)

        self.assertEqual(len(database.list_specialties(self.db_path)), 2)

    def test_professionals_have_many_to_many_specialties(self) -> None:
        dermatology_id = database.create_specialty("Dermatologia", self.db_path)
        second_professional_id = database.create_professional(
            "Segundo médico",
            "(11) 90000-2001",
            "",
            [self.specialty_id, dermatology_id],
            self.db_path,
        )
        database.set_professional_specialties(
            self.professional_id,
            [dermatology_id, self.specialty_id],
            self.db_path,
        )

        database.set_professional_specialties(
            second_professional_id,
            [self.specialty_id],
            self.db_path,
        )
        professionals = database.list_professionals(self.db_path)
        self.assertEqual(len(professionals), 2)
        self.assertIn("Cardiologia", str(professionals[0]["especialidades"]))
        self.assertIn("Dermatologia", str(professionals[0]["especialidades"]))

        with database._connect(self.db_path) as connection:
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """
                    INSERT INTO profissional_especialidade
                        (profissional_id, especialidade_id)
                    VALUES (?, ?)
                    """,
                    (self.professional_id, self.specialty_id),
                )

    def test_foreign_keys_reject_missing_related_records(self) -> None:
        with database._connect(self.db_path) as connection:
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """
                    INSERT INTO profissional_especialidade
                        (profissional_id, especialidade_id)
                    VALUES (?, ?)
                    """,
                    (99999, self.specialty_id),
                )

    def test_appointment_requires_linked_specialty_and_valid_interval(self) -> None:
        dermatology_id = database.create_specialty("Dermatologia", self.db_path)
        with self.assertRaises(database.ValidationError):
            database.create_appointment(
                self.patient_id,
                self.professional_id,
                dermatology_id,
                self.appointment_date,
                time(9, 0),
                time(9, 30),
                self.db_path,
            )

        with self.assertRaises(database.ValidationError):
            database.create_appointment(
                self.patient_id,
                self.professional_id,
                self.specialty_id,
                self.appointment_date,
                time(9, 30),
                time(9, 30),
                self.db_path,
            )
        with self.assertRaises(database.ValidationError):
            database.create_appointment(
                self.patient_id,
                self.professional_id,
                self.specialty_id,
                self.appointment_date,
                time(10, 0),
                time(9, 30),
                self.db_path,
            )

    def test_conflicts_are_rejected_but_adjacent_appointments_are_allowed(self) -> None:
        first_id = database.create_appointment(
            self.patient_id,
            self.professional_id,
            self.specialty_id,
            self.appointment_date,
            time(9, 0),
            time(9, 30),
            self.db_path,
        )
        with self.assertRaises(database.ScheduleConflictError):
            database.create_appointment(
                self.patient_id,
                self.professional_id,
                self.specialty_id,
                self.appointment_date,
                time(9, 15),
                time(9, 45),
                self.db_path,
            )

        adjacent_id = database.create_appointment(
            self.patient_id,
            self.professional_id,
            self.specialty_id,
            self.appointment_date,
            time(9, 30),
            time(10, 0),
            self.db_path,
        )
        self.assertNotEqual(first_id, adjacent_id)

    def test_inactive_status_frees_slot_and_confirming_checks_conflicts(self) -> None:
        first_id = database.create_appointment(
            self.patient_id,
            self.professional_id,
            self.specialty_id,
            self.appointment_date,
            time(9, 0),
            time(9, 30),
            self.db_path,
        )
        database.update_appointment_status(first_id, "cancelada", self.db_path)
        database.create_appointment(
            self.patient_id,
            self.professional_id,
            self.specialty_id,
            self.appointment_date,
            time(9, 15),
            time(9, 45),
            self.db_path,
        )

        with self.assertRaises(database.ScheduleConflictError):
            database.update_appointment_status(first_id, "confirmada", self.db_path)

    def test_demo_seed_is_explicit_and_refuses_nonempty_database(self) -> None:
        seed_path = Path(self.temp_dir.name) / "seed.sqlite3"
        database.initialize_database(seed_path)
        inserted = database.seed_demo_data(seed_path)
        self.assertEqual(inserted, 10)
        self.assertEqual(len(database.list_patients(seed_path)), 2)
        self.assertEqual(len(database.list_professionals(seed_path)), 2)
        self.assertEqual(len(database.list_specialties(seed_path)), 3)
        self.assertEqual(len(database.list_appointments(seed_path)), 3)

        with self.assertRaises(database.DemoDataRequiresEmptyDatabaseError):
            database.seed_demo_data(seed_path)
        self.assertEqual(len(database.list_patients(seed_path)), 2)

    def test_appointment_timestamps_are_persisted_in_utc_and_displayed_locally(self) -> None:
        database.create_appointment(
            self.patient_id,
            self.professional_id,
            self.specialty_id,
            self.appointment_date,
            time(9, 0),
            time(9, 30),
            self.db_path,
        )
        appointment = database.list_appointments(self.db_path)[0]
        self.assertTrue(str(appointment["inicio_em"]).endswith("+00:00"))
        self.assertEqual(
            database.format_local_timestamp(str(appointment["inicio_em"])),
            "20/05/2030 09:00",
        )


if __name__ == "__main__":
    unittest.main()
