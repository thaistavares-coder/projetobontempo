import calendar
from collections.abc import Mapping, Sequence
from datetime import date, datetime, time, timedelta
import html
from typing import Any

import streamlit as st

from services.xano import (
    CONSULTATION_TIMEZONE,
    XanoClient,
    XanoError,
    XanoHTTPError,
    XanoSettings,
    api_enabled,
    consultation_datetime_to_unix_ms,
    consultation_status_api_enabled,
    consultation_timestamp_to_local_datetime,
    consultations_api_enabled,
    consultations_write_enabled,
    professional_specialties_api_enabled,
    specialties_api_enabled,
)
from services.xano_cache import (
    XanoReadRateLimit,
    clear_xano_read_caches,
    load_consultations,
    load_consultation_statuses,
    load_professional_specialties,
    load_records,
    load_specialties,
)
from ui import apply_styles, show_page_header


MONTH_NAMES_PT = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


def _raise_cached_rate_limit(result: object) -> object:
    if isinstance(result, XanoReadRateLimit):
        raise XanoHTTPError(result.status_code)
    return result


def _to_int_id(value: object) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, str) and value.strip().isdigit():
        parsed = int(value.strip())
        return parsed if parsed > 0 else None
    return None


def _catalog_names(records: Sequence[Mapping[str, Any]]) -> dict[int, str]:
    names: dict[int, str] = {}
    for record in records:
        record_id = _to_int_id(record.get("id"))
        name = record.get("nome") or record.get("name") or record.get("titulo")
        if record_id is not None and isinstance(name, str) and name.strip():
            names[record_id] = name.strip()
    return names


def _same_schedule(
    consultations: Sequence[Mapping[str, Any]],
    professional_id: int,
    timestamp_ms: int,
    excluding_id: int | None = None,
) -> bool:
    for consultation in consultations:
        consultation_id = _to_int_id(consultation.get("id"))
        if excluding_id is not None and consultation_id == excluding_id:
            continue
        if (
            _to_int_id(consultation.get("profissional_id")) == professional_id
            and consultation.get("data_e_hora_do_agendamento") == timestamp_ms
        ):
            return True
    return False


def _status_category(status_label: str) -> str:
    normalized = status_label.strip().lower()
    if "cancel" in normalized:
        return "canceled"
    if (
        "confirm" in normalized
        or "realiz" in normalized
        or "conclu" in normalized
    ):
        return "confirmed"
    return "scheduled"


def _inject_consultations_styles() -> None:
    st.markdown(
        """<style>
.consult-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
    gap: 14px;
    margin-top: 8px;
    margin-bottom: 12px;
}
.consult-card {
    background: #ffffff;
    border: 1px solid #d8e6e3;
    border-left: 5px solid #0d9488;
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.consult-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.08);
}
.consult-card--canceled {
    background: #fef2f2;
    border-color: #fecaca;
    border-left: 5px solid #dc2626;
}
.consult-card--confirmed {
    background: #f0fdf4;
    border-color: #bbf7d0;
    border-left: 5px solid #16a34a;
}
.consult-card__top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}
.consult-card__datetime {
    font-size: 0.85rem;
    font-weight: 700;
    color: #0f172a;
}
.consult-badge {
    font-size: 0.74rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 999px;
    letter-spacing: 0.02em;
    white-space: nowrap;
}
.consult-badge--scheduled {
    background: #ccfbf1;
    color: #0f766e;
}
.consult-badge--confirmed {
    background: #dcfce7;
    color: #15803d;
}
.consult-badge--canceled {
    background: #fee2e2;
    color: #b91c1c;
}
.consult-card__patient {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 6px;
}
.consult-card__meta {
    font-size: 0.88rem;
    color: #334155;
    line-height: 1.5;
}
.consult-card__obs {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px dashed rgba(148, 163, 184, 0.45);
    font-size: 0.82rem;
    color: #475569;
}
.cal-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 6px;
    table-layout: fixed;
    margin-top: 6px;
}
.cal-table th {
    text-align: center;
    font-size: 0.8rem;
    font-weight: 700;
    color: #475569;
    padding: 6px 0;
    text-transform: uppercase;
}
.cal-cell {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    vertical-align: top;
    height: 104px;
    padding: 6px 8px;
}
.cal-cell--empty {
    background: #f8fafc;
    border-color: #f1f5f9;
}
.cal-cell--today {
    border: 2px solid #0d9488;
    background: #f0fdfa;
}
.cal-day-num {
    font-size: 0.82rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 4px;
}
.cal-pill {
    display: block;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 6px;
    margin-bottom: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    background: #ccfbf1;
    color: #0f766e;
}
.cal-pill--canceled {
    background: #fee2e2;
    color: #b91c1c;
    text-decoration: line-through;
}
.cal-pill--confirmed {
    background: #dcfce7;
    color: #15803d;
}
</style>""",
        unsafe_allow_html=True,
    )


