import streamlit as st
import random

from data.lotofacil_historico import carregar_historico
from engine import gerar_fechamento_21_8, gerar_jogos_historico_real
from utils import converter_lista

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🍀",
    layout="wide"
)

# ======================================================
# SESSION STATE
# ======================================================

st.session_state.setdefault("modo", None)          # None | demo | pro
st.session_state.setdefault("estrategia", None)
st.session_state.setdefault("jogos", [])
st.session_state.setdefault("resultado_real", [])
st.session_state.setdefault("comparar", False)
st.session_state.setdefault("nome_estrategia", None)

# ======================================================
# ESTILO GLOBAL (INTACTO)
# ======================================================

st.markdown("""
<style>
header, footer { display: none; }

[data-testid="stApp"] {
    background:
        radial-gradient(circle at center, rgba(168,85,247,.22), transparent 55%),
        linear-gradient(180deg, #050007, #0B0B12);
}

div[data-testid="stButton"] button {
    height: 50px;
    border-radius: 16px;
    font-weight: 700;
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    border: none;
    color: white;
    box-shadow: 0 10px 30px rgba(168,85,247,.45);
}

.hero-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 18vh;
}

.hero {
    max-width: 820px;
    padding: 64px 60px;
    text-align: center;
    border-radius: 36px;
    background: linear-gradient(180deg, #2a0045, #12001f);
    box-shadow:
        0 50px 140px rgba(0,0,0,.9),
        inset 0 0 120px rgba(168,85,247,.25);
}

.hero::before {
    content: "";
    position: absolute;
    inset: -80px;
    background: radial-gradient(circle, rgba(168,85,247,.45), transparent 70%);
    filter: blur(90px);
    z-index: -1;
}

.hero h1 { font-size: 44px; font-weight: 900; }
.hero p { font-size: 16px; opacity: .9; }

.badge {
    background:#2A0934;
    padding:10px 16px;
    border-radius:16px;
    font-size:14px;
    margin-bottom:14px;
}

.numero {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    font-size: 16px;
    font-weight: 800;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    background: radial-gradient(circle at top, #A855F7, #6A1B9A);
}

.acerto {
    border:2px solid #00E676;
    box-shadow:0 0 18px rgba(0,230,118,.8);
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# HOME
# ======================================================

if st.session_state.modo is None:
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero">
            <h1>🍀 Lotomilion Estrategista</h1>
            <p>Inteligência estatística aplicada à Lotofácil</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 Modo Demonstração", use_container_width=True):
            st.session_state.modo = "demo"
            st.rerun()
    with c2:
        if st.button("🔒 Sou PRO", use_container_width=True):
            st.session_state.modo = "pro"
            st.rerun()

    st.stop()

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("🍀 Lotomilion")

if st.session_state.modo == "demo":
    st.sidebar.warning("🔓 DEMO — limitado")

if st.sidebar.button("🔒 Sou PRO"):
    st.session_state.modo = "pro"
    st.rerun()

menu = st.sidebar.radio(
    "Menu",
    ["📊 Estratégias Avançadas", "🎯 Gerador Simples"]
)

# ======================================================
# ESTRATÉGIAS
# ======================================================

if menu == "📊 Estratégias Avançadas":

    if st.session_state.estrategia is None:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎯 Fechamento 21", use_container_width=True):
                st.session_state.estrategia = "fechamento"
                st.session_state.nome_estrategia = "Fechamento 21"
                st.rerun()
        with c2:
            if st.button("📊 Histórico Real", use_container_width=True):
                st.session_state.estrategia = "historico"
                st.session_state.nome_estrategia = "Histórico Real"
                st.rerun()

    else:
        st.markdown(
            f"<div class='badge'>📌 {st.session_state.nome_estrategia}</div>",
            unsafe_allow_html=True
        )

        # ================= FECHAMENTO =================
        if st.session_state.estrategia == "fechamento":

            fixas = st.text_area("🔒 9 fixas")
            variaveis = st.text_area("🔄 12 variáveis")

            if st.button("🧠 Gerar Jogos"):
                dezenas = sorted(set(converter_lista(fixas) + converter_lista(variaveis)))
                if len(dezenas) != 21:
                    st.error("Use exatamente 21 dezenas")
                    st.stop()

                jogos = gerar_fechamento_21_8(dezenas)
                jogos = [sorted(j[:15]) for j in jogos][:8]

                st.session_state.jogos = jogos

        # ================= HISTÓRICO =================
        if st.session_state.estrategia == "historico":

            if st.button("🧠 Gerar Jogo"):
                historico = carregar_historico(qtd=50)

                base = list(range(1, 22))
                jogos, _ = gerar_jogos_historico_real(base, historico)

                st.session_state.jogos = [sorted(jogos[0][:15])]

    # ================= EXIBIÇÃO =================
    if st.session_state.jogos:

        limite = 2 if st.session_state.modo == "demo" else len(st.session_state.jogos)

        for jogo in st.session_state.jogos[:limite]:
            for i in range(0, 15, 5):
                cols = st.columns(5)
                for c, n in zip(cols, jogo[i:i+5]):
                    c.markdown(f"<div class='numero'>{n:02d}</div>", unsafe_allow_html=True)

        if st.session_state.modo == "demo" and len(st.session_state.jogos) > 2:
            st.warning("🔒 Jogos completos apenas no PRO")

# ======================================================
# GERADOR SIMPLES
# ======================================================

elif menu == "🎯 Gerador Simples":
    if st.button("Gerar jogo"):
        jogo = sorted(random.sample(range(1, 26), 15))
        for i in range(0, 15, 5):
            cols = st.columns(5)
            for c, n in zip(cols, jogo[i:i+5]):
                c.markdown(f"<div class='numero'>{n:02d}</div>", unsafe_allow_html=True)
