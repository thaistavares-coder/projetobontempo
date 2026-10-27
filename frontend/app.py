import streamlit as st

from services.database import (
    DemoDataRequiresEmptyDatabaseError,
    initialize_database,
    seed_demo_data,
)
from ui import apply_styles


st.set_page_config(
    page_title="Sistema de Gestão de Consultório",
    page_icon=":hospital:",
    layout="wide",
)

apply_styles()


@st.cache_resource
def setup_local_database() -> None:
    initialize_database()


setup_local_database()

st.sidebar.info(
    "Modo demonstração local · SQLite\n\n"
    "Os dados são armazenados neste computador. A integração GET com Xano "
    "não é usada neste modo."
)
if st.sidebar.button("Carregar exemplos fictícios", use_container_width=True):
    try:
        inserted = seed_demo_data()
        st.sidebar.success(f"{inserted} registros de demonstração criados.")
    except DemoDataRequiresEmptyDatabaseError as error:
        st.sidebar.warning(str(error))


def show_home() -> None:
    st.markdown(
        "<div class='bontempo-eyebrow'>Bem-vindo ao</div>",
        unsafe_allow_html=True,
    )
    st.title("🏥 Bontempo")
    st.markdown(
        "<div class='bontempo-description'>Sistema de Gestão de Consultório</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "Uma interface para apoiar a organização do consultório e facilitar o acesso aos seus módulos.",
    )
    st.divider()
    st.subheader("Acesso rápido")

    columns = st.columns(2)
    for column, page, title, description, icon in (
        (
            columns[0],
            patients_page,
            "Pacientes",
            "Acesse o módulo de gestão de pacientes.",
            ":material/groups:",
        ),
        (
            columns[1],
            professionals_page,
            "Profissionais",
            "Acesse o módulo de gestão de profissionais.",
            ":material/medical_services:",
        ),
        (
            columns[0],
            specialties_page,
            "Especialidades",
            "Cadastre especialidades e relacione-as aos profissionais.",
            ":material/medical_information:",
        ),
        (
            columns[1],
            appointments_page,
            "Consultas",
            "Agende consultas e acompanhe seus status.",
            ":material/calendar_month:",
        ),
    ):
        with column:
            with st.container(border=True):
                st.subheader(title)
                st.write(description)
                st.page_link(page, label=f"Abrir {title.lower()}", icon=icon)
    with st.container(border=True):
        st.caption("Ambiente local de demonstração. Nenhuma alteração é enviada ao Xano.")


patients_page = st.Page("pages/1_Pacientes.py", title="Pacientes", icon=":material/groups:")
professionals_page = st.Page(
    "pages/2_Profissionais.py",
    title="Profissionais",
    icon=":material/medical_services:",
)
specialties_page = st.Page(
    "pages/3_Especialidades.py",
    title="Especialidades",
    icon=":material/medical_information:",
)
appointments_page = st.Page(
    "pages/4_Consultas.py",
    title="Consultas",
    icon=":material/calendar_month:",
)
pages = [
    st.Page(show_home, title="Início", icon=":material/home:", default=True),
    patients_page,
    professionals_page,
    specialties_page,
    appointments_page,
]

st.navigation(pages, position="sidebar").run()
