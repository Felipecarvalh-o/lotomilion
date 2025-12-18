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

if "modo" not in st.session_state:
    st.session_state.modo = None  # demo | pro

defaults = {
    "estrategia": None,
    "jogos": [],
    "classificacao": None,
    "nome_estrategia": None
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ======================================================
# ESTILO GLOBAL (PREMIUM)
# ======================================================

st.markdown("""
<style>
header, footer { display: none; }

[data-testid="stApp"] {
    background: radial-gradient(circle at top, #1a002b, #050007 70%);
}

/* HERO */
.hero {
    max-width: 900px;
    margin: 18vh auto;
    padding: 60px 50px;
    text-align: center;
    border-radius: 32px;
    background: linear-gradient(180deg, rgba(40,0,70,.9), rgba(10,0,20,.95));
    box-shadow:
        0 0 120px rgba(168,85,247,.65),
        inset 0 0 60px rgba(168,85,247,.15);
}

.hero h1 {
    font-size: 42px;
    font-weight: 900;
}

.hero p {
    font-size: 16px;
    opacity: .9;
    margin: 20px 0 34px;
}

.hero-buttons {
    display: flex;
    gap: 18px;
    justify-content: center;
    flex-wrap: wrap;
}

/* BOTÕES ROXOS */
div[data-testid="stButton"] button {
    height: 52px;
    min-width: 260px;
    border-radius: 16px;
    font-size: 16px;
    font-weight: 700;
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    border: none;
    color: white;
}

/* MENU */
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    color: white;
    font-weight: 700;
    border-radius: 10px;
}

/* UI */
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
# TELA INICIAL (CENTRAL PREMIUM)
# ======================================================

if st.session_state.modo is None:
    st.markdown("""
    <div class="hero">
        <h1>🍀 Lotomilion Estrategista</h1>
        <p>
            Inteligência estatística aplicada à Lotofácil<br>
            Teste gratuitamente no modo demonstração.
        </p>
    """, unsafe_allow_html=True)

    st.markdown("<div class='hero-buttons'>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("🚀 Entrar no modo Demonstração"):
            st.session_state.modo = "demo"
            st.rerun()

    with c2:
        if st.button("🔒 Já sou PRO"):
            st.session_state.modo = "pro"
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
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
# 📊 ESTRATÉGIAS AVANÇADAS
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

        # ================= FECHAMENTO 21 =================
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

        # ================= HISTÓRICO REAL (100% SEGURO) =================
        else:
            st.info("📊 Geração automática baseada nos últimos sorteios reais.")

            if st.button("🧠 Gerar Jogos"):
                historico = carregar_historico(qtd=50)

                base_fake = list(range(1, 22))
                _, ranking = gerar_jogos_historico_real(base_fake, historico)

                dezenas_base = (
                    ranking["quentes"]
                    + ranking["mornas"]
                    + ranking["frias"]
                )[:21]

                jogos, classificacao = gerar_jogos_historico_real(
                    dezenas_base, historico
                )

                st.session_state.jogos = jogos
                st.session_state.classificacao = classificacao

    # ================= RESULTADOS =================
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
