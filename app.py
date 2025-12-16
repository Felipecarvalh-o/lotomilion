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
    padding:14px;
    border-radius:16px;
    font-size:16px;
    font-weight:700;
    text-align:center;
}
.bloco-jogo {
    margin-bottom:28px;
    padding-bottom:20px;
    border-bottom:1px solid #2a2a2a;
}
.badge {
    padding:4px 12px;
    border-radius:14px;
    font-size:12px;
    color:white;
    margin-right:6px;
}
.badge-quente {background:#E53935;}
.badge-morna {background:#FB8C00;}
.badge-fria {background:#3949AB;}

.copy-btn {
    background:#9C27B0;
    color:white;
    padding:7px 18px;
    border-radius:20px;
    font-size:13px;
    border:none;
    cursor:pointer;
    margin-top:10px;
}
.copy-btn:hover {opacity:0.85;}

.aviso {
    font-size:12px;
    color:#999;
    margin-top:26px;
    line-height:1.6;
}
</style>
""", unsafe_allow_html=True)

# ================= AVISO SUPERIOR =================
st.caption(
    "Ferramenta educacional e estatística • "
    "Sem vínculo com Loterias Caixa"
)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")

st.markdown("""
Aqui o jogo é **organizado**, pensado pra  
chegar na **quadra, quina, 13 ou 14 pontos**,  
sem chute e sem promessa milagrosa.
""")

# ================= PASSO 1 =================
st.subheader("🧠 Passo 1 — Escolha a Estratégia")

estrategia = st.radio(
    "",
    [
        "🎯 Fechamento 21 (9 fixas + 12 variáveis)",
        "🔥 Frequencial (quentes e frios)"
    ],
    horizontal=True
)

# ================= PASSO 2 =================
st.subheader("🎯 Passo 2 — Monte sua base de 21 dezenas")

fixas_txt = st.text_area(
    "🔒 9 dezenas FIXAS",
    help="Essas entram em todos os jogos"
)

variaveis_txt = st.text_area(
    "🔄 12 dezenas VARIÁVEIS",
    help="Essas fazem a rotação do jogo"
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
        st.error("Não repita dezenas.")
        st.stop()

    if "Fechamento" in estrategia:
        jogos = gerar_fechamento_21_8(dezenas)
        st.session_state.nome_estrategia = "Fechamento 21"
        st.session_state.classificacao = None
    else:
        jogos, classificacao = gerar_jogos_quentes_frios(dezenas)
        st.session_state.nome_estrategia = "Quentes e Frios"
        st.session_state.classificacao = classificacao

    st.session_state.jogos = jogos
    st.session_state.simulado = None

# ================= RESULTADOS =================
if "jogos" in st.session_state:

    st.subheader("🎲 Passo 3 — Jogos Gerados")
    st.caption(f"Estratégia ativa: **{st.session_state.nome_estrategia}**")

    for i, jogo in enumerate(st.session_state.jogos, 1):

        st.markdown(f"### Jogo {i}")

        # BADGES VISUAIS
        if st.session_state.nome_estrategia == "Quentes e Frios":
            st.markdown(
                """
                <span class="badge badge-quente">🔥 Quentes</span>
                <span class="badge badge-morna">🟠 Mornas</span>
                <span class="badge badge-fria">❄️ Frias</span>
                """,
                unsafe_allow_html=True
            )

        # GRADE 5x3
        for linha in range(0, 15, 5):
            cols = st.columns(5, gap="small")
            for c, n in zip(cols, jogo[linha:linha+5]):
                c.markdown(
                    f"<div class='numero'>{n:02d}</div>",
                    unsafe_allow_html=True
                )

        # BOTÃO COPIAR
        jogo_txt = " ".join(f"{n:02d}" for n in jogo)
        st.markdown(
            f"""
            <button class="copy-btn"
            onclick="navigator.clipboard.writeText('{jogo_txt}')">
            📋 Copiar Jogo
            </button>
            """,
            unsafe_allow_html=True
        )

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

        c1.metric("📊 Média", r["media"])
        c2.metric("🏆 Máximo", r["maximo"])
        c3.metric("❌ Zerou", r["zeros"])
        c4.metric("🔢 Sorteios", r["total"])

# ================= AVISO FINAL =================
st.markdown("""
<div class='aviso'>
Este aplicativo é uma ferramenta educacional e estatística.  
Não possui vínculo com a Caixa Econômica Federal ou Loterias Caixa.  
A Lotofácil é um jogo de azar e não há garantia de premiação,
incluindo 13, 14 ou 15 pontos.
</div>
""", unsafe_allow_html=True)
