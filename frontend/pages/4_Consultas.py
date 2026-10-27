from datetime import date, time

import streamlit as st

from services import database
from ui import apply_styles, show_page_header


apply_styles()
show_page_header(
    "Consultas",
    "Agende consultas locais, evite conflitos de horário e acompanhe o status.",
    ":material/calendar_month:",
)

pacientes = database.list_patients()
profissionais = database.list_professionals()

if not pacientes:
    st.info("Cadastre ao menos um paciente antes de agendar consultas.")
if not profissionais:
    st.info("Cadastre ao menos um profissional antes de agendar consultas.")

if pacientes and profissionais:
    patient_names = {
        int(patient["id"]): str(patient["nome"]) for patient in pacientes
    }
    professional_names = {
        int(professional["id"]): str(professional["nome"])
        for professional in profissionais
    }
    professional_id = st.selectbox(
        "Profissional *",
        options=list(professional_names),
        index=None,
        placeholder="Selecione uma opção",
        format_func=lambda item_id: professional_names[item_id],
        label_visibility="visible",
    )
    professional_specialties = (
        database.list_professional_specialties(professional_id)
        if professional_id is not None
        else []
    )
    specialty_names = {
        int(specialty["id"]): str(specialty["nome"])
        for specialty in database.list_specialties()
    }
    available_specialties = [
        specialty_id
        for specialty_id in professional_specialties
        if specialty_id in specialty_names
    ]

    if professional_id is None:
        st.info("Selecione um profissional para consultar suas especialidades.")
    elif not available_specialties:
        st.warning(
            "Vincule uma especialidade ao profissional antes de agendar uma consulta."
        )
    else:
        with st.form("cadastro_consulta", clear_on_submit=True):
            st.caption("* Campos obrigatórios.")
            patient_id = st.selectbox(
                "Paciente *",
                options=[int(patient["id"]) for patient in pacientes],
                index=None,
                placeholder="Selecione uma opção",
                format_func=lambda item_id: patient_names[item_id],
                label_visibility="visible",
            )
            specialty_id = st.selectbox(
                "Especialidade *",
                options=available_specialties,
                index=None,
                placeholder="Selecione uma opção",
                format_func=lambda item_id: specialty_names[item_id],
                label_visibility="visible",
            )
            appointment_date = st.date_input(
                "Data da consulta *",
                value=date.today(),
                label_visibility="visible",
            )
            start_time = st.time_input(
                "Horário de início *",
                value=time(9, 0),
                label_visibility="visible",
            )
            end_time = st.time_input(
                "Horário de término *",
                value=time(9, 30),
                label_visibility="visible",
            )
            cadastrar = st.form_submit_button(
                "Agendar consulta",
                type="primary",
                icon=":material/event_available:",
            )

        if cadastrar:
            try:
                database.create_appointment(
                    patient_id,
                    professional_id,
                    specialty_id,
                    appointment_date,
                    start_time,
                    end_time,
                )
                st.success("Consulta agendada.")
                st.rerun()
            except database.ValidationError as error:
                st.error(str(error))
            except database.ScheduleConflictError as error:
                st.error(str(error))
            except database.DatabaseError as error:
                st.error(f"Não foi possível agendar a consulta: {error}")
else:
    professional_id = None

st.divider()
st.subheader("Consultas cadastradas")
consultas = database.list_appointments()
if consultas:
    table_rows = [
        {
            "ID": consultation["id"],
            "Data e hora inicial": database.format_local_timestamp(
                str(consultation["inicio_em"])
            ),
            "Data e hora final": database.format_local_timestamp(
                str(consultation["fim_em"])
            ),
            "Paciente": consultation["paciente_nome"],
            "Profissional": consultation["profissional_nome"],
            "Especialidade": consultation["especialidade_nome"],
            "Status": consultation["status_nome"],
        }
        for consultation in consultas
    ]
    st.dataframe(table_rows, hide_index=True, use_container_width=True)

    status_options = database.get_statuses()
    status_codes = [str(status["codigo"]) for status in status_options]
    status_names = {
        str(status["codigo"]): str(status["nome"]) for status in status_options
    }
    st.subheader("Atualizar status")
    consultation_ids = [int(item["id"]) for item in consultas]
    consultation_labels = {
        int(item["id"]): (
            f"#{item['id']} · {item['paciente_nome']} · "
            f"{database.format_local_timestamp(str(item['inicio_em']))}"
        )
        for item in consultas
    }
    with st.form("atualizar_status_consulta"):
        consultation_id = st.selectbox(
            "Consulta *",
            options=consultation_ids,
            index=None,
            placeholder="Selecione uma opção",
            format_func=lambda item_id: consultation_labels[item_id],
            label_visibility="visible",
        )
        new_status = st.selectbox(
            "Status *",
            options=status_codes,
            index=None,
            placeholder="Selecione uma opção",
            format_func=lambda code: status_names[code],
            label_visibility="visible",
        )
        atualizar = st.form_submit_button("Atualizar status")

    if atualizar:
        try:
            database.update_appointment_status(consultation_id, new_status)
            st.success("Status da consulta atualizado.")
            st.rerun()
        except database.ScheduleConflictError as error:
            st.error(str(error))
        except database.DatabaseError as error:
            st.error(f"Não foi possível atualizar o status: {error}")
else:
    st.info("Nenhuma consulta cadastrada neste banco SQLite local.")
