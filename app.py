import streamlit as st
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
# ESTILO GLOBAL
# ======================================================

st.markdown("""
<style>

/* RESET */
header, footer {
    display: none;
}

/* FUNDO */
[data-testid="stApp"] {
    background: linear-gradient(180deg, #0B0B12, #050007);
}

/* CARD CENTRAL */
.login-card {
    max-width: 460px;
    margin: 12vh auto;
    padding: 36px 32px;
    border-radius: 26px;
    background: linear-gradient(180deg, #1A002B, #0E0018);
    border: 1px solid rgba(168,85,247,.45);
    box-shadow: 0 0 120px rgba(168,85,247,.6);
    text-align: center;
}

/* TÍTULO */
.login-title {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 6px;
}

.login-sub {
    font-size: 14px;
    opacity: .85;
    margin-bottom: 26px;
}

/* INPUT */
div[data-testid="stTextInput"] input {
    height: 48px;
    border-radius: 12px;
    background: rgba(255,255,255,.08);
}

/* BOTÃO */
div[data-testid="stButton"] button {
    height: 50px;
    border-radius: 14px;
    font-weight: 700;
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    border: none;
}

/* CAPTION */
.login-caption {
    margin-top: 16px;
    font-size: 12px;
    opacity: .6;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logado:

    st.markdown("""
    <div class="login-card">
        <div class="login-title">🍀 Lotomilion Estrategista</div>
        <div class="login-sub">
            Inteligência estatística aplicada à Lotofácil<br>
            <b>Acesso Premium</b>
        </div>
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
        st.session_state.email = email
        st.rerun()

    st.markdown("""
        <div class="login-caption">
            🔒 Sistema estatístico • Não garante premiação
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ======================================================
# APP PRINCIPAL
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Logado como {st.session_state.email}")
