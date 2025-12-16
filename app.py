import streamlit as st
import pandas as pd
import plotly.express as px
import pyperclip

from utils import converter_lista
from engine import gerar_fechamento_21_8, gerar_jogos_quentes_frios
from simulador import simular_cenario

# ================= CONFIG =================
st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🟣",
    layout="centered"
)

# ================= ESTILO GLOBAL =================
st.markdown("""
<style>
.numero {
    background:#7A1FA2;
    color:white;
    padding:14px;
    border-radius:16px;
    font-size:16px;
    font-weight:700;
    text-align:center;
}
.bloco-jogo {
    margin-bottom:26px;
    padding-bottom:16px;
    border-bottom:1px solid #333;
}
.copy-btn {
    background:#9C27B0;
    color:white;
    padding:6px 14px;
    border-radius:20px;
    font-size:13px;
    text-align:center;
    margin-top:6px;
}
.aviso {
    font-size:12px;
    color:#999;
    margin-top:22px;
    line-height:1.5;
}
</style>
""", unsafe_allow_html=True)

# ================= AVISO JURÍDICO SUPERIOR =================
st.caption(
    "Ferramenta educacional e estatística. "
    "Sem vínculo com Loterias Caixa ou órgãos oficiais."
)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")

st.markdown("""
Aqui o jogo é **organizado**, pensado pra  
chegar na **quadra, quina, 13 ou 14 pontos**,  
sem chute, sem milagre e sem promessa vazia.
""")

# ================= ESTRATÉGIAS =================
st.subheader("🧠 Escolha a Estratégia")

estrategia = st.radio(
    "",
    [
        "🎯 Fechamento 21 dezenas (9 fixas + 12 variáveis)",
        "🔥 Frequencial (quentes e frios)"
    ],
    horizontal=True
)

# ================= ENTRADAS =================
st.subheader("📌 Monte sua base de dezenas")

fixas_txt = st.text_area(
    "🔒 9 dezenas FIXAS (as que você confia)",
    help="Essas entram em todos os jogos"
)

variaveis_txt = st.text_area(
    "🔄 12 dezenas VARIÁVEIS (pra rodar o jogo)",
    help="Essas fazem a rotação"
)

# ================= PROCESSAMENTO =================
if st.button("🧠 Gerar Jogos Estratégicos"):

    fixas = converter_lista(fixas_txt)
    variaveis = converter_lista(variaveis_txt)

    if len(fixas) != 9 or len(variaveis) != 12:
        st.error("Use exatamente 9 fixas e 12 variáveis.")
        st.stop()

    dezenas = sorted(set(fixas + variaveis))
    if len(dezenas) != 21:
        st.error("Não repita dezenas entre fixas e variáveis.")
        st.stop()

    if "Fechamento" in estrategia:
        jogos = gerar_fechamento_21_8(dezenas)
        st.session_state.estrategia_nome = "Fechamento 21"
    else:
        jogos = gerar_jogos_quentes_frios(dezenas)
        st.session_state.estrategia_nome = "Frequencial"

    st.session_state.jogos = jogos
    st.session_state.simulado = None

# ================= RESULTADOS =================
if "jogos" in st.session_state:

    st.subheader(f"🎲 Jogos Gerados ({len(st.session_state.jogos)} bilhetes)")
    st.caption(f"Estratégia ativa: **{st.session_state.estrategia_nome}**")

    for i, jogo in enumerate(st.session_state.jogos, 1):

        st.markdown(f"### Jogo {i}")

        # Grade 5x3 (melhor pra mobile)
        for linha in range(0, 15, 5):
            cols = st.columns(5, gap="small")
            for c, n in zip(cols, jogo[linha:linha+5]):
                c.markdown(
                    f"<div class='numero'>{n:02d}</div>",
                    unsafe_allow_html=True
                )

        # BOTÃO COPIAR
        jogo_txt = " ".join(f"{n:02d}" for n in jogo)
        if st.button(f"📋 Copiar Jogo {i}", key=f"copy_{i}"):
            pyperclip.copy(jogo_txt)
            st.success("Jogo copiado!")

        st.markdown("<div class='bloco-jogo'></div>", unsafe_allow_html=True)

    # ================= SIMULAÇÃO =================
    st.subheader("🧪 Simulação Estatística")
    st.caption(
        "Cada clique gera novos sorteios aleatórios. "
        "Por isso a média pode variar — isso é normal e esperado."
    )

    if st.button("▶️ Simular 500 sorteios"):
        st.session_state.simulado = simular_cenario(st.session_state.jogos)

    if st.session_state.simulado:
        r = st.session_state.simulado
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("📊 Média de acertos", r["media"])
        c2.metric("🏆 Melhor cenário", r["maximo"])
        c3.metric("❌ Zerou", r["zeros"])
        c4.metric("🔢 Sorteios", r["total"])

# ================= AVISO FINAL =================
st.markdown("""
<div class='aviso'>
Este aplicativo não garante prêmios.  
Lotofácil é um jogo de azar.  
O objetivo aqui é **organizar o jogo, estudar padrões e reduzir o chute** —
não prometer quadra, quina ou 14 pontos.
</div>
""", unsafe_allow_html=True)
