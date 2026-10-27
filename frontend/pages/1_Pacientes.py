import streamlit as st

from services.validation import validate_contact
from services.xano import (
    XanoClient,
    XanoError,
    XanoSettings,
    api_enabled,
)
from ui import apply_styles, show_page_header


RESOURCE = "pacientes"

apply_styles()
show_page_header(
    "Pacientes",
    "Consulte e organize as informações dos pacientes do consultório.",
    "👥",
)

feedback = st.session_state.pop("patients_feedback", None)
if feedback:
    st.success(feedback)

settings = XanoSettings.from_environment()
client = XanoClient(settings)
enabled = api_enabled()

if not settings.patients_base_url or not settings.patients_base_url.strip():
    st.warning(
        "A URL da API de Pacientes não está configurada. Defina "
        "XANO_PACIENTES_BASE_URL no ambiente da aplicação."
    )
    enabled = False
elif not enabled:
    st.info(
        "A integração com o Xano está desabilitada. Defina "
        "XANO_API_ENABLED=true para permitir chamadas à API."
    )

with st.form("create_patient", clear_on_submit=True):
    st.subheader("Cadastrar paciente")
    name = st.text_input("Nome *", key="patient_create_name")
    phone = st.text_input("Telefone *", key="patient_create_phone")
    email = st.text_input("Email", key="patient_create_email")
    create_submitted = st.form_submit_button(
        "Cadastrar paciente",
        type="primary",
        disabled=not enabled,
    )

if create_submitted:
    validation_error = validate_contact(name, phone, email)
    if validation_error:
        st.error(validation_error)
    else:
        try:
            client.create_record(
                RESOURCE,
                {
                    "nome": name,
                    "telefone": phone,
                    "email": email or None,
                },
            )
        except XanoError as error:
            st.error(f"Não foi possível cadastrar o paciente: {error}")
        else:
            st.session_state["patients_feedback"] = "Paciente cadastrado."
            st.rerun()

st.divider()
st.subheader("Pacientes cadastrados")

patients: list[dict[str, object]] = []
list_succeeded = False
if enabled:
    try:
        patients = client.list_records(RESOURCE)
    except XanoError as error:
        st.error(f"Não foi possível carregar pacientes do Xano: {error}")
    else:
        list_succeeded = True
        if patients:
            st.dataframe(patients, hide_index=True, width="stretch")
        else:
            st.info("Nenhum paciente cadastrado no Xano.")

if list_succeeded and patients:
    with st.expander("Editar paciente"):
        patient_ids = [int(patient["id"]) for patient in patients]
        selected_id = st.selectbox(
            "Paciente",
            patient_ids,
            format_func=lambda patient_id: next(
                f"{patient['nome']} · ID {patient_id}"
                for patient in patients
                if patient["id"] == patient_id
            ),
            key="patient_edit_selection",
        )
        if st.button(
            "Carregar paciente",
            key="patient_load",
            disabled=not enabled,
        ):
            try:
                loaded_patient = client.get_record(RESOURCE, selected_id)
            except XanoError as error:
                st.error(f"Não foi possível carregar o paciente: {error}")
            else:
                for field in ("name", "phone", "email"):
                    st.session_state.pop(
                        f"patient_edit_{field}_{selected_id}", None
                    )
                st.session_state["patient_edit_record"] = loaded_patient

        patient_to_edit = st.session_state.get("patient_edit_record")
        if patient_to_edit:
            edit_id = int(patient_to_edit["id"])
            with st.form(f"edit_patient_{edit_id}"):
                edit_name = st.text_input(
                    "Nome *",
                    value=str(patient_to_edit["nome"]),
                    key=f"patient_edit_name_{edit_id}",
                )
                edit_phone = st.text_input(
                    "Telefone *",
                    value=str(patient_to_edit.get("telefone") or ""),
                    key=f"patient_edit_phone_{edit_id}",
                )
                edit_email = st.text_input(
                    "Email",
                    value=str(patient_to_edit.get("email") or ""),
                    key=f"patient_edit_email_{edit_id}",
                )
                update_submitted = st.form_submit_button(
                    "Salvar alterações",
                    disabled=not enabled,
                )
            if update_submitted:
                validation_error = validate_contact(
                    edit_name, edit_phone, edit_email
                )
                if validation_error:
                    st.error(validation_error)
                else:
                    try:
                        client.update_record(
                            RESOURCE,
                            edit_id,
                            {
                                "nome": edit_name.strip(),
                                "telefone": edit_phone.strip(),
                                "email": edit_email.strip() or None,
                            },
                        )
                    except XanoError as error:
                        st.error(f"Não foi possível atualizar o paciente: {error}")
                    else:
                        st.session_state.pop("patient_edit_record", None)
                        st.session_state["patients_feedback"] = (
                            "Paciente atualizado."
                        )
                        st.rerun()

    st.subheader("Excluir paciente")
    for patient in patients:
        patient_id = int(patient["id"])
        with st.container(border=True):
            st.write(f"{patient['nome']} · ID {patient_id}")
            confirmed = st.checkbox(
                f"Confirmo a exclusão de {patient['nome']}",
                key=f"patient_delete_confirm_{patient_id}",
                disabled=not enabled,
            )
            if st.button(
                "Excluir paciente",
                key=f"patient_delete_{patient_id}",
                type="secondary",
                disabled=not enabled or not confirmed,
            ):
                try:
                    client.delete_record(RESOURCE, patient_id)
                except XanoError as error:
                    st.error(f"Não foi possível excluir o paciente: {error}")
                else:
                    st.session_state.pop("patient_edit_record", None)
                    st.session_state["patients_feedback"] = (
                        "Paciente excluído."
                    )
                    st.rerun()
