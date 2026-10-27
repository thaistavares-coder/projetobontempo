import streamlit as st

from services.validation import validate_contact
from services.xano import (
    XanoClient,
    XanoError,
    XanoSettings,
    api_enabled,
)
from ui import apply_styles, show_page_header


RESOURCE = "profissionais"

apply_styles()
show_page_header(
    "Profissionais",
    "Consulte os profissionais e suas áreas de atuação no consultório.",
    "🩺",
)

feedback = st.session_state.pop("professionals_feedback", None)
if feedback:
    st.success(feedback)

settings = XanoSettings.from_environment()
client = XanoClient(settings)
enabled = api_enabled()

if not settings.professionals_base_url or not settings.professionals_base_url.strip():
    st.warning(
        "A URL da API de Profissionais não está configurada. Defina "
        "XANO_PROFISSIONAIS_BASE_URL no ambiente da aplicação."
    )
    enabled = False
elif not enabled:
    st.info(
        "A integração com o Xano está desabilitada. Defina "
        "XANO_API_ENABLED=true para permitir chamadas à API."
    )

with st.form("create_professional", clear_on_submit=True):
    st.subheader("Cadastrar profissional")
    name = st.text_input("Nome *", key="professional_create_name")
    phone = st.text_input("Telefone *", key="professional_create_phone")
    email = st.text_input("Email", key="professional_create_email")
    specialty = st.text_input(
        "Especialidade",
        help="Campo textual nesta etapa.",
        key="professional_create_specialty",
    )
    create_submitted = st.form_submit_button(
        "Cadastrar profissional",
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
                    "especialidade": specialty or None,
                },
            )
        except XanoError as error:
            st.error(f"Não foi possível cadastrar o profissional: {error}")
        else:
            st.session_state["professionals_feedback"] = (
                "Profissional cadastrado."
            )
            st.rerun()

st.divider()
st.subheader("Profissionais cadastrados")

professionals: list[dict[str, object]] = []
list_succeeded = False
if enabled:
    try:
        professionals = client.list_records(RESOURCE)
    except XanoError as error:
        st.error(f"Não foi possível carregar profissionais do Xano: {error}")
    else:
        list_succeeded = True
        if professionals:
            st.dataframe(professionals, hide_index=True, width="stretch")
        else:
            st.info("Nenhum profissional cadastrado no Xano.")

if list_succeeded and professionals:
    with st.expander("Editar profissional"):
        professional_ids = [
            int(professional["id"]) for professional in professionals
        ]
        selected_id = st.selectbox(
            "Profissional",
            professional_ids,
            format_func=lambda professional_id: next(
                f"{professional['nome']} · ID {professional_id}"
                for professional in professionals
                if professional["id"] == professional_id
            ),
            key="professional_edit_selection",
        )
        if st.button(
            "Carregar profissional",
            key="professional_load",
            disabled=not enabled,
        ):
            try:
                loaded_professional = client.get_record(RESOURCE, selected_id)
            except XanoError as error:
                st.error(f"Não foi possível carregar o profissional: {error}")
            else:
                for field in ("name", "phone", "email", "specialty"):
                    st.session_state.pop(
                        f"professional_edit_{field}_{selected_id}", None
                    )
                st.session_state["professional_edit_record"] = loaded_professional

        professional_to_edit = st.session_state.get("professional_edit_record")
        if professional_to_edit:
            edit_id = int(professional_to_edit["id"])
            with st.form(f"edit_professional_{edit_id}"):
                edit_name = st.text_input(
                    "Nome *",
                    value=str(professional_to_edit["nome"]),
                    key=f"professional_edit_name_{edit_id}",
                )
                edit_phone = st.text_input(
                    "Telefone *",
                    value=str(professional_to_edit.get("telefone") or ""),
                    key=f"professional_edit_phone_{edit_id}",
                )
                edit_email = st.text_input(
                    "Email",
                    value=str(professional_to_edit.get("email") or ""),
                    key=f"professional_edit_email_{edit_id}",
                )
                edit_specialty = st.text_input(
                    "Especialidade",
                    value=str(professional_to_edit.get("especialidade") or ""),
                    key=f"professional_edit_specialty_{edit_id}",
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
                                "especialidade": edit_specialty.strip() or None,
                            },
                        )
                    except XanoError as error:
                        st.error(
                            f"Não foi possível atualizar o profissional: {error}"
                        )
                    else:
                        st.session_state.pop("professional_edit_record", None)
                        st.session_state["professionals_feedback"] = (
                            "Profissional atualizado."
                        )
                        st.rerun()

    st.subheader("Excluir profissional")
    for professional in professionals:
        professional_id = int(professional["id"])
        with st.container(border=True):
            st.write(f"{professional['nome']} · ID {professional_id}")
            confirmed = st.checkbox(
                f"Confirmo a exclusão de {professional['nome']}",
                key=f"professional_delete_confirm_{professional_id}",
                disabled=not enabled,
            )
            if st.button(
                "Excluir profissional",
                key=f"professional_delete_{professional_id}",
                type="secondary",
                disabled=not enabled or not confirmed,
            ):
                try:
                    client.delete_record(RESOURCE, professional_id)
                except XanoError as error:
                    st.error(f"Não foi possível excluir o profissional: {error}")
                else:
                    st.session_state.pop("professional_edit_record", None)
                    st.session_state["professionals_feedback"] = (
                        "Profissional excluído."
                    )
                    st.rerun()
