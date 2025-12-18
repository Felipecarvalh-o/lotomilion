# ======================================================
# Lotomilion Estrategista — Login Premium (FINAL ABSOLUTO)
# ======================================================

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
# CSS + FUNDO (100% SEGURO)
# ======================================================

st.markdown("""
<style>

/* RESET */
html, body, [data-testid="stApp"] {
    height: 100%;
}

[data-testid="stAppViewContainer"] > .main {
    padding: 0;
}

header, footer {
    display: none;
}

/* FUNDO ANIMADO */
.login-bg {
    position: fixed;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    background:
        radial-gradient(circle at top, rgba(168,85,247,.25), transparent 55%),
        linear-gradient(180deg, #12001B, #050007);
}

.login-bg::before {
    content: "🍀 🍀 🍀 🍀 🍀 🍀 🍀 🍀 🍀 🍀 01 03 05 07 10 13 15 18 21 25";
    position: absolute;
    inset: -200%;
    font-size: 48px;
    opacity: 0.12;
    color: #A855F7;
    animation: subir 40s linear infinite;
    white-space: nowrap;
}

@keyframes subir {
    from { transform: translateY(0); }
    to   { transform: translateY(-50%); }
}

/* WRAPPER */
.login-wrapper {
    height: 100vh;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding-top: 12vh;
    padding-left: 12px;
    padding-right: 12px;
    position: relative;
    z-index: 5;
}

/* CARD */
.login-card {
    width: 100%;
    max-width: 420px;
    padding: 30px 26px;
    border-radius: 28px;
    background: rgba(24,0,38,.68);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(168,85,247,.45);
    box-shadow: 0 0 140px rgba(168,85,247,.85);
    text-align: center;
}

/* TEXTO */
.login-title {
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 6px;
}

.login-sub {
    font-size: 14px;
    opacity: .85;
    margin-bottom: 14px;
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
}

/* CAPTION */
.login-caption {
    margin-top: 12px;
    font-size: 12px;
    opacity: .6;
}

</style>

<div class="login-bg"></div>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logado:

    st.markdown("""
    <div class="login-wrapper">
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
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ======================================================
# APP
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Logado como {st.session_state.email}")
