import streamlit as st

def apply_design_system():
    """Aplica o Design System Institucional da Mercury AI."""
    st.markdown("""
        <style>
        /* Cores Institucionais */
        :root {
            --mercury-primary: #003366;
            --mercury-bg: #f4f6f9;
            --mercury-card-bg: #ffffff;
        }
        .stMetric {
            background-color: var(--mercury-card-bg);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background-color: var(--mercury-primary);
            color: white;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

def display_metric(label, value):
    """Componente de métrica institucional."""
    st.metric(label, value)

def display_status(label, status):
    """Componente de status institucional."""
    color = "green" if status == "OK" or status == "ACTIVE" else ("orange" if status == "WARNING" else "red")
    st.write(f"**{label}:** :{color}[{status}]")

def display_card(title, content):
    """Componente de card reutilizável."""
    with st.container(border=True):
        st.subheader(title)
        st.write(content)