def _render_consultation_cards(items: Sequence[dict[str, Any]]) -> None:
    cards_html: list[str] = ['<div class="consult-grid">']
    for item in items:
        category = _status_category(item["status"])
        card_cls = f"consult-card consult-card--{category}"
        badge_cls = f"consult-badge consult-badge--{category}"
        dt_str = html.escape(item["local_dt"].strftime("%d/%m/%Y · %H:%M"))
        status_str = html.escape(item["status"])
        patient_str = html.escape(item["paciente"])
        prof_str = html.escape(item["profissional"])
        spec_str = html.escape(item["especialidade"])
        id_str = html.escape(str(item["id"]))
        obs_raw = (item.get("observacoes") or "").strip()
        obs_html = (
            f'<div class="consult-card__obs">📝 {html.escape(obs_raw)}</div>'
            if obs_raw
            else ""
        )
        cards_html.append(
            f'<div class="{card_cls}">'
            f'<div class="consult-card__top">'
            f'<span class="consult-card__datetime">🗓️ {dt_str} · #{id_str}</span>'
            f'<span class="{badge_cls}">{status_str}</span>'
            f"</div>"
            f'<div class="consult-card__patient">👤 {patient_str}</div>'
            f'<div class="consult-card__meta">'
            f"<div>🩺 <strong>Profissional:</strong> {prof_str}</div>"
            f"<div>🏷️ <strong>Especialidade:</strong> {spec_str}</div>"
            f"</div>"
            f"{obs_html}"
            f"</div>"
        )
    cards_html.append("</div>")
    st.markdown("".join(cards_html), unsafe_allow_html=True)


def _render_month_calendar(
    year: int,
    month: int,
    items: Sequence[dict[str, Any]],
    today_date: date,
) -> None:
    by_day: dict[date, list[dict[str, Any]]] = {}
    for item in items:
        day_key = item["local_dt"].date()
        by_day.setdefault(day_key, []).append(item)

    cal = calendar.Calendar(firstweekday=6)
    weeks = cal.monthdatescalendar(year, month)

    html_parts = [
        '<table class="cal-table">',
        "<thead><tr>"
        "<th>Dom</th><th>Seg</th><th>Ter</th><th>Qua</th>"
        "<th>Qui</th><th>Sex</th><th>Sáb</th>"
        "</tr></thead><tbody>",
    ]
    for week in weeks:
        html_parts.append("<tr>")
        for day_obj in week:
            if day_obj.month != month:
                html_parts.append(
                    f'<td class="cal-cell cal-cell--empty">'
                    f'<div class="cal-day-num" style="color:#94a3b8;">{day_obj.day}</div>'
                    f"</td>"
                )
                continue

            today_cls = " cal-cell--today" if day_obj == today_date else ""
            day_events = sorted(
                by_day.get(day_obj, []),
                key=lambda x: x["local_dt"],
            )
            pills: list[str] = []
            for ev in day_events[:3]:
                cat = _status_category(ev["status"])
                pill_cls = (
                    f"cal-pill cal-pill--{cat}"
                    if cat in ("canceled", "confirmed")
                    else "cal-pill"
                )
                hora = ev["local_dt"].strftime("%H:%M")
                pac = html.escape(ev["paciente"].split()[0])
                pills.append(
                    f'<span class="{pill_cls}" title="{html.escape(ev["paciente"])} ({html.escape(ev["status"])})">'
                    f"{hora} {pac}</span>"
                )
            if len(day_events) > 3:
                pills.append(
                    f'<span class="cal-pill">+{len(day_events) - 3} mais</span>'
                )

            html_parts.append(
                f'<td class="cal-cell{today_cls}">'
                f'<div class="cal-day-num">{day_obj.day}</div>'
                f"{''.join(pills)}"
                f"</td>"
            )
        html_parts.append("</tr>")
    html_parts.append("</tbody></table>")
    st.markdown("".join(html_parts), unsafe_allow_html=True)


