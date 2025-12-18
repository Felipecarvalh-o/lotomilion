# ======================================================
# Lotomilion Estrategista — App Premium
# ======================================================

from data.lotofacil_historico import carregar_historico
from engine import gerar_fechamento_21_8, gerar_historico_21_automatico
from simulador import simular_cenario
from utils import converter_lista
from auth import verificar_usuario

import streamlit as st
import random

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🍀",
    layout="centered"
)

# ======================================================
# SESSION STATE AUTH
# ======================================================

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.email = None

# ======================================================
# ESTILO GLOBAL (STREAMLIT SAFE)
# ======================================================

st.markdown("""
<style>
:root {
    --bg: #050007;
    --primary: #A855F7;
    --secondary: #7C3AED;
    --text: #EDE9FE;
    --muted: #C4B5FD;
    --border: #2E1065;
    --success: #00E676;
}

/* Streamlit root */
[data-testid="stApp"] {
    background: radial-gradient(circle at top, #1B0A2A, var(--bg));
    color: var(--text);
}

/* ================= FUNDO DECORATIVO ================= */

.login-bg {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}

.float {
    position: absolute;
    bottom: -120px;
    opacity: 0.12;
    animation: float 30s linear infinite;
    filter: blur(0.6px);
    user-select: none;
}

.trevo {
    color: #A855F7;
    text-shadow: 0 0 22px rgba(168,85,247,.7);
}

.n1 { color: #FACC15; }
.n2 { color: #3B82F6; }
.n3 { color: #22C55E; }
.n4 { color: #EC4899; }

@keyframes float {
    from { transform: translateY(0) rotate(0deg); }
    to { transform: translateY(-140vh) rotate(360deg); }
}

/* ================= CARD ================= */

.card {
    position: relative;
    z-index: 2;
    background: linear-gradient(160deg, #14001F, #1F0030);
    border-radius: 26px;
    padding: 30px;
    border: 1px solid var(--border);
    box-shadow: 0 0 60px rgba(168,85,247,.35);
    margin-bottom: 24px;
}

.card-title {
    font-size: 24px;
    font-weight: 900;
}

.card-sub {
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN PREMIUM — FUNDO VISÍVEL
# ======================================================

if not st.session_state.logado:

    elementos = []

    # Trevos roxos
    for _ in range(14):
        left = random.randint(0, 100)
        delay = random.randint(0, 25)
        size = random.choice([42, 54, 66, 78])
        elementos.append(
            f"""
            <div class="float trevo"
                 style="left:{left}%;
                        font-size:{size}px;
                        animation-delay:{delay}s;">
                🍀
            </div>
            """
        )

    # Números coloridos
    numeros = ["07", "10", "13", "18", "21", "25"]
    cores = ["n1", "n2", "n3", "n4"]

    for _ in range(10):
        left = random.randint(0, 100)
        delay = random.randint(0, 30)
        size = random.choice([36, 44, 52])
        num = random.choice(numeros)
        cor = random.choice(cores)
        elementos.append(
            f"""
            <div class="float {cor}"
                 style="left:{left}%;
                        font-size:{size}px;
                        animation-delay:{delay}s;">
                {num}
            </div>
            """
        )

    st.markdown(
        f"<div class='login-bg'>{''.join(elementos)}</div>",
        unsafe_allow_html=True
    )

    # Card de login
    st.markdown("""
    <div class="card" style="max-width:420px;margin:12vh auto;text-align:center">
        <div class="card-title">🍀 Lotomilion Estrategista</div>
        <div class="card-sub">
            Inteligência estatística aplicada à Lotofácil<br>
            <b>Acesso Premium</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "Email",
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
    st.stop()

# ======================================================
# APP NORMAL (SEM FUNDO)
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Acesso ativo • {st.session_state.email}")
