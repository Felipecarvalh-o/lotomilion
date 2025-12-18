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
# ESTILO
# ======================================================

st.markdown("""
<style>
header, footer { display: none; }

[data-testid="stApp"] {
    background: linear-gradient(180deg, #0B0B12, #050007);
}

/* BOTÕES ROXOS */
div[data-testid="stButton"] button {
    height: 48px;
    border-radius: 14px;
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
# TELA INICIAL (SEM LOGIN)
# ======================================================

if st.session_state.modo is None:
    st.title("🍀 Lotomilion Estrategista")

    st.markdown("""
    **Inteligência estatística aplicada à Lotofácil**  
    Teste gratuitamente no modo demonstração.
    """)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("🚀 Entrar no modo Demonstração", use_container_width=True):
            st.session_state.modo = "demo"
            st.rerun()

    with c2:
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

        # ================= HISTÓRICO REAL (CORRIGIDO) =================
        else:
            st.info("📊 Geração automática baseada nos últimos sorteios reais.")

            if st.button("🧠 Gerar Jogos"):
                historico = carregar_historico(qtd=50)

                # 1️⃣ gera ranking histórico usando qualquer base válida
                base_fake = list(range(1, 22))
                _, ranking = gerar_jogos_historico_real(base_fake, historico)

                # 2️⃣ monta as 21 melhores dezenas reais
                dezenas_base = (
                    ranking["quentes"]
                    + ranking["mornas"]
                    + ranking["frias"]
                )[:21]

                # 3️⃣ agora sim gera os jogos corretamente
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
