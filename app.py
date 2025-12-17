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
    "estrategia": None,
    "jogos": None,
    "classificacao": None,
    "resultado_real": None,
    "comparacao_ativa": False,
    "nome_estrategia": None
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ================= ESTILO =================
st.markdown("""
<style>
.card {
    background:#151515;
    padding:20px;
    border-radius:20px;
    text-align:center;
    cursor:pointer;
    transition:all .25s ease;
    border:2px solid transparent;
}
.card:hover {
    border-color:#9C27B0;
    transform:scale(1.03);
}
.card-ativa {
    border-color:#9C27B0;
    box-shadow:0 0 18px rgba(156,39,176,.6);
}

.numero {
    padding:14px;
    border-radius:16px;
    font-size:16px;
    font-weight:700;
    text-align:center;
    color:white;
    background:#6A1B9A;
    position:relative;
}

.acerto {
    border:2px solid #00E676;
    box-shadow:0 0 14px rgba(0,230,118,.8);
}

.trofeu {
    position:absolute;
    top:-6px;
    right:-6px;
    font-size:14px;
}

.ranking-box {
    background:#111;
    padding:16px;
    border-radius:16px;
    margin-top:18px;
}
</style>
""", unsafe_allow_html=True)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.caption("Ferramenta educacional e estatística • Sem vínculo com Loterias Caixa")

# ================= MENU EM CARDS =================
st.subheader("🎯 Escolha a Estratégia")

c1, c2 = st.columns(2)

with c1:
    if st.button("🎯 Fechamento 21", use_container_width=True):
        st.session_state.estrategia = "fechamento"
        st.session_state.nome_estrategia = "Fechamento 21"

with c2:
    if st.button("📊 Histórico Real", use_container_width=True):
        st.session_state.estrategia = "historico"
        st.session_state.nome_estrategia = "Histórico Real"

# ================= BASE =================
if st.session_state.estrategia:
    st.subheader("🧩 Base de 21 dezenas")
    fixas_txt = st.text_area("🔒 9 dezenas FIXAS")
    variaveis_txt = st.text_area("🔄 12 dezenas VARIÁVEIS")

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

        if st.session_state.estrategia == "fechamento":
            st.session_state.jogos = gerar_fechamento_21_8(dezenas)
            st.session_state.classificacao = None

        else:
            historico = carregar_historico(qtd=50)
            jogos, classificacao = gerar_jogos_historico_real(dezenas, historico)
            st.session_state.jogos = jogos
            st.session_state.classificacao = classificacao

        st.session_state.comparacao_ativa = False

# ================= JOGOS =================
if st.session_state.jogos:
    st.subheader(f"🎲 Jogos Gerados — {st.session_state.nome_estrategia}")

    for i, jogo in enumerate(st.session_state.jogos, 1):
        st.markdown(f"### Jogo {i}")
        cols = st.columns(5)

        for c, n in zip(cols * 3, jogo):
            acerto = (
                st.session_state.comparacao_ativa
                and n in (st.session_state.resultado_real or [])
            )

            extra = "acerto" if acerto else ""
            trofeu = "🏆" if acerto else ""

            c.markdown(
                f"""
                <div class="numero {extra}">
                    {n:02d}
                    <span class="trofeu">{trofeu}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.session_state.comparacao_ativa:
            pontos = len(set(jogo) & set(st.session_state.resultado_real))
            st.success(f"🎯 {pontos} pontos")

# ================= RANKING =================
if st.session_state.classificacao:
    st.subheader("🧠 Ranking Estatístico das Dezenas")
    st.caption(
        "Classificação estatística baseada na estratégia Histórico Real. "
        "Não representa previsão ou garantia de acerto."
    )

    with st.container():
        st.markdown("🔴 **Quentes — maior presença histórica**")
        st.write(" • ".join(f"{n:02d}" for n in st.session_state.classificacao["quentes"]))

        st.markdown("🟠 **Mornas — presença intermediária**")
        st.write(" • ".join(f"{n:02d}" for n in st.session_state.classificacao["mornas"]))

        st.markdown("🔵 **Frias — menor presença histórica**")
        st.write(" • ".join(f"{n:02d}" for n in st.session_state.classificacao["frias"]))
