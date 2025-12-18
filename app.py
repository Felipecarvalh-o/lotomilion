# ======================================================
# Lotomilion Estrategista — Login Premium (DEFINITIVO)
# ======================================================

import streamlit as st
import random
import streamlit.components.v1 as components
from auth import verificar_usuario

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🍀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ======================================================
# SESSION
# ======================================================

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.email = None

# ======================================================
# FUNDO ESTÁTICO
# ======================================================

bg_items = ""

for _ in range(20):
    bg_items += f"""
    <div class="item trevo"
         style="top:{random.randint(5,90)}%;
                left:{random.randint(5,90)}%;
                font-size:{random.choice([22,28,34,40])}px;">
        🍀
    </div>
    """

for _ in range(16):
    bg_items += f"""
    <div class="item numero"
         style="top:{random.randint(5,90)}%;
                left:{random.randint(5,90)}%;
                font-size:{random.choice([18,22,26,30])}px;">
        {random.choice(['01','03','05','07','10','13','15','18','21','25'])}
    </div>
    """

components.html(
f"""
<html>
<head>
<style>
html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
}}

.bg {{
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at top, rgba(168,85,247,.35), transparent 55%),
        linear-gradient(180deg, #12001B, #050007);
}}

.item {{
    position: absolute;
    opacity: 0.18;
    pointer-events: none;
}}

.trevo {{
    color: #A855F7;
    text-shadow: 0 0 22px rgba(168,85,247,.85);
}}

.numero {{
    color: #22C55E;
    font-weight: 700;
    text-shadow: 0 0 16px rgba(34,197,94,.6);
}}
</style>
</head>

<body>
<div class="bg">
    {bg_items}
</div>
</body>
</html>
""",
height=0
)

# ======================================================
# CSS STREAMLIT (LIMPEZA TOTAL)
# ======================================================

st.markdown("""
<style>
header, footer, [data-testid="stToolbar"] {
    display: none !important;
}

.block-container {
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN (CARD FIXO)
# ======================================================

if not st.session_state.logado:

    st.markdown("""
    <style>
    .login-card {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 90%;
        max-width: 440px;
        padding: 30px;
        border-radius: 26px;
        background: rgba(24,0,38,.78);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(168,85,247,.45);
        box-shadow: 0 0 120px rgba(168,85,247,.9);
        text-align: center;
        z-index: 10;
    }

    div[data-testid="stTextInput"] input {
        background: rgba(255,255,255,.08);
        border-radius: 10px;
    }

    div[data-testid="stButton"] button {
        background: linear-gradient(90deg,#7C3AED,#A855F7);
        border: none;
        border-radius: 12px;
        font-weight: bold;
    }
    </style>

    <div class="login-card">
        <h2>🍀 Lotomilion Estrategista</h2>
        <p style="opacity:.85">
            Inteligência estatística aplicada à Lotofácil<br>
            <b>Acesso Premium</b>
        </p>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "",
        placeholder="seu@email.com",
        label_visibility="collapsed"
    )

    if st.button("Entrar no Painel Premium", use_container_width=True):
        ok, msg = verificar_usuario(email)
        if not ok:
            st.error(msg)
            st.stop()

        st.session_state.logado = True
        st.session_state.email_
