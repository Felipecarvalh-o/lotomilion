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

defaults = {
    "estrategia": None,
    "jogos": [],
    "classificacao": None,
    "nome_estrategia": None
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ======================================================
# ESTILO GLOBAL
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

/* HERO */
.hero-wrapper {
    position: relative;
    margin-top: 18vh;
    display: flex;
    justify-content: center;
}

.hero {
    position: relative;
    width: 100%;
    max-width: 820px;
    padding: 64px 60px;
    text-align: center;
    border-radius: 36px;
    background: linear-gradient(180deg, #2a0045, #12001f);
    box-shadow:
        0 50px 140px rgba(0,0,0,.9),
        inset 0 0 120px rgba(168,85,247,.25);
    z-index: 2;
}

.hero::before {
    content: "";
    position: absolute;
    inset: -80px;
    background: radial-gradient(circle, rgba(168,85,247,.45), transparent 70%);
    filter: blur(80px);
    z-index: -1;
}

.hero h1 {
    font-size: 44px;
    font-weight: 900;
    margin-bottom: 18px;
}

.hero p {
    font-size: 16px;
    opacity: .9;
}

.badge {
    background:#2A0934;
    padding:10px 16px;
    border-radius:16px;
    font-size:14px;
    margin-bottom:14px;
}

.numero {
    padding:14px;
    border-radius:16px;
    font-size:16px;
    font-weight:700;
    text-align:center;
    color:white;
    background:#6A1B9A;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# TELA INICIAL
# ======================================================

if st.session_state.modo is None:

    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero">
            <h1>🍀 Lotomilion Estrategista</h1>
            <p>
                Inteligência estatística aplicada à Lotofácil.<br>
                Teste gratuitamente no modo demonstração.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns([2,3,1,3,2])

    with c2:
        if st.button("🚀 Entrar no modo Demonstração", use_container_width=True):
            st.session_state.modo = "demo"
            st.rerun()

    with c4:
        if st.button("🔒 Já sou PRO", use_container_width=True):
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
    ["📊 Estratégias Avançadas", "🎯 Gerador Simples", "ℹ️ Sobre"]
)

# ======================================================
# 📊 ESTRATÉGIAS
# ======================================================

if menu == "📊 Estratégias Avançadas":

    st.title("📊 Estratégias Avançadas — Lotofácil")

    if not st.session_state.estrategia:
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

    if st.session_state.estrategia:

        st.markdown(
            f"<div class='badge'>📌 Estratégia ativa: <b>{st.session_state.nome_estrategia}</b></div>",
            unsafe_allow_html=True
        )

        if st.button("🔄 Trocar estratégia"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()

        if st.session_state.estrategia == "fechamento":

            fixas_txt = st.text_area("🔒 9 dezenas FIXAS")
            variaveis_txt = st.text_area("🔄 12 dezenas VARIÁVEIS")

            if st.button("🧠 Gerar Jogos"):
                dezenas = sorted(
                    set(converter_lista(fixas_txt) + converter_lista(variaveis_txt))
                )

                if len(dezenas) != 21:
                    st.error("Use exatamente 21 dezenas.")
                    st.stop()

                st.session_state.jogos = gerar_fechamento_21_8(dezenas)

        else:
            if st.button("🧠 Gerar Jogos"):
                historico = carregar_historico(qtd=50)

                base_fake = list(range(1, 22))
                _, ranking = gerar_jogos_historico_real(base_fake, historico)

                dezenas_base = (
                    ranking["quentes"] +
                    ranking["mornas"] +
                    ranking["frias"]
                )[:21]

                jogos, classificacao = gerar_jogos_historico_real(
                    dezenas_base, historico
                )

                st.session_state.jogos = jogos
                st.session_state.classificacao = classificacao

    if st.session_state.jogos:
        st.subheader("🎲 Jogos Gerados")

        limite = 2 if st.session_state.modo == "demo" else len(st.session_state.jogos)

        for jogo in st.session_state.jogos[:limite]:
            cols = st.columns(5)
            for c, n in zip(cols * 3, jogo):
                c.markdown(f"<div class='numero'>{n:02d}</div>", unsafe_allow_html=True)

        if st.session_state.modo == "demo" and len(st.session_state.jogos) > 2:
            st.warning("🔒 Jogos ilimitados disponíveis no plano PRO")

# ======================================================
# OUTROS
# ======================================================

elif menu == "🎯 Gerador Simples":
    st.title("🎯 Gerador Simples")
    if st.button("Gerar jogo"):
        jogo = sorted(random.sample(range(1, 26), 15))
        st.write(" ".join(f"{n:02d}" for n in jogo))

elif menu == "ℹ️ Sobre":
    st.title("ℹ️ Sobre")
    st.write("Sistema estatístico educacional. Não garante premiação.")
