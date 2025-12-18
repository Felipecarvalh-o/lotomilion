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

st.session_state.setdefault("modo", None)

st.session_state.setdefault("estrategia", None)
st.session_state.setdefault("jogos", [])
st.session_state.setdefault("classificacao", None)
st.session_state.setdefault("nome_estrategia", None)

# ======================================================
# ESTILO
# ======================================================

st.markdown("""
<style>
header, footer { display: none; }

[data-testid="stApp"] {
    background:
        radial-gradient(circle at center, rgba(168,85,247,.18), transparent 55%),
        linear-gradient(180deg, #050007, #0B0B12);
}

/* BOTÕES */
div[data-testid="stButton"] button {
    height: 50px;
    border-radius: 16px;
    font-weight: 700;
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    border: none;
    color: white;
    box-shadow: 0 10px 30px rgba(168,85,247,.45);
}

/* NUMEROS */
.numero {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    font-size: 16px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    background: radial-gradient(circle at top, #A855F7, #6A1B9A);
    box-shadow:
        inset 0 0 12px rgba(255,255,255,.15),
        0 8px 20px rgba(168,85,247,.45);
}

.badge {
    background:#2A0934;
    padding:10px 16px;
    border-radius:16px;
    font-size:14px;
    margin-bottom:14px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# TELA INICIAL
# ======================================================

if st.session_state.modo is None:
    st.title("🍀 Lotomilion Estrategista")
    st.write("Inteligência estatística aplicada à Lotofácil")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 Modo Demonstração", use_container_width=True):
            st.session_state.modo = "demo"
            st.rerun()
    with c2:
        if st.button("🔒 Modo PRO", use_container_width=True):
            st.session_state.modo = "pro"
            st.rerun()

    st.stop()

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("🍀 Lotomilion")

if st.session_state.modo == "demo":
    st.sidebar.warning("🔓 Modo Demonstração")

menu = st.sidebar.radio(
    "Menu",
    ["📊 Estratégias Avançadas", "🎯 Gerador Simples"]
)

# ======================================================
# 📊 ESTRATÉGIAS
# ======================================================

if menu == "📊 Estratégias Avançadas":

    st.title("📊 Estratégias Avançadas — Lotofácil")

    # ============================
    # ESCOLHA DA ESTRATÉGIA
    # ============================
    if st.session_state.estrategia is None:
        st.subheader("🎯 Escolha a estratégia")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎯 Fechamento 21", use_container_width=True):
                st.session_state.estrategia = "fechamento"
                st.session_state.nome_estrategia = "Fechamento 21"
                st.session_state.jogos = []
                st.rerun()

        with c2:
            if st.button("📊 Histórico Real", use_container_width=True):
                st.session_state.estrategia = "historico"
                st.session_state.nome_estrategia = "Histórico Real"
                st.session_state.jogos = []
                st.rerun()

    # ============================
    # ESTRATÉGIA ATIVA
    # ============================
    else:
        st.markdown(
            f"<div class='badge'>📌 Estratégia ativa: <b>{st.session_state.nome_estrategia}</b></div>",
            unsafe_allow_html=True
        )

        if st.button("🔄 Trocar estratégia"):
            st.session_state.estrategia = None
            st.session_state.jogos = []
            st.session_state.classificacao = None
            st.rerun()

        # ---------- FECHAMENTO ----------
        if st.session_state.estrategia == "fechamento":

            fixas = st.text_area("🔒 9 dezenas fixas")
            variaveis = st.text_area("🔄 12 dezenas variáveis")

            if st.button("🧠 Gerar Jogos"):
                dezenas = sorted(
                    set(converter_lista(fixas) + converter_lista(variaveis))
                )

                if len(dezenas) != 21:
                    st.error("Use exatamente 21 dezenas.")
                    st.stop()

                jogos = gerar_fechamento_21_8(dezenas)

                st.session_state.jogos = [
                    sorted(jogo[:15]) for jogo in jogos
                ]

        # ---------- HISTÓRICO ----------
        if st.session_state.estrategia == "historico":

            if st.button("🧠 Gerar Jogos"):
                historico = carregar_historico(qtd=50)

                base_fake = list(range(1, 22))
                _, ranking = gerar_jogos_historico_real(base_fake, historico)

                dezenas_base = (
                    ranking["quentes"] +
                    ranking["mornas"] +
                    ranking["frias"]
                )[:21]

                jogos, _ = gerar_jogos_historico_real(dezenas_base, historico)

                st.session_state.jogos = [
                    sorted(jogo[:15]) for jogo in jogos
                ]

    # ============================
    # EXIBIÇÃO DOS JOGOS
    # ============================
    if st.session_state.jogos:
        st.subheader("🎲 Jogos Sugeridos (15 dezenas)")

        limite = 2 if st.session_state.modo == "demo" else len(st.session_state.jogos)

        for jogo in st.session_state.jogos[:limite]:
            for i in range(0, 15, 5):
                cols = st.columns(5)
                for c, n in zip(cols, jogo[i:i+5]):
                    c.markdown(
                        f"<div class='numero'>{n:02d}</div>",
                        unsafe_allow_html=True
                    )

        if st.session_state.modo == "demo" and len(st.session_state.jogos) > 2:
            st.warning("🔒 Jogos ilimitados disponíveis no plano PRO")

# ======================================================
# GERADOR SIMPLES
# ======================================================

elif menu == "🎯 Gerador Simples":
    st.title("🎯 Gerador Simples")

    if st.button("Gerar jogo"):
        jogo = sorted(random.sample(range(1, 26), 15))
        for i in range(0, 15, 5):
            cols = st.columns(5)
            for c, n in zip(cols, jogo[i:i+5]):
                c.markdown(f"<div class='numero'>{n:02d}</div>", unsafe_allow_html=True)
