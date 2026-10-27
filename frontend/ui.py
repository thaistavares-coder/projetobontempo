import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: #F4F7FA;
                color: #203040;
            }
            main, [data-testid="stSidebar"] {
                color: #203040;
            }
            h1, h2, h3, h4 {
                color: #123B56;
                letter-spacing: -0.025em;
            }
            h1 {
                margin-bottom: 0.25rem;
            }
            p, li, label, [data-testid="stCaptionContainer"] {
                color: #203040;
            }
            .bontempo-eyebrow {
                color: #00777F;
                font-size: 0.78rem;
                font-weight: 750;
                letter-spacing: 0.12em;
                margin-bottom: 0.4rem;
                text-transform: uppercase;
            }
            .bontempo-description {
                color: #435568;
                font-size: 1.02rem;
                line-height: 1.65;
                margin: 0.2rem 0 1.2rem;
                max-width: 820px;
            }
            [data-testid="stWidgetLabel"] p,
            [data-testid="stWidgetLabel"] label,
            [data-testid="stWidgetLabel"] span {
                color: #203040;
                font-weight: 600;
                opacity: 1;
            }
            [data-testid="stTextInputRootElement"],
            [data-testid="stTextAreaRootElement"],
            [data-testid="stDateInputField"],
            [data-testid="stTimeInputTimeDisplay"],
            [data-testid="stSelectbox"] [role="combobox"],
            [data-testid="stMultiSelect"] [role="combobox"] {
                background-color: #FFFFFF;
                border-color: #CBD5E1;
                color: #203040;
            }
            [data-testid="stTextInputRootElement"] input,
            [data-testid="stTextAreaRootElement"] textarea,
            [data-testid="stSelectbox"] input,
            [data-testid="stMultiSelect"] input,
            [data-testid="stDateInput"] input,
            [data-testid="stTimeInput"] input,
            [data-testid="stDateInputField"] [role="spinbutton"],
            [data-testid="stTimeInputTimeDisplay"] [role="spinbutton"] {
                color: #203040;
            }
            [data-testid="stTextInputRootElement"] input::placeholder,
            [data-testid="stTextAreaRootElement"] textarea::placeholder,
            [data-testid="stSelectbox"] input::placeholder,
            [data-testid="stMultiSelect"] input::placeholder,
            [data-testid="stDateInput"] input::placeholder,
            [data-testid="stTimeInput"] input::placeholder {
                color: #526273 !important;
                opacity: 1 !important;
            }
            [data-testid="stTextInputRootElement"]:focus-within,
            [data-testid="stTextAreaRootElement"]:focus-within,
            [data-testid="stDateInputField"]:focus-within,
            [data-testid="stTimeInputTimeDisplay"]:focus-within,
            [data-testid="stSelectbox"] [role="combobox"]:focus-within,
            [data-testid="stMultiSelect"] [role="combobox"]:focus-within {
                border-color: #008C95;
                box-shadow: 0 0 0 1px #008C95;
            }
            [data-baseweb="popover"],
            [data-baseweb="menu"],
            [role="listbox"] {
                background-color: #FFFFFF;
                color: #203040;
            }
            [role="option"] {
                color: #203040;
            }
            [role="option"]:hover,
            [role="option"][aria-selected="true"] {
                background-color: #E6F3F4;
                color: #123B56;
            }
            [data-testid^="stBaseButton-primary"] {
                background-color: #00777F;
                border-color: #00777F;
                color: #FFFFFF;
            }
            [data-testid^="stBaseButton-primary"]:hover {
                background-color: #006D75;
                border-color: #006D75;
                color: #FFFFFF;
            }
            [data-testid^="stBaseButton-secondary"] {
                background-color: #FFFFFF;
                border-color: #CBD5E1;
                color: #123B56;
            }
            [data-testid^="stBaseButton-secondary"]:hover {
                background-color: #EAF0F5;
                border-color: #123B56;
                color: #123B56;
            }
            [data-testid^="stBaseButton-"]:focus-visible,
            [data-testid="stPageLink"] a:focus-visible,
            [data-testid="stSidebar"] a:focus-visible {
                outline: 3px solid #008C95;
                outline-offset: 2px;
            }
            button[data-testid^="stBaseButton-"]:disabled,
            button[data-testid^="stBaseButton-"][disabled] {
                background-color: #E2E8F0 !important;
                border-color: #CBD5E1 !important;
                color: #526273 !important;
                opacity: 1 !important;
            }
            button[data-testid^="stBaseButton-"]:disabled *,
            button[data-testid^="stBaseButton-"][disabled] * {
                color: #526273 !important;
                fill: currentColor;
            }
            [data-testid^="stBaseButton-"] svg {
                fill: currentColor;
                color: inherit;
            }
            [data-testid="stPageLink"] a {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 0.5rem;
                color: #123B56;
                text-decoration: none;
            }
            [data-testid="stPageLink"] a:hover {
                background-color: #EAF0F5;
                border-color: #123B56;
                color: #123B56;
            }
            [data-testid="stSidebar"] {
                background-color: #FFFFFF;
            }
            [data-testid="stSidebar"] a,
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
                color: #203040;
            }
            [data-testid="stSidebar"] a[aria-current="page"] {
                background-color: #E6F3F4;
                color: #123B56;
                font-weight: 650;
            }
            .block-container {
                max-width: 1440px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background-color: #FFFFFF;
                border-color: #CBD5E1;
                border-radius: 16px;
                box-shadow: 0 5px 18px rgba(18, 59, 86, 0.06);
            }
            div[data-testid="stVerticalBlockBorderWrapper"] h3 {
                margin-bottom: 0.35rem;
            }
            div[data-testid="stVerticalBlockBorderWrapper"] p {
                color: #435568;
                line-height: 1.6;
            }
            [data-testid="stExpander"] {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 0.75rem;
                color: #203040;
            }
            [data-testid="stExpander"] summary,
            [data-testid="stExpander"] summary p,
            [data-testid="stExpander"] summary span {
                background-color: #FFFFFF;
                color: #123B56;
                font-weight: 600;
            }
            [data-testid="stExpander"] summary:hover {
                background-color: #EAF0F5;
            }
            [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
                color: #203040;
            }
            [data-testid="stDataFrame"] {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 12px;
                overflow: hidden;
            }
            [data-testid="stAlert"] {
                border-radius: 12px;
                color: #203040;
            }
            [data-testid="stAlert"] p {
                color: #203040;
            }
            @media (max-width: 760px) {
                .block-container {
                    padding: 1.25rem 1rem 2rem;
                }
                .bontempo-description {
                    font-size: 0.95rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_page_header(title: str, description: str, icon: str) -> None:
    st.markdown(
        "<div class='bontempo-eyebrow'>Bontempo · Gestão de Consultório</div>",
        unsafe_allow_html=True,
    )
    st.title(f"{icon} {title}")
    st.markdown(
        f"<div class='bontempo-description'>{description}</div>",
        unsafe_allow_html=True,
    )
