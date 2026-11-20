import streamlit as st

from services.validation import validate_contact
from services.xano import (
    XanoClient,
    XanoError,
    XanoSettings,
    api_enabled,
    professional_specialties_api_enabled,
    professional_specialties_write_enabled,
    professionals_write_enabled,
    specialties_api_enabled,
)
from services.xano_cache import clear_xano_read_caches
from ui import apply_styles, render_clean_table, show_page_header


RESOURCE = "profissionais"


def _professional_specialty_label(
    professional_id: int,
    legacy_specialty: object,
    associations_by_professional: dict[int, list[dict[str, int]]],
    specialty_names: dict[int, str],
) -> str:
    linked_specialty_ids = {
        int(association["especialidade_id"])
        for association in associations_by_professional.get(professional_id, [])
        if int(association["especialidade_id"]) in specialty_names
    }
    linked_names = [
        specialty_names[specialty_id]
        for specialty_id in sorted(linked_specialty_ids)
    ]
    if linked_names:
        return ", ".join(linked_names)
    if legacy_specialty is not None:
        legacy_text = str(legacy_specialty).strip()
        if legacy_text:
            return legacy_text
    return ""


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
write_enabled = enabled and professionals_write_enabled()
relations_enabled = professional_specialties_api_enabled()
relations_write_enabled = (
    relations_enabled and professional_specialties_write_enabled()
)

specialties: list[dict[str, object]] = []
specialty_names: dict[int, str] = {}
associations: list[dict[str, int]] = []
associations_by_professional: dict[int, list[dict[str, int]]] = {}

if specialties_api_enabled():
    try:
        specialties = client.list_specialties()
    except XanoError as error:
        st.error(f"Não foi possível carregar as especialidades: {error}")
    else:
        specialty_names = {
            int(specialty["id"]): str(specialty["nome"])
            for specialty in specialties
        }

if relations_enabled:
    try:
        associations = client.list_professional_specialties()
    except XanoError as error:
        st.error(f"Não foi possível carregar o catálogo de vínculos: {error}")
    else:
        for association in associations:
            professional_id = int(association["profissional_id"])
            associations_by_professional.setdefault(professional_id, []).append(
                association
            )

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

if "show_create_professional_form" not in st.session_state:
    st.session_state["show_create_professional_form"] = False

