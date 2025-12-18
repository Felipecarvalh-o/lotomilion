# ======================================================
# Lotomilion Estrategista — Login Premium (ESTÁTICO FINAL)
# ======================================================

import streamlit as st
import random
from auth import verificar_usuario

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🍀",
    layout="centered"
)

# ======================================================
# SESSION
# ======================================================

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.email = None

# ======================================================
# BACKGROUND ESTÁTICO (SEGURO)
# ======================================================

elementos = ""

# Trevos
for _ in range(18):
    elementos += f"""
    <div class="bg-item trevo"
         style="
            top:{random.randint(2,95)}%;
            left:{random.randint(2,95)}%;
            font-size:{random.choice([22,28,34,40])}px;">
        🍀
    </div>
    """

# Números
for _ in range(16):
    elementos += f"""
    <div class="bg-item numero"
         style="
            top:{random.randint(2,95)}%;
            left:{random.randint(2,95)}%;
            font-size:{random.choice([18,22,26,30])}px;">
        {random.choice(['01','03','05','07','10','13','15','18','21','25'])}
    </div>
    """

st.markdown(
f"""
<style>

/* RESET STREAMLIT */
html, body, [data-testid="stApp"] {{
    height: 100%;
}}

[data-testid="stAppViewContainer"] > .main {{
    padding: 0;
}}

header, footer {{
    display: none;
}}

/* FUNDO */
.bg {{
    position: fixed;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    background:
        radial-gradient(circle at top, rgba(168,85,247,.35), transparent 55%),
        linear-gradient(180deg, #12001B, #050007);
}}

/* ELEMENTOS */
.bg-item {{
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

/* LOGIN */
.login-wrapper {{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 5;
    padding: 16px;
}}

.login-card {{
    width: 100%;
    max-width: 420px;
    padding: 28px;
    border-radius: 26px;
    background: rgba(24,0,38,.78);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(168,85,247,.45);
    box-shadow: 0 0 120px rgba(168,85,247,.9);
    text-align: center;
}}

.login-title {{
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 6px;
}}

.login-sub {{
    font-size: 14px;
    opacity: .85;
    margin-bottom: 16px;
}}

div[data-testid="stTextInput"] input {{
    background: rgba(255,255,255,.08);
    border-radius: 10px;
}}

div[data-testid="stButton"] button {{
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    border: none;
    border-radius: 12px;
    font-weight: bold;
}}

.login-caption {{
    margin-top: 14px;
    font-size: 12px;
    opacity: .6;
}}

</style>

<div class="bg">
    {elementos}
</div>
""",
unsafe_allow_html=True
)

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logado:

    st.markdown(
    """
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-title">🍀 Lotomilion Estrategista</div>
            <div class="login-sub">
                Inteligência estatística aplicada à Lotofácil<br>
                <b>Acesso Premium</b>
            </div>
    """,
    unsafe_allow_html=True
    )

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

    st.markdown(
    """
            <div class="login-caption">
                🔒 Sistema estatístico • Não garante premiação
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
    )

    st.stop()

# ======================================================
# APP PRINCIPAL
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Logado como {st.session_state.email}")
