import streamlit as st

from services import database
from ui import apply_styles, show_page_header


apply_styles()
show_page_header(
    "Especialidades",
    "Cadastre especialidades médicas para vinculá-las a um ou mais profissionais.",
    ":material/medical_information:",
)

with st.form("cadastro_especialidade", clear_on_submit=True):
    st.caption("* Campo obrigatório.")
    nome = st.text_input(
        "Especialidade *",
        placeholder="Digite o nome da especialidade",
        label_visibility="visible",
    )
    cadastrar = st.form_submit_button(
        "Cadastrar especialidade",
        type="primary",
        icon=":material/add:",
    )

if cadastrar:
    try:
        database.create_specialty(nome)
        st.success("Especialidade cadastrada.")
        st.rerun()
    except database.ValidationError as error:
        st.error(str(error))
    except database.DuplicateSpecialtyError as error:
        st.warning(str(error))
    except database.DatabaseError as error:
        st.error(f"Não foi possível salvar a especialidade: {error}")

st.divider()
st.subheader("Especialidades cadastradas")
especialidades = database.list_specialties()
if especialidades:
    st.dataframe(especialidades, hide_index=True, use_container_width=True)
else:
    st.info("Nenhuma especialidade cadastrada neste banco SQLite local.")