if not st.session_state["show_create_professional_form"]:
    col_btn, _ = st.columns([1.4, 4.6])
    with col_btn:
        if st.button(
            "Novo profissional",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["show_create_professional_form"] = True
            st.rerun()
else:
    _, col_close = st.columns([5, 1])
    with col_close:
        if st.button(
            "Fechar",
            key="close_create_professional",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state["show_create_professional_form"] = False
            st.rerun()

    with st.form("create_professional", clear_on_submit=True):
        st.subheader("Cadastrar profissional")
        name = st.text_input("Nome *", key="professional_create_name")
        phone = st.text_input("Telefone *", key="professional_create_phone")
        email = st.text_input("Email", key="professional_create_email")
        specialty_ids_to_link = st.multiselect(
            "Especialidade",
            options=list(specialty_names),
            format_func=lambda specialty_id: (
                f"{specialty_names[specialty_id]} · ID {specialty_id}"
            ),
            key="professional_create_specialty_ids",
            disabled=not relations_write_enabled or not specialty_names,
            help=(
                "Selecione especialidades cadastradas no Xano."
                if relations_write_enabled
                else "Habilite XANO_PROFISSIONAL_ESPECIALIDADES_WRITE_ENABLED=true no .env."
            ),
        )
        create_submitted = st.form_submit_button(
            "Cadastrar profissional",
            type="primary",
            disabled=not write_enabled,
        )

    if create_submitted:
        validation_error = validate_contact(name, phone, email)
        if validation_error:
            st.error(validation_error)
        else:
            try:
                created_professional = client.create_record(
                    RESOURCE,
                    {
                        "nome": name,
                        "telefone": phone,
                        "email": email or None,
                    },
                )
            except XanoError as error:
                st.error(f"Não foi possível cadastrar o profissional: {error}")
            else:
                professional_id = int(created_professional["id"])
                relation_errors: list[XanoError] = []
                for specialty_id in specialty_ids_to_link:
                    try:
                        client.create_professional_specialty(
                            professional_id,
                            int(specialty_id),
                        )
                    except XanoError as error:
                        relation_errors.append(error)
                if relation_errors:
                    clear_xano_read_caches()
                    st.error(
                        "Profissional cadastrado, mas não foi possível vincular "
                        f"{len(relation_errors)} especialidade(s)."
                    )
                else:
                    clear_xano_read_caches()
                    st.session_state["show_create_professional_form"] = False
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
            professional_rows = []
            for professional in professionals:
                professional_id = int(professional["id"])
                row = dict(professional)
                row["especialidade"] = _professional_specialty_label(
                    professional_id,
                    professional.get("especialidade"),
                    associations_by_professional,
                    specialty_names,
                )
                professional_rows.append(row)
            render_clean_table(
                professional_rows,
                headers={
                    "id": "ID",
                    "nome": "Nome",
                    "telefone": "Telefone",
                    "email": "Email",
                    "especialidade": "Especialidade",
                },
            )
        else:
            st.info("Nenhum profissional cadastrado no Xano.")

if list_succeeded and professionals:
    professional_ids = [
        int(professional["id"]) for professional in professionals
    ]
    professional_labels = {
        int(professional["id"]): f"{professional['nome']} · ID {int(professional['id'])}"
        for professional in professionals
    }

    with st.expander("Editar profissional"):
        selected_id = st.selectbox(
            "Profissional",
            professional_ids,
            format_func=lambda professional_id: professional_labels[professional_id],
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
            current_specialty_ids = {
                int(association["especialidade_id"])
                for association in associations_by_professional.get(edit_id, [])
                if int(association["especialidade_id"]) in specialty_names
            }
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
                edit_specialty_ids = st.multiselect(
                    "Especialidade",
                    options=list(specialty_names),
                    default=[
                        specialty_id
                        for specialty_id in current_specialty_ids
                    ],
                    format_func=lambda specialty_id: (
                        f"{specialty_names[specialty_id]} · ID {specialty_id}"
                    ),
                    key=f"professional_edit_specialty_ids_{edit_id}",
                    disabled=not relations_write_enabled or not specialty_names,
                    help=(
                        "Os vínculos serão persistidos pelos IDs selecionados."
                        if relations_write_enabled
                        else "Habilite a escrita de vínculos para alterá-los."
                    ),
                )
                update_submitted = st.form_submit_button(
                    "Salvar alterações",
                    disabled=not write_enabled,
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
                        st.error(
                            f"Não foi possível atualizar o profissional: {error}"
                        )
                    else:
                        relation_errors: list[XanoError] = []
                        if relations_write_enabled:
                            selected_specialty_ids = {
                                int(specialty_id)
                                for specialty_id in edit_specialty_ids
                            }
                            for specialty_id in (
                                selected_specialty_ids - current_specialty_ids
                            ):
                                try:
                                    client.create_professional_specialty(
                                        edit_id,
                                        specialty_id,
                                    )
                                except XanoError as error:
                                    relation_errors.append(error)
                            for association in associations_by_professional.get(
                                edit_id,
                                [],
                            ):
                                specialty_id = int(
                                    association["especialidade_id"]
                                )
                                if specialty_id not in selected_specialty_ids:
                                    try:
                                        client.delete_professional_specialty(
                                            int(association["id"])
                                        )
                                    except XanoError as error:
                                        relation_errors.append(error)
                        if relation_errors:
                            clear_xano_read_caches()
                            st.error(
                                "Profissional atualizado, mas não foi possível "
                                f"alterar {len(relation_errors)} vínculo(s)."
                            )
                        else:
                            clear_xano_read_caches()
                            st.session_state.pop("professional_edit_record", None)
                            st.session_state["professionals_feedback"] = (
                                "Profissional atualizado."
                            )
                        st.rerun()

    st.subheader("Excluir profissional")
    with st.container(border=True):
        delete_id = st.selectbox(
            "Selecione o profissional para excluir",
            professional_ids,
            format_func=lambda professional_id: professional_labels[professional_id],
            key="professional_delete_selection",
        )
        selected_professional = next(
            p for p in professionals if int(p["id"]) == delete_id
        )
        confirmed = st.checkbox(
            f"Confirmo a exclusão de {selected_professional['nome']}",
            key=f"professional_delete_confirm_{delete_id}",
            disabled=not write_enabled,
        )
        if st.button(
            "Excluir profissional",
            key=f"professional_delete_{delete_id}",
            type="secondary",
            disabled=not write_enabled or not confirmed,
        ):
            try:
                client.delete_record(RESOURCE, delete_id)
            except XanoError as error:
                st.error(f"Não foi possível excluir o profissional: {error}")
            else:
                st.session_state.pop("professional_edit_record", None)
                st.session_state["professionals_feedback"] = (
                    "Profissional excluído."
                )
                st.rerun()

st.divider()
st.subheader("Especialidades dos profissionais")

if not specialties_api_enabled():
    st.warning("A leitura do catálogo de Especialidades está desabilitada.")
elif not relations_enabled:
    st.warning(
        "XANO_PROFISSIONAL_ESPECIALIDADES_API_ENABLED=true não está habilitado."
    )
elif not settings.professional_specialties_base_url:
    st.error(
        "A URL da API de vínculos Profissional–Especialidade não está configurada."
    )
elif not professionals:
    st.info("Cadastre um profissional para gerenciar seus vínculos.")
else:
    selected_professional_id = st.selectbox(
        "Profissional",
        [int(professional["id"]) for professional in professionals],
        format_func=lambda professional_id: next(
            f"{professional['nome']} · ID {professional_id}"
            for professional in professionals
            if int(professional["id"]) == professional_id
        ),
        key="professional_specialty_selection",
    )
    current_associations = associations_by_professional.get(
        selected_professional_id, []
    )

    st.write("Especialidades vinculadas")
    if current_associations:
        for association in current_associations:
            specialty_id = int(association["especialidade_id"])
            if specialty_id not in specialty_names:
                continue
            with st.container(border=True):
                st.write(specialty_names[specialty_id])
                confirmed = st.checkbox(
                    f"Confirmo a remoção de {specialty_names[specialty_id]}",
                    key=(
                        "professional_specialty_delete_confirm_"
                        f"{association['id']}"
                    ),
                    disabled=not relations_write_enabled,
                )
                if st.button(
                    "Remover vínculo",
                    key=f"professional_specialty_delete_{association['id']}",
                    disabled=not relations_write_enabled or not confirmed,
                ):
                    try:
                        client.delete_professional_specialty(
                            int(association["id"])
                        )
                    except XanoError as error:
                        st.error(f"Não foi possível remover o vínculo: {error}")
                    else:
                        clear_xano_read_caches()
                        st.session_state["professionals_feedback"] = (
                            "Vínculo removido."
                        )
                        st.rerun()
    else:
        st.info("Nenhuma especialidade vinculada.")

    linked_specialty_ids = {
        int(association["especialidade_id"])
        for association in current_associations
    }
    available_specialties = [
        specialty
        for specialty in specialties
        if int(specialty["id"]) not in linked_specialty_ids
    ]
    if available_specialties:
        specialty_id_to_add = st.selectbox(
            "Especialidade para vincular",
            [int(specialty["id"]) for specialty in available_specialties],
            format_func=lambda specialty_id: specialty_names[specialty_id],
            key="professional_specialty_create_selection",
        )
        if st.button(
            "Adicionar vínculo",
            disabled=not relations_write_enabled,
            key="professional_specialty_create",
        ):
            pair_exists = any(
                int(association["profissional_id"]) == selected_professional_id
                and int(association["especialidade_id"]) == specialty_id_to_add
                for association in associations
            )
            if pair_exists:
                st.error("O vínculo já está cadastrado.")
            else:
                try:
                    client.create_professional_specialty(
                        selected_professional_id,
                        specialty_id_to_add,
                    )
                except XanoError as error:
                    st.error(f"Não foi possível criar o vínculo: {error}")
                else:
                    clear_xano_read_caches()
                    st.session_state["professionals_feedback"] = (
                        "Vínculo criado."
                    )
                    st.rerun()
    else:
        st.info("Não há nova especialidade disponível para vincular.")