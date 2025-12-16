import streamlit as st
import pandas as pd
import plotly.express as px

from utils import converter_lista
from engine import gerar_fechamento_21_8
from simulador import simular_cenario
from historico import registrar_analise, listar_analises_usuario, gerar_ranking

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
    padding:10px;
    border-radius:12px;
    font-size:15px;
    font-weight:700;
    text-align:center;
    margin:4px;
}

.bloco-jogo {
    margin-bottom:20px;
    padding-bottom:10px;
    border-bottom:1px solid #e0e0e0;
}

.aviso {
    font-size:12px;
    color:#777;
    margin-top:8px;
    text-align:center;
}

.copy-box {
    background:#f3e5f5;
    border-radius:8px;
    padding:6px;
    font-size:13px;
    margin-top:6px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
st.session_state.setdefault("logado", False)
st.session_state.setdefault("usuario", "")

if not st.session_state.logado:
    st.title("🔐 Acesso Lotomilion Estrategista")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")

    if st.button("🔓 Entrar no Painel"):
        if u and s:
            st.session_state.logado = True
            st.session_state.usuario = u
            st.rerun()
        else:
            st.warning("Informe usuário e senha")

    st.stop()

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.write(f"👤 **{st.session_state.usuario}**")

st.markdown("""
Onde o apostador joga com **organização**,  
pensando em **chegar perto**, bater na **quadra, quina ou 14 pontos**,  
sem achismo e sem promessa.
""")

st.markdown("""
<div class='aviso'>
Ferramenta educacional e estatística.  
Sem vínculo com a Caixa ou Loterias Caixa.  
A Lotofácil é jogo de azar e não há garantia de prêmios.
</div>
""", unsafe_allow_html=True)

# ================= CONTROLE DE VISUAL =================
st.divider()
modo_detalhado = st.toggle("🧩 Modo detalhado (melhor no PC)", value=True)

# ================= ENTRADA =================
st.subheader("🎯 Monte sua base de 21 dezenas")

fixas_txt = st.text_area("🔒 9 dezenas FIXAS (aquelas que você confia)")
variaveis_txt = st.text_area("🔄 12 dezenas VARIÁVEIS (para rodar o jogo)")

# ================= PROCESSAMENTO =================
if st.button("🧠 Gerar Jogos Estratégicos"):

    fixas = converter_lista(fixas_txt)
    variaveis = converter_lista(variaveis_txt)

    if len(fixas) != 9:
        st.error("Informe exatamente 9 dezenas FIXAS.")
        st.stop()

    if len(variaveis) != 12:
        st.error("Informe exatamente 12 dezenas VARIÁVEIS.")
        st.stop()

    dezenas = sorted(set(fixas + variaveis))
    if len(dezenas) != 21:
        st.error("Não repita dezenas entre fixas e variáveis.")
        st.stop()

    st.session_state.jogos = gerar_fechamento_21_8(dezenas)
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
    st.caption("Modelo muito usado por quem busca organização e chegar perto do 14.")

    for i, jogo in enumerate(st.session_state.jogos, 1):

        if modo_detalhado:
            st.markdown(f"### Jogo {i}")

        numeros_str = " ".join(f"{n:02d}" for n in jogo)

        cols = st.columns(5)
        for c, n in zip(cols * 3, jogo):
            c.markdown(f"<div class='numero'>{n:02d}</div>", unsafe_allow_html=True)

        st.code(numeros_str, language="text")
        st.caption("👆 Copie e cole direto no volante")

        st.markdown("<div class='bloco-jogo'></div>", unsafe_allow_html=True)

    # ================= SIMULAÇÃO =================
    st.subheader("🧪 Simulação Estatística")

    if st.button("▶️ Simular 500 sorteios"):
        st.session_state.resultado_sim = simular_cenario(
            st.session_state.jogos,
            total_sorteios=500,
            universo=25,
            tamanho_jogo=15
        )

    if st.session_state.resultado_sim:
        r = st.session_state.resultado_sim
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Média", r["media"])
        c2.metric("🏆 Máximo", r["maximo"])
        c3.metric("❌ Zeros", r["zeros"])
        c4.metric("🔢 Sorteios", r["total"])

# ================= HISTÓRICO =================
st.divider()
st.subheader("📈 Histórico do Usuário")

dados = listar_analises_usuario(st.session_state.usuario)
if dados:
    df = pd.DataFrame(dados)
    fig = px.line(
        df,
        x=df.index,
        y="melhor_pontuacao",
        markers=True,
        color_discrete_sequence=["#7A1FA2"]
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= RANKING =================
st.divider()
st.subheader("🏅 Ranking Geral")
ranking = gerar_ranking()
if ranking:
    st.dataframe(pd.DataFrame(ranking), use_container_width=True)
