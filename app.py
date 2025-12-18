import streamlit as st
import random

from auth import verificar_usuario
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
# SESSION STATE (LOGIN)
# ======================================================

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.email = None

# ======================================================
# SESSION STATE (ESTRATÉGIAS)
# ======================================================

defaults = {
    "estrategia": None,
    "jogos": None,
    "classificacao": None,
    "resultado_real": None,
    "comparacao_ativa": False,
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
    background: linear-gradient(180deg, #0B0B12, #050007);
}

/* LOGIN */
.login-card {
    max-width: 460px;
    margin: 12vh auto;
    padding: 36px;
    border-radius: 26px;
    background: linear-gradient(180deg, #1A002B, #0E0018);
    border: 1px solid rgba(168,85,247,.45);
    box-shadow: 0 0 120px rgba(168,85,247,.6);
    text-align: center;
}

/* BOTÃO ROXO (LOGIN + APP) */
div[data-testid="stButton"] button {
    height: 50px;
    border-radius: 14px;
    font-weight: 700;
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    border: none;
    color: white;
}

/* MENU ROXO */
section[data-testid="stSidebar"] div[role="radiogroup"] > label {
    border-radius: 10px;
    padding: 6px 10px;
    margin-bottom: 4px;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: rgba(168,85,247,0.15);
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    color: white;
    font-weight: 700;
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

.acerto {
    border:2px solid #00E676;
    box-shadow:0 0 14px rgba(0,230,118,.8);
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logado:
    st.markdown("""
    <div class="login-card">
        <h2>🍀 Lotomilion Estrategista</h2>
        <p>Inteligência estatística aplicada à Lotofácil<br><b>Acesso Premium</b></p>
    """, unsafe_allow_html=True)

    email = st.text_input("", placeholder="seu@email.com", label_visibility="collapsed")

    if st.button("Entrar no Painel Premium", use_container_width=True):
        ok, msg = verificar_usuario(email)
        if not ok:
            st.error(msg)
            st.stop()

        st.session_state.logado = True
        st.session_state.email = email
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ======================================================
# MENU LATERAL
# ======================================================

st.sidebar.title("🍀 Lotomilion")
st.sidebar.caption(st.session_state.email)

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
        st.subheader("🎯 Escolha a Estratégia")
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

            st.subheader("🧩 Base de 21 dezenas")
            fixas_txt = st.text_area("🔒 9 dezenas FIXAS")
            variaveis_txt = st.text_area("🔄 12 dezenas VARIÁVEIS")

            if st.button("🧠 Gerar Jogos"):
                fixas = converter_lista(fixas_txt)
                variaveis = converter_lista(variaveis_txt)
                dezenas = sorted(set(fixas + variaveis))

                if len(dezenas) != 21:
                    st.error("Use exatamente 21 dezenas.")
                    st.stop()

                st.session_state.jogos = gerar_fechamento_21_8(dezenas)

        # ================= HISTÓRICO REAL (CORRIGIDO) =================
        else:
            st.info(
                "📊 Geração automática baseada nos números mais fortes "
                "dos últimos sorteios."
            )

            if st.button("🧠 Gerar Jogos"):
                historico = carregar_historico(qtd=50)

                # gera base de 21 dezenas a partir do ranking real
                _, ranking = gerar_jogos_historico_real(
                    list(range(1, 22)), historico
                )

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

    if st.session_state.jogos:
        st.subheader("🎲 Jogos Gerados")
        for i, jogo in enumerate(st.session_state.jogos, 1):
            cols = st.columns(5)
            for c, n in zip(cols * 3, jogo):
                c.markdown(
                    f"<div class='numero'>{n:02d}</div>",
                    unsafe_allow_html=True
                )

# ======================================================
# OUTROS MENUS
# ======================================================

elif menu == "🎯 Gerador Simples":
    st.title("🎯 Gerador Simples")
    if st.button("Gerar jogo"):
        jogo = sorted(random.sample(range(1, 26), 15))
        st.write(" ".join(f"{n:02d}" for n in jogo))

elif menu == "ℹ️ Sobre":
    st.title("ℹ️ Sobre")
    st.write("Sistema estatístico educacional. Não garante premiação.")
