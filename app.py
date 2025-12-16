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
    padding:12px;
    border-radius:12px;
    font-size:16px;
    font-weight:700;
    text-align:center;
}
.bloco-jogo {
    margin-bottom:22px;
    padding-bottom:12px;
    border-bottom:1px solid #e6e6e6;
}
.aviso-topo {
    font-size:12px;
    color:#666;
    background:#f7f2fa;
    padding:8px 12px;
    border-radius:8px;
    margin-bottom:14px;
}
.aviso {
    font-size:12px;
    color:#777;
    margin-top:16px;
}
.titulo-estrategia {
    border-left:6px solid #7A1FA2;
    padding-left:12px;
    margin-top:12px;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# ================= AVISO JURÍDICO TOPO =================
st.markdown("""
<div class='aviso-topo'>
Ferramenta educacional e estatística independente.  
Sem vínculo com a Caixa, Loterias Caixa ou órgãos oficiais.
</div>
""", unsafe_allow_html=True)

# ================= LOGIN =================
st.session_state.setdefault("logado", False)
st.session_state.setdefault("usuario", "")
st.session_state.setdefault("estrategia", "fechamento")

if not st.session_state.logado:
    st.title("🔐 Acesso • Lotomilion Estrategista")
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
Aqui o jogo é feito com **organização**,  
pensando em **chegar perto**, bater na **quadra, quina ou 14 pontos**,  
sem achismo e sem promessa.
""")

# ================= BOTÕES DE ESTRATÉGIA =================
c1, c2 = st.columns(2)

if c1.button("🧠 Fechamento 21 (Principal)", use_container_width=True):
    st.session_state.estrategia = "fechamento"

if c2.button("🔥 Frequencial (em breve)", use_container_width=True):
    st.info("Estratégia frequencial será liberada na próxima atualização.")

# ================= DESCRIÇÃO ESTRATÉGIA =================
if st.session_state.estrategia == "fechamento":
    st.markdown("""
    <div class='titulo-estrategia'>
        <h4>🧠 Fechamento 21 dezenas (9 Fixas + 12 Variáveis)</h4>
        <p>
        Estratégia clássica, muito usada por quem busca <b>chegar perto</b>.  
        Se as 15 dezenas do sorteio estiverem dentro das 21 escolhidas,
        o modelo favorece bater <i>quadra, quina ou até 14 pontos</i>,
        dependendo do cenário.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ================= ENTRADA =================
st.subheader("🎯 Monte sua base de 21 dezenas")

fixas_txt = st.text_area(
    "🔒 9 dezenas FIXAS (as que você confia)",
    help="Entram em todos os jogos"
)

variaveis_txt = st.text_area(
    "🔄 12 dezenas VARIÁVEIS (fazem a rotação)",
    help="Responsáveis pela cobertura estatística"
)

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
        st.error("As dezenas não podem se repetir.")
        st.stop()

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

# ================= GRÁFICO =================
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

# ================= AVISO FINAL =================
st.markdown("""
<div class='aviso'>
Este aplicativo é educacional e estatístico.  
A Lotofácil é um jogo de azar e não há garantia de premiação,
inclusive 13, 14 ou 15 pontos.
</div>
""", unsafe_allow_html=True)
