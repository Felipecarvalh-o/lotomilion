import streamlit as st
import pandas as pd
import plotly.express as px

from historico import registrar_analise, listar_analises_usuario, gerar_ranking
from simulador import simular_cenario
from utils import converter_lista

# ==================================================
# CONFIGURAÇÃO
# ==================================================

st.set_page_config(
    page_title="Lotofácil Inteligente",
    page_icon="🟣",
    layout="centered"
)

# ==================================================
# ESTILO GLOBAL (ROXO LOTOFÁCIL)
# ==================================================

st.markdown("""
<style>
.numero {
    background:#7D3C98;
    color:white;
    padding:10px;
    border-radius:10px;
    font-size:18px;
    font-weight:700;
    text-align:center;
}
.jogo {
    margin-bottom:14px;
    padding-bottom:8px;
    border-bottom:1px solid #eee;
}
.aviso {
    font-size:12px;
    color:#777;
    margin-top:10px;
}
.titulo {
    color:#7D3C98;
}
.score {
    font-size:14px;
    font-weight:600;
    color:#555;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# ESTADO
# ==================================================

st.session_state.setdefault("logado", False)
st.session_state.setdefault("usuario", "")
st.session_state.setdefault("jogos", [])
st.session_state.setdefault("resultado_sim", None)

# ==================================================
# LOGIN SIMPLES
# ==================================================

if not st.session_state.logado:
    st.title("🟣 Lotofácil Inteligente")
    st.caption("Quem estuda, joga diferente.")

    usuario = st.text_input("Seu nome ou apelido")
    if st.button("🎯 Entrar para Análise"):
        if usuario:
            st.session_state.usuario = usuario
            st.session_state.logado = True
            st.rerun()

    st.stop()

# ==================================================
# TOPO
# ==================================================

st.title("🟣 Lotofácil Inteligente")
st.markdown(
    "<div class='score'>Análise estatística • Estudo de comportamento • Organização de jogos</div>",
    unsafe_allow_html=True
)

# ==================================================
# ENTRADA PRINCIPAL
# ==================================================

st.subheader("🎯 Escolha suas 21 dezenas")

st.markdown("""
Aqui você monta o **bolo de 21 dezenas**.<br>
A ideia não é adivinhar o resultado, e sim **organizar bem o jogo**
pra tentar **chegar perto** — 13 ou 14 pontos.
""", unsafe_allow_html=True)

dezenas_txt = st.text_area(
    "Digite as 21 dezenas (ex: 01 02 03 ...)",
    placeholder="01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21"
)

# ==================================================
# GERAÇÃO DOS JOGOS (FECHAMENTO EDUCACIONAL)
# ==================================================

if st.button("🧠 Montar Jogos com Leitura Inteligente"):
    dezenas = converter_lista(dezenas_txt)

    if len(dezenas) != 21:
        st.error("⚠️ Informe exatamente 21 dezenas.")
    else:
        # fechamento educacional simplificado (8 jogos)
        jogos = [
            dezenas[i:i+15]
            for i in range(0, 21, 3)
        ][:8]

        st.session_state.jogos = jogos
        st.session_state.resultado_sim = None

        registrar_analise(
            st.session_state.usuario,
            "lotofacil_21",
            dezenas,
            0
        )

# ==================================================
# EXIBIÇÃO DOS JOGOS
# ==================================================

if st.session_state.jogos:
    st.subheader("🎲 Jogos Montados")

    for i, jogo in enumerate(st.session_state.jogos, start=1):
        st.markdown(f"**Jogo {i}**")

        cols = st.columns(5)
        for idx, n in enumerate(jogo):
            cols[idx % 5].markdown(
                f"<div class='numero'>{n:02d}</div>",
                unsafe_allow_html=True
            )

        st.markdown("<div class='jogo'></div>", unsafe_allow_html=True)

# ==================================================
# SIMULAÇÃO
# ==================================================

if st.session_state.jogos:
    st.subheader("🧪 Simulação Estatística")

    st.markdown("""
Aqui o sistema faz **centenas de sorteios aleatórios**
só pra observar o comportamento dos jogos.<br>
Não é previsão. É estudo.
""", unsafe_allow_html=True)

    if st.button("▶️ Simular 500 Cenários"):
        st.session_state.resultado_sim = simular_cenario(
            st.session_state.jogos,
            total_sorteios=500,
            universo=25,
            tamanho_jogo=15
        )

# ==================================================
# RESULTADOS DA SIMULAÇÃO
# ==================================================

if st.session_state.resultado_sim:
    r = st.session_state.resultado_sim

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📊 Média", r["media"])
    c2.metric("🏆 Máximo", r["maximo"], help="13, 14 ou até 15 em algum cenário")
    c3.metric("❌ Zeros", r["zeros"])
    c4.metric("🔢 Simulações", r["total"])

# ==================================================
# HISTÓRICO
# ==================================================

st.divider()
st.subheader("📈 Seu Histórico")

dados = listar_analises_usuario(st.session_state.usuario)
if dados:
    df = pd.DataFrame(dados)
    fig = px.line(
        df,
        y="melhor_pontuacao",
        markers=True,
        title="Evolução das Análises"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Ainda não há histórico suficiente para análise.")

# ==================================================
# RANKING
# ==================================================

st.divider()
st.subheader("🏅 Ranking Geral")

ranking = gerar_ranking()
if ranking:
    st.dataframe(pd.DataFrame(ranking), use_container_width=True)

# ==================================================
# AVISO LEGAL
# ==================================================

st.markdown("""
<div class='aviso'>
Este aplicativo é uma ferramenta independente de estudo estatístico.<br>
Não possui vínculo com a Caixa Econômica Federal ou Loterias Caixa.<br>
A Lotofácil é um jogo de azar e não há garantia de premiação,
incluindo 13, 14 ou 15 pontos.
</div>
""", unsafe_allow_html=True)
