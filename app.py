import streamlit as st
import pandas as pd
import plotly.express as px

from utils import converter_lista
from engine import gerar_fechamento_21_8
from simulador import simular_cenario
from historico import registrar_analise, listar_analises_usuario, gerar_ranking

st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🟣",
    layout="centered"
)

# ================= ESTILO =================
st.markdown("""
<style>
.numero {background:#7A1FA2;color:white;padding:12px;border-radius:12px;
font-size:16px;font-weight:700;text-align:center;}
.bloco-jogo {margin-bottom:22px;padding-bottom:12px;border-bottom:1px solid #e0e0e0;}
.aviso-topo {font-size:12px;color:#666;background:#f6effa;
padding:8px;border-radius:8px;margin-bottom:14px;}
.aviso {font-size:12px;color:#777;margin-top:16px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='aviso-topo'>
Ferramenta educacional e estatística. Sem vínculo com a Caixa ou Loterias Caixa.
</div>
""", unsafe_allow_html=True)

# ================= LOGIN =================
st.session_state.setdefault("logado", False)
st.session_state.setdefault("usuario", "")

if not st.session_state.logado:
    st.title("🔐 Lotomilion Estrategista")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")

    if st.button("🔓 Entrar"):
        if u and s:
            st.session_state.logado = True
            st.session_state.usuario = u
            st.rerun()
    st.stop()

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.write(f"👤 **{st.session_state.usuario}**")

st.markdown("""
Jogo organizado, pensado para **chegar perto**.  
Modelo muito usado por quem busca **quadra, quina ou 14 pontos**,
sem achismo e sem promessa.
""")

# ================= ENTRADA =================
st.subheader("🎯 Base de 21 dezenas")

fixas_txt = st.text_area("🔒 9 FIXAS")
variaveis_txt = st.text_area("🔄 12 VARIÁVEIS")

# ================= PROCESSAMENTO =================
if st.button("🧠 Gerar Jogos"):
    fixas = converter_lista(fixas_txt)
    variaveis = converter_lista(variaveis_txt)

    if len(fixas) != 9 or len(variaveis) != 12:
        st.error("Informe 9 fixas e 12 variáveis.")
        st.stop()

    dezenas = sorted(set(fixas + variaveis))
    jogos = gerar_fechamento_21_8(dezenas)

    st.session_state.jogos = jogos
    st.session_state.analise_pronta = True
    st.session_state.resultado_sim = None

    registrar_analise(
        st.session_state.usuario,
        "Fechamento 21 (9F + 12V)",
        dezenas,
        0
    )

# ================= RESULTADOS =================
if st.session_state.get("analise_pronta"):
    st.subheader("🎲 Jogos Gerados (8 bilhetes)")

    for i, jogo in enumerate(st.session_state.jogos, 1):
        st.markdown(f"**Jogo {i}**")
        cols = st.columns(5)
        for idx, n in enumerate(jogo):
            cols[idx % 5].markdown(
                f"<div class='numero'>{n:02d}</div>",
                unsafe_allow_html=True
            )
        st.markdown("<div class='bloco-jogo'></div>", unsafe_allow_html=True)

    if st.button("▶️ Simular 500 sorteios"):
        st.session_state.resultado_sim = simular_cenario(st.session_state.jogos)

    if st.session_state.get("resultado_sim"):
        r = st.session_state.resultado_sim
        st.metric("📊 Média", r["media"])
        st.metric("🏆 Máximo", r["maximo"])

# ================= HISTÓRICO =================
st.divider()
st.subheader("📈 Histórico")
dados = listar_analises_usuario(st.session_state.usuario)
if dados:
    df = pd.DataFrame(dados)
    fig = px.line(df, y="melhor_pontuacao")
    st.plotly_chart(fig, use_container_width=True)

# ================= RANKING =================
st.divider()
st.subheader("🏅 Ranking")
ranking = gerar_ranking()
if ranking:
    st.dataframe(pd.DataFrame(ranking))

st.markdown("""
<div class='aviso'>
Lotofácil é um jogo de azar. Não há garantia de premiação.
</div>
""", unsafe_allow_html=True)