apply_styles()
_inject_consultations_styles()
show_page_header(
    "Consultas",
    "Gerencie consultas e horários integrados ao Xano.",
    ":material/calendar_month:",
)

feedback = st.session_state.pop("consultations_feedback", None)
if feedback:
    st.success(feedback)

settings = XanoSettings.from_environment()
client = XanoClient(settings)

if not consultations_api_enabled():
    st.warning(
        "A leitura de Consultas está desabilitada. Defina "
        "XANO_CONSULTAS_API_ENABLED=true para conectar esta página ao Xano."
    )
    st.stop()

if not settings.consultations_base_url or not settings.consultations_base_url.strip():
    st.error("XANO_CONSULTAS_BASE_URL não está configurada.")
    st.stop()

consultations: list[dict[str, Any]] = []
statuses: list[dict[str, Any]] = []
patients: list[dict[str, Any]] = []
professionals: list[dict[str, Any]] = []
specialties: list[dict[str, Any]] = []
associations: list[dict[str, int]] = []

read_failed = False
try:
    consultations = list(
        _raise_cached_rate_limit(
            load_consultations(
                settings.consultations_base_url,
                settings.authorization,
            )
        )
    )
except XanoError as error:
    read_failed = True
    st.error(f"Não foi possível carregar Consultas do Xano: {error}")

if consultation_status_api_enabled():
    try:
        statuses = list(
            _raise_cached_rate_limit(
                load_consultation_statuses(
                    settings.statuses_base_url or "",
                    settings.authorization,
                )
            )
        )
    except XanoError as error:
        read_failed = True
        st.error(f"Não foi possível carregar Status de Consulta: {error}")
else:
    st.warning("XANO_STATUS_CONSULTA_API_ENABLED=true não está habilitado.")

if api_enabled():
    try:
        patients = list(
            _raise_cached_rate_limit(
                load_records(
                    "pacientes",
                    settings.patients_base_url or "",
                    settings.authorization,
                )
            )
        )
    except XanoError as error:
        read_failed = True
        st.error(f"Não foi possível carregar Pacientes: {error}")
    try:
        professionals = list(
            _raise_cached_rate_limit(
                load_records(
                    "profissionais",
                    settings.professionals_base_url or "",
                    settings.authorization,
                )
            )
        )
    except XanoError as error:
        read_failed = True
        st.error(f"Não foi possível carregar Profissionais: {error}")
else:
    st.warning("A leitura de Pacientes e Profissionais está desabilitada.")

if specialties_api_enabled():
    try:
        specialties = list(
            _raise_cached_rate_limit(
                load_specialties(
                    settings.specialties_base_url or "",
                    settings.authorization,
                )
            )
        )
        if not specialties:
            specialties = client.list_specialties()
    except XanoError as error:
        read_failed = True
        st.error(f"Não foi possível carregar Especialidades: {error}")
else:
    st.warning("XANO_ESPECIALIDADES_API_ENABLED=true não está habilitado.")

