import streamlit as st
import pandas as pd
import plotly.express as px

from utils import converter_lista
from engine import gerar_fechamento_21_8, gerar_jogos_quentes_frios
from simulador import simular_cenario

# ================= CONFIG =================
st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🟣",
    layout="centered"
)

# ================= ESTILO =================
st.markdown("""
<style>
.numero {
    background:#7A1FA2;
    color:white;
    padding:12px;
    border-radius:14px;
    font-size:16px;
    font-weight:700;
    text-align:center;
}
.bloco-jogo {
    margin-bottom:20px;
    padding-bottom:10px;
    border-bottom:1px solid #333;
}
.aviso {
    font-size:12px;
    color:#999;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# ================= AVISO JURÍDICO SUTIL =================
st.caption(
    "Ferramenta educacional e estatística. "
    "Sem vínculo com Loterias Caixa."
)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")

st.markdown("""
Aqui o jogo é **organizado**, pensado pra  
chegar na **quadra, quina, 13 ou 14 pontos**,  
sem chute e sem promessa milagrosa.
""")

# ================= ENTRADA =================
st.subheader("🎯 Monte sua base de 21 dezenas")

fixas_txt = st.text_area("🔒 9 dezenas FIXAS (as que você confia)")
variaveis_txt = st.text_area("🔄 12 dezenas VARIÁVEIS (pra rodar o jogo)")

# ================= PROCESSAMENTO =================
if st.button("🧠 Gerar Jogos Estratégicos"):
    fixas = converter_lista(fixas_txt)
    variaveis = converter_lista(variaveis_txt)

    if len(fixas) != 9 or len(variaveis) != 12:
        st.error("Use exatamente 9 fixas e 12 variáveis.")
        st.stop()

    dezenas = sorted(set(fixas + variaveis))

    if len(dezenas) != 21:
        st.error("Não repita dezenas.")
        st.stop()

    st.session_state.jogos = gerar_fechamento_21_8(dezenas)
    st.session_state.simulado = None

# ================= RESULTADOS =================
if "jogos" in st.session_state:
    st.subheader("🎲 Jogos Gerados (8 bilhetes)")

    for i, jogo in enumerate(st.session_state.jogos, 1):
        st.markdown(f"**Jogo {i}**")

        for linha in range(0, 15, 5):
            cols = st.columns(5, gap="small")
            for c, n in zip(cols, jogo[linha:linha+5]):
                c.markdown(
                    f"<div class='numero'>{n:02d}</div>",
                    unsafe_allow_html=True
                )

        st.markdown("<div class='bloco-jogo'></div>", unsafe_allow_html=True)

    # ================= SIMULAÇÃO =================
    st.subheader("🧪 Simulação Estatística")
    st.caption("Cada clique simula novos sorteios aleatórios.")

    if st.button("▶️ Simular 500 sorteios"):
        st.session_state.simulado = simular_cenario(st.session_state.jogos)

    if st.session_state.simulado:
        r = st.session_state.simulado
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("📊 Média", r["media"])
        c2.metric("🏆 Máximo", r["maximo"])
        c3.metric("❌ Zerou", r["zeros"])
        c4.metric("🔢 Sorteios", r["total"])

# ================= AVISO FINAL =================
st.markdown("""
<div class='aviso'>
Este app não garante prêmios.  
Lotofácil é um jogo de azar.  
Aqui o foco é **estatística, organização e estudo**.
</div>
""", unsafe_allow_html=True)
