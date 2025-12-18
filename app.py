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
# ESTILO GLOBAL
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

html, body, [data-testid="stApp"] {
    background: radial-gradient(circle at top, #1B0A2A, var(--bg));
    color: var(--text);
}

/* ================= LOGIN DECOR ================= */

.login-bg {
    position: fixed;
    inset: 0;
    overflow: hidden;
    z-index: -1;
    pointer-events: none;
}

.float {
    position: absolute;
    font-size: 64px;
    opacity: 0.10;
    animation: float 26s linear infinite;
    filter: blur(0.5px);
}

.trevo {
    color: #A855F7;
    text-shadow: 0 0 18px rgba(168,85,247,.6);
}

.n1 { color: #FACC15; }
.n2 { color: #3B82F6; }
.n3 { color: #22C55E; }
.n4 { color: #EC4899; }

@keyframes float {
    from { transform: translateY(120vh) rotate(0deg); }
    to { transform: translateY(-140vh) rotate(360deg); }
}

/* ================= CARD ================= */

.card {
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

.numero {
    background: linear-gradient(145deg, var(--secondary), var(--primary));
    padding: 14px;
    border-radius: 18px;
    font-weight: 800;
    text-align: center;
    position: relative;
}

.acerto {
    outline: 3px solid var(--success);
    box-shadow: 0 0 18px rgba(0,230,118,.7);
}

.trofeu {
    position:absolute;
    top:-6px;
    right:-6px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN PREMIUM (CHAMATIVO)
# ======================================================

if not st.session_state.logado:

    # FUNDO DECORATIVO
    elementos = []
    for _ in range(16):
        left = random.randint(0, 100)
        delay = random.randint(0, 20)
        size = random.choice([40, 50, 60, 72])
        elementos.append(
            f"<div class='float trevo' style='left:{left}%; font-size:{size}px; animation-delay:{delay}s'>🍀</div>"
        )

    numeros = ["07", "13", "21", "25", "18", "10"]
    cores = ["n1", "n2", "n3", "n4"]

    for _ in range(10):
        left = random.randint(0, 100)
        delay = random.randint(0, 25)
        size = random.choice([36, 44, 52])
        num = random.choice(numeros)
        cor = random.choice(cores)
        elementos.append(
            f"<div class='float {cor}' style='left:{left}%; font-size:{size}px; animation-delay:{delay}s'>{num}</div>"
        )

    st.markdown(
        "<div class='login-bg'>" + "".join(elementos) + "</div>",
        unsafe_allow_html=True
    )

    # CARD LOGIN
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
# APP NORMAL (SEM FUNDO DECORATIVO)
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Acesso ativo • {st.session_state.email}")

# (restante do app segue igual à versão anterior)