if professional_specialties_api_enabled():
    try:
        associations = list(
            _raise_cached_rate_limit(
                load_professional_specialties(
                    settings.professional_specialties_base_url or "",
                    settings.authorization,
                )
            )
        )
    except XanoError as error:
        read_failed = True
        st.error(
            "Não foi possível carregar vínculos "
            f"Profissional–Especialidade: {error}"
        )
else:
    st.warning(
        "XANO_PROFISSIONAL_ESPECIALIDADES_API_ENABLED=true não está habilitado."
    )

patient_names = _catalog_names(patients)
professional_names = _catalog_names(professionals)
specialty_names = _catalog_names(specialties)
status_names = _catalog_names(statuses)

valid_associations: dict[int, set[int]] = {}
invalid_associations = 0
seen_associations: set[tuple[int, int]] = set()
for association in associations:
    professional_id = _to_int_id(association.get("profissional_id"))
    specialty_id = _to_int_id(association.get("especialidade_id"))
    if (
        professional_id is None
        or specialty_id is None
        or professional_id not in professional_names
        or specialty_id not in specialty_names
    ):
        invalid_associations += 1
        continue
    pair = (professional_id, specialty_id)
    if pair in seen_associations:
        invalid_associations += 1
        continue
    seen_associations.add(pair)
    valid_associations.setdefault(professional_id, set()).add(specialty_id)

if invalid_associations:
    st.error(
        f"{invalid_associations} vínculo(s) inválido(s) ou duplicado(s) "
        "foram bloqueados."
    )

write_enabled = (
    not read_failed
    and consultations_write_enabled()
    and bool(patient_names)
    and bool(professional_names)
    and bool(specialty_names)
    and bool(status_names)
)

# --- BOTÃO RECOLHÍVEL PARA NOVA CONSULTA + ATUALIZAR CACHE ---
if "show_create_consultation_form" not in st.session_state:
    st.session_state["show_create_consultation_form"] = False

