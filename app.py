# ======================================================
# Lotomilion Estrategista — Login Premium (ESTÁVEL REAL)
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
# FUNDO ESTÁTICO (ISOLADO)
# ======================================================

items = ""

for _ in range(18):
    items += f"""
    <div class="item trevo"
         style="top:{random.randint(5,90)}%;
                left:{random.randint(5,90)}%;
                font-size:{random.choice([22,28,34,40])}px;">
        🍀
    </div>
    """

for _ in range(14):
    items += f"""
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
    {items}
</div>
</body>
</html>
""",
height=0
)

# ======================================================
# CSS STREAMLIT (ANTI-ESPAÇO FANTASMA)
# ======================================================

st.markdown("""
<style>

/* REMOVE ESPAÇOS MALDITOS */
header, footer, [data-testid="stToolbar"] {
    display: none !important;
}

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* CARD */
.login-card {
    max-width: 420px;
    margin: 12vh auto 0 auto;
    padding: 28px;
    border-radius: 26px;
    background: rgba(24,0,38,.78);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(168,85,247,.45);
    box-shadow: 0 0 120px rgba(168,85,247,.9);
    text-align: center;
}

/* INPUT */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,.08);
    border-radius: 10px;
}

/* BOTÃO */
div[data-testid="stButton"] button {
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    border: none;
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logado:

    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown("## 🍀 Lotomilion Estrategista")
    st.caption("Inteligência estatística aplicada à Lotofácil — **Acesso Premium**")

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
        st.session_state.email = email
        st.rerun()

    st.caption("🔒 Sistema estatístico • Não garante premiação")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ======================================================
# APP
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Logado como {st.session_state.email}")
