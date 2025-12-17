from data.lotofacil_historico import carregar_historico
from engine import gerar_fechamento_21_8, gerar_jogos_historico_real
from utils import converter_lista

import streamlit as st
from streamlit.components.v1 import html

# ================= CONFIG =================
st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🟣",
    layout="centered"
)

# ================= SESSION STATE =================
defaults = {
    "jogos": None,
    "classificacao": None,
    "resultado_real": None,
    "comparacao_ativa": False,
    "mostrar_analise": False,
    "nome_estrategia": None
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ================= ESTILO =================
st.markdown("""
<style>
.numero {
    padding:14px;
    border-radius:16px;
    font-size:16px;
    font-weight:700;
    text-align:center;
    color:white;
    transition:all .3s ease;
}

.neutra {background:#6A1B9A;}

.quente {background:#E53935;}
.morna {background:#FB8C00;}
.fria {background:#3949AB;}

.acerto {
    border:2px solid #00E676;
    box-shadow:0 0 12px rgba(0,230,118,.7);
}

.legenda span {
    margin-right:14px;
    font-size:13px;
}

.ranking-box {
    background:#111;
    padding:14px;
    border-radius:14px;
    margin-top:14px;
}
</style>
""", unsafe_allow_html=True)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.caption("Ferramenta educacional e estatística • Sem vínculo com Loterias Caixa")

# ================= ESTRATÉGIA =================
st.subheader("🎯 Estratégia")
estrategia = st.radio(
    "",
    ["🎯 Fechamento 21", "📊 Histórico Real"]
)

# ================= BASE =================
st.subheader("🧩 Base de 21 dezenas")
fixas_txt = st.text_area("🔒 9 dezenas FIXAS")
variaveis_txt = st.text_area("🔄 12 dezenas VARIÁVEIS")

# ================= RESULTADO =================
st.subheader("📥 Resultado Oficial (opcional)")
resultado_txt = st.text_input("Informe o resultado do sorteio (15 dezenas)")

if st.button("📊 Ativar Comparação"):
    resultado = converter_lista(resultado_txt)
    if len(resultado) == 15:
        st.session_state.resultado_real = resultado
        st.session_state.comparacao_ativa = True
    else:
        st.warning("Informe exatamente 15 dezenas.")

# ================= GERAR =================
if st.button("🧠 Gerar Jogos"):
    fixas = converter_lista(fixas_txt)
    variaveis = converter_lista(variaveis_txt)

    dezenas = sorted(set(fixas + variaveis))
    if len(dezenas) != 21:
        st.error("Use exatamente 21 dezenas.")
        st.stop()

    if "Fechamento" in estrategia:
        st.session_state.jogos = gerar_fechamento_21_8(dezenas)
        st.session_state.classificacao = None
        st.session_state.nome_estrategia = "Fechamento 21"

    else:
        historico = carregar_historico(qtd=50)
        jogos, classificacao = gerar_jogos_historico_real(dezenas, historico)
        st.session_state.jogos = jogos
        st.session_state.classificacao = classificacao
        st.session_state.nome_estrategia = "Histórico Real"

    st.session_state.comparacao_ativa = False

# ================= TOGGLE =================
st.checkbox("🔄 Mostrar análise de frequência", key="mostrar_analise")

# ================= JOGOS =================
if st.session_state.jogos:
    st.subheader(f"🎲 Jogos Gerados — {st.session_state.nome_estrategia}")

    for i, jogo in enumerate(st.session_state.jogos, 1):
        st.markdown(f"### Jogo {i}")
        cols = st.columns(5)

        for c, n in zip(cols * 3, jogo):
            classe = "neutra"

            if st.session_state.comparacao_ativa and st.session_state.classificacao:
                if n in st.session_state.classificacao["quentes"]:
                    classe = "quente"
                elif n in st.session_state.classificacao["mornas"]:
                    classe = "morna"
                elif n in st.session_state.classificacao["frias"]:
                    classe = "fria"

            acerto = (
                st.session_state.comparacao_ativa
                and n in (st.session_state.resultado_real or [])
            )

            extra = "acerto" if acerto else ""

            c.markdown(
                f"<div class='numero {classe} {extra}'>{n:02d}</div>",
                unsafe_allow_html=True
            )

        if st.session_state.comparacao_ativa:
            pontos = len(set(jogo) & set(st.session_state.resultado_real))
            st.success(f"🎯 {pontos} pontos")

# ================= LEGENDA + RANKING =================
if st.session_state.mostrar_analise and st.session_state.classificacao:

    st.markdown("""
<div class="legenda">
<span>🔴 Quente — maior presença estatística</span>
<span>🟠 Morna — presença intermediária</span>
<span>🔵 Fria — menor presença estatística</span>
<span>🟢 Borda verde — número acertado no sorteio</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("### 🧠 Ranking Estatístico das Dezenas")
    st.caption("Classificação baseada na estratégia escolhida. Não é previsão.")

    for titulo, cor in [
        ("🔴 Quentes", "quentes"),
        ("🟠 Mornas", "mornas"),
        ("🔵 Frias", "frias")
    ]:
        st.markdown(f"**{titulo}**")
        st.write(" • ".join(f"{n:02d}" for n in st.session_state.classificacao[cor]))