if not st.session_state["show_create_consultation_form"]:
    col_btn, _, col_refresh = st.columns([1.4, 3.3, 1.3])
    with col_btn:
        if st.button(
            "Nova consulta",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["show_create_consultation_form"] = True
            st.rerun()
    with col_refresh:
        if st.button(
            "🔄 Atualizar",
            key="refresh_consultations_cache",
            type="secondary",
            use_container_width=True,
        ):
            clear_xano_read_caches()
            st.rerun()
else:
    _, col_close = st.columns([5, 1])
    with col_close:
        if st.button(
            "Fechar",
            key="close_create_consultation",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state["show_create_consultation_form"] = False
            st.rerun()

    with st.container(border=True):
        st.subheader("Cadastrar consulta")
        if not write_enabled:
            st.info(
                "As gravações estão desabilitadas. Defina "
                "XANO_CONSULTAS_WRITE_ENABLED=true no .env."
            )

        professional_id = st.selectbox(
            "Profissional *",
            options=list(professional_names),
            index=None,
            placeholder="Selecione uma opção",
            format_func=lambda item_id: (
                f"{professional_names[item_id]} (#{item_id})"
            ),
            key="xano_create_professional",
        )
        available_specialty_ids = (
            sorted(valid_associations.get(professional_id, set()))
            if professional_id is not None
            else []
        )

        with st.form("xano_create_consultation", clear_on_submit=True):
            patient_id = st.selectbox(
                "Paciente *",
                options=list(patient_names),
                index=None,
                placeholder="Selecione uma opção",
                format_func=lambda item_id: (
                    f"{patient_names[item_id]} (#{item_id})"
                ),
                key="xano_create_patient",
            )
            specialty_id = st.selectbox(
                "Especialidade *",
                options=available_specialty_ids,
                index=None,
                placeholder=(
                    "Nenhum vínculo disponível"
                    if professional_id is not None
                    else "Selecione um profissional"
                ),
                disabled=not available_specialty_ids,
                format_func=lambda item_id: (
                    f"{specialty_names[item_id]} (#{item_id})"
                ),
                key="xano_create_specialty",
            )
            status_id = st.selectbox(
                "Status *",
                options=list(status_names),
                index=None,
                placeholder="Selecione uma opção",
                format_func=lambda item_id: (
                    f"{status_names[item_id]} (#{item_id})"
                ),
                key="xano_create_status",
            )
            col_d, col_t = st.columns(2)
            with col_d:
                appointment_date = st.date_input(
                    "Data da consulta *",
                    value=datetime.now(CONSULTATION_TIMEZONE).date(),
                    key="xano_create_date",
                )
            with col_t:
                appointment_time = st.time_input(
                    "Horário da consulta *",
                    value=time(9, 0),
                    key="xano_create_time",
                )
            observations = st.text_area(
                "Observações (opcional)",
                key="xano_create_observacoes",
            )
            submitted = st.form_submit_button(
                "Cadastrar consulta",
                type="primary",
                disabled=not write_enabled,
            )

        if submitted:
            if (
                patient_id is None
                or professional_id is None
                or specialty_id is None
                or status_id is None
            ):
                st.error(
                    "Paciente, profissional, especialidade e status são obrigatórios."
                )
            elif appointment_date < date.today():
                st.error(
                    "Não é permitido agendar uma consulta em data passada."
                )
            else:
                timestamp_ms = consultation_datetime_to_unix_ms(
                    appointment_date,
                    appointment_time,
                )
                if _same_schedule(
                    consultations,
                    professional_id,
                    timestamp_ms,
                ):
                    st.error(
                        "Já existe uma consulta para este profissional no mesmo instante."
                    )
                else:
                    payload = {
                        "paciente_id": patient_id,
                        "profissional_id": professional_id,
                        "especialidade_id": specialty_id,
                        "data_e_hora_do_agendamento": timestamp_ms,
                        "status_consulta_id": status_id,
                        "observacoes": (
                            observations if observations.strip() else None
                        ),
                    }
                    try:
                        with st.spinner("Cadastrando consulta no Xano..."):
                            client.create_consultation(payload)
                    except XanoError as error:
                        st.error(
                            f"Não foi possível cadastrar a consulta: {error}"
                        )
                    else:
                        clear_xano_read_caches()
                        st.session_state["show_create_consultation_form"] = False
                        st.session_state["consultations_feedback"] = (
                            "Consulta cadastrada no Xano."
                        )
                        st.rerun()

st.divider()
st.subheader("Agenda e consultas")

enriched_consultations: list[dict[str, Any]] = []
invalid_timestamp = False
for consultation in consultations:
    try:
        local_datetime = consultation_timestamp_to_local_datetime(
            consultation["data_e_hora_do_agendamento"]
        )
    except (KeyError, ValueError):
        invalid_timestamp = True
        break

    cid = _to_int_id(consultation.get("id")) or consultation.get("id")
    pid = _to_int_id(consultation.get("paciente_id"))
    prof_id = _to_int_id(consultation.get("profissional_id"))
    spec_id = _to_int_id(consultation.get("especialidade_id"))
    stat_id = _to_int_id(consultation.get("status_consulta_id"))

    enriched_consultations.append(
        {
            "id": cid,
            "paciente": (
                patient_names.get(pid, f"ID {consultation.get('paciente_id')}")
                if pid is not None
                else f"ID {consultation.get('paciente_id')}"
            ),
            "profissional": (
                professional_names.get(
                    prof_id, f"ID {consultation.get('profissional_id')}"
                )
                if prof_id is not None
                else f"ID {consultation.get('profissional_id')}"
            ),
            "especialidade": (
                specialty_names.get(
                    spec_id, f"ID {consultation.get('especialidade_id')}"
                )
                if spec_id is not None
                else f"ID {consultation.get('especialidade_id')}"
            ),
            "status": (
                status_names.get(
                    stat_id, f"ID {consultation.get('status_consulta_id')}"
                )
                if stat_id is not None
                else f"ID {consultation.get('status_consulta_id')}"
            ),
            "local_dt": local_datetime,
            "observacoes": consultation.get("observacoes"),
        }
    )

enriched_consultations.sort(key=lambda item: item["local_dt"])

if invalid_timestamp:
    st.error("A lista contém uma Consulta com timestamp incompatível.")
elif not enriched_consultations:
    st.info("Nenhuma consulta foi retornada pelo Xano.")
else:
    tab_cards, tab_calendar = st.tabs(
        ["🗂️ Cards e filtros", "📅 Calendário mensal"]
    )

    today_local = datetime.now(CONSULTATION_TIMEZONE).date()
    week_start = today_local - timedelta(days=today_local.weekday())
    week_end = week_start + timedelta(days=6)

    with tab_cards:
        col_f1, col_f2, col_f3 = st.columns([1.3, 1.3, 2.0])
        with col_f1:
            period_filter = st.selectbox(
                "Período",
                [
                    "Todas",
                    "Hoje",
                    "Esta semana",
                    "Próximas",
                    "Passadas",
                ],
                key="consult_period_filter",
            )
        with col_f2:
            status_filter = st.selectbox(
                "Status",
                [
                    "Todos",
                    "Ativas (não canceladas)",
                    "Canceladas",
                ],
                key="consult_status_filter",
            )
        with col_f3:
            search_query = st.text_input(
                "Buscar paciente, profissional ou especialidade",
                placeholder="Digite para filtrar...",
                key="consult_search_filter",
            ).strip().lower()

        filtered_items: list[dict[str, Any]] = []
        for item in enriched_consultations:
            item_date = item["local_dt"].date()
            if period_filter == "Hoje" and item_date != today_local:
                continue
            if period_filter == "Esta semana" and not (
                week_start <= item_date <= week_end
            ):
                continue
            if period_filter == "Próximas" and item_date < today_local:
                continue
            if period_filter == "Passadas" and item_date >= today_local:
                continue

            cat = _status_category(item["status"])
            if status_filter == "Canceladas" and cat != "canceled":
                continue
            if (
                status_filter == "Ativas (não canceladas)"
                and cat == "canceled"
            ):
                continue

            if search_query:
                searchable = (
                    f"{item['paciente']} {item['profissional']} "
                    f"{item['especialidade']} #{item['id']}"
                ).lower()
                if search_query not in searchable:
                    continue

            filtered_items.append(item)

        st.caption(
            f"Exibindo **{len(filtered_items)}** de **{len(enriched_consultations)}** consulta(s)."
        )
        if filtered_items:
            _render_consultation_cards(filtered_items)
        else:
            st.info("Nenhuma consulta encontrada para os filtros selecionados.")

    with tab_calendar:
        if "cal_year" not in st.session_state:
            st.session_state["cal_year"] = today_local.year
        if "cal_month" not in st.session_state:
            st.session_state["cal_month"] = today_local.month

        c_prev, c_title, c_next = st.columns([1, 3, 1])
        with c_prev:
            if st.button("◀ Mês anterior", use_container_width=True):
                if st.session_state["cal_month"] == 1:
                    st.session_state["cal_month"] = 12
                    st.session_state["cal_year"] -= 1
                else:
                    st.session_state["cal_month"] -= 1
                st.rerun()
        with c_title:
            m_name = MONTH_NAMES_PT[st.session_state["cal_month"]]
            st.markdown(
                f"<h4 style='text-align:center;margin:4px 0;'>"
                f"{m_name} de {st.session_state['cal_year']}</h4>",
                unsafe_allow_html=True,
            )
        with c_next:
            if st.button("Próximo mês ▶", use_container_width=True):
                if st.session_state["cal_month"] == 12:
                    st.session_state["cal_month"] = 1
                    st.session_state["cal_year"] += 1
                else:
                    st.session_state["cal_month"] += 1
                st.rerun()

        _render_month_calendar(
            st.session_state["cal_year"],
            st.session_state["cal_month"],
            enriched_consultations,
            today_local,
        )

        st.markdown("##### Detalhes de um dia específico")
        selected_cal_day = st.date_input(
            "Selecione uma data para ver as consultas do dia",
            value=today_local,
            key="cal_selected_day_detail",
        )
        day_items = [
            item
            for item in enriched_consultations
            if item["local_dt"].date() == selected_cal_day
        ]
        if day_items:
            _render_consultation_cards(day_items)
        else:
            st.info(
                f"Nenhuma consulta agendada para {selected_cal_day.strftime('%d/%m/%Y')}."
            )

st.divider()
st.subheader("Consultar, editar ou excluir")

consultation_ids = [
    int(consultation["id"])
    for consultation in consultations
    if isinstance(consultation.get("id"), int)
    and consultation["id"] > 0
]

if not consultation_ids:
    st.info("Não há consultas válidas para consultar ou editar.")
else:
    consultation_labels = {
        item["id"]: (
            f"#{item['id']} · {item['paciente']} ({item['local_dt'].strftime('%d/%m/%Y %H:%M')}) — {item['status']}"
        )
        for item in enriched_consultations
    }
    consultation_id = st.selectbox(
        "Consulta",
        options=consultation_ids,
        index=None,
        placeholder="Selecione uma consulta",
        format_func=lambda cid: consultation_labels.get(cid, f"Consulta #{cid}"),
        key="xano_edit_consultation_id",
    )
    if st.button(
        "Carregar consulta",
        key="xano_load_consultation",
        disabled=consultation_id is None,
    ):
        try:
            record = client.get_consultation(consultation_id)
        except XanoError as error:
            st.error(f"Não foi possível carregar a Consulta: {error}")
        else:
            st.session_state["xano_consultation_edit"] = record
            st.rerun()

    record = st.session_state.get("xano_consultation_edit")
    if (
        isinstance(record, dict)
        and consultation_id is not None
        and record.get("id") == consultation_id
    ):
        local_datetime = consultation_timestamp_to_local_datetime(
            record["data_e_hora_do_agendamento"]
        )
        edit_professional_id = st.selectbox(
            "Profissional *",
            options=list(professional_names),
            index=(
                list(professional_names).index(record["profissional_id"])
                if record["profissional_id"] in professional_names
                else None
            ),
            format_func=lambda item_id: (
                f"{professional_names[item_id]} (#{item_id})"
            ),
            key="xano_edit_professional",
        )
        edit_specialty_ids = (
            sorted(valid_associations.get(edit_professional_id, set()))
            if edit_professional_id is not None
            else []
        )

        with st.form("xano_edit_consultation"):
            edit_patient_id = st.selectbox(
                "Paciente *",
                options=list(patient_names),
                index=(
                    list(patient_names).index(record["paciente_id"])
                    if record["paciente_id"] in patient_names
                    else None
                ),
                format_func=lambda item_id: (
                    f"{patient_names[item_id]} (#{item_id})"
                ),
                key="xano_edit_patient",
            )
            edit_specialty_id = st.selectbox(
                "Especialidade *",
                options=edit_specialty_ids,
                index=(
                    edit_specialty_ids.index(record["especialidade_id"])
                    if record["especialidade_id"] in edit_specialty_ids
                    else None
                ),
                placeholder="Nenhum vínculo disponível",
                disabled=not edit_specialty_ids,
                format_func=lambda item_id: (
                    f"{specialty_names[item_id]} (#{item_id})"
                ),
                key="xano_edit_specialty",
            )
            edit_status_id = st.selectbox(
                "Status *",
                options=list(status_names),
                index=(
                    list(status_names).index(record["status_consulta_id"])
                    if record["status_consulta_id"] in status_names
                    else None
                ),
                format_func=lambda item_id: (
                    f"{status_names[item_id]} (#{item_id})"
                ),
                key="xano_edit_status",
            )
            edit_date = st.date_input(
                "Data da consulta *",
                value=local_datetime.date(),
                key="xano_edit_date",
            )
            edit_time = st.time_input(
                "Horário da consulta *",
                value=local_datetime.time().replace(tzinfo=None),
                key="xano_edit_time",
            )
            edit_observations = st.text_area(
                "Observações (opcional)",
                value=record.get("observacoes") or "",
                key="xano_edit_observacoes",
            )
            edit_submitted = st.form_submit_button(
                "Salvar alterações",
                disabled=not write_enabled,
            )

        if edit_submitted:
            if (
                edit_patient_id is None
                or edit_professional_id is None
                or edit_specialty_id is None
                or edit_status_id is None
            ):
                st.error(
                    "Paciente, profissional, especialidade e status são obrigatórios."
                )
            elif edit_date < date.today():
                st.error(
                    "Não é permitido definir uma consulta em data passada."
                )
            else:
                edit_timestamp = consultation_datetime_to_unix_ms(
                    edit_date,
                    edit_time,
                )
                if _same_schedule(
                    consultations,
                    edit_professional_id,
                    edit_timestamp,
                    excluding_id=consultation_id,
                ):
                    st.error(
                        "Já existe outra consulta para este profissional "
                        "no mesmo instante."
                    )
                else:
                    payload: dict[str, Any] = {}
                    if edit_patient_id != record["paciente_id"]:
                        payload["paciente_id"] = edit_patient_id
                    if edit_professional_id != record["profissional_id"]:
                        payload["profissional_id"] = edit_professional_id
                    if edit_specialty_id != record["especialidade_id"]:
                        payload["especialidade_id"] = edit_specialty_id
                    if edit_status_id != record["status_consulta_id"]:
                        payload["status_consulta_id"] = edit_status_id
                    if edit_timestamp != record["data_e_hora_do_agendamento"]:
                        payload["data_e_hora_do_agendamento"] = edit_timestamp
                    new_observations = (
                        edit_observations if edit_observations.strip() else None
                    )
                    if new_observations != record.get("observacoes"):
                        payload["observacoes"] = new_observations
                    if not payload:
                        st.info("Nenhuma alteração foi informada.")
                    else:
                        try:
                            with st.spinner("Atualizando consulta no Xano..."):
                                client.update_consultation(
                                    consultation_id,
                                    payload,
                                )
                        except XanoError as error:
                            st.error(
                                f"Não foi possível atualizar a consulta: {error}"
                            )
                        else:
                            clear_xano_read_caches()
                            st.session_state.pop(
                                "xano_consultation_edit",
                                None,
                            )
                            st.session_state["consultations_feedback"] = (
                                "Consulta atualizada no Xano."
                            )
                            st.rerun()

        st.subheader("Excluir consulta")
        confirmed = st.checkbox(
            f"Confirmo a exclusão da consulta #{consultation_id}",
            key=f"xano_delete_confirm_{consultation_id}",
            disabled=not write_enabled,
        )
        if st.button(
            "Excluir consulta",
            key="xano_delete_consultation",
            type="secondary",
            disabled=not write_enabled or not confirmed,
        ):
            try:
                with st.spinner("Excluindo consulta no Xano..."):
                    client.delete_consultation(consultation_id)
            except XanoError as error:
                st.error(f"Não foi possível excluir a consulta: {error}")
            else:
                clear_xano_read_caches()
                st.session_state.pop("xano_consultation_edit", None)
                st.session_state["consultations_feedback"] = (
                    "Consulta excluída no Xano."
                )
                st.rerun()

st.caption(
    "A página usa somente APIs Xano. O frontend bloqueia o mesmo instante "
    "para o mesmo profissional; disponibilidade, duração e conflitos definitivos "
    "devem ser confirmados no backend."
)