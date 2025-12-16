import streamlit as st
from streamlit.components.v1 import html

from utils import converter_lista
from engine import gerar_fechamento_21_8, gerar_jogos_quentes_frios

# ================= CONFIG =================
st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🟣",
    layout="centered"
)

# ================= SESSION STATE =================
for k in [
    "jogos", "classificacao", "resultado_real",
    "resultado_ativo", "nome_estrategia"
]:
    if k not in st.session_state:
        st.session_state[k] = None

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
}
.quente {background:#E53935;}
.morna {background:#FB8C00;}
.fria {background:#3949AB;}
.neutra {background:#7A1FA2;}

.badge {padding:4px 10px;border-radius:12px;font-size:12px;color:white;margin-right:6px;}
.badge-q {background:#E53935;}
.badge-m {background:#FB8C00;}
.badge-f {background:#3949AB;}

.copy-btn {
    background:#9C27B0;
    color:white;
    padding:7px 18px;
    border-radius:20px;
    border:none;
    cursor:pointer;
}
</style>
""", unsafe_allow_html=True)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.caption("Ferramenta educacional e estatística • Sem vínculo com Loterias Caixa")

st.markdown("""
Aqui o jogo é **organizado**, pensado pra  
chegar na **quadra, quina, 13 ou 14 pontos**,  
sem chute e sem promessa milagrosa.
""")

# ================= PASSO 1 =================
st.subheader("🧠 Passo 1 — Estratégia")
estrategia = st.radio(
    "",
    ["🎯 Fechamento 21", "🔥 Quentes, Mornas e Frias"],
    horizontal=True
)

# ================= PASSO 2 =================
st.subheader("🎯 Passo 2 — Base de 21 dezenas")
fixas_txt = st.text_area("🔒 9 dezenas FIXAS")
variaveis_txt = st.text_area("🔄 12 dezenas VARIÁVEIS")

# ================= GERAR =================
if st.button("🧠 Gerar Jogos"):

    fixas = converter_lista(fixas_txt)
    variaveis = converter_lista(variaveis_txt)

    if len(fixas) != 9 or len(variaveis) != 12:
        st.error("Use exatamente 9 fixas e 12 variáveis.")
        st.stop()

    dezenas = sorted(set(fixas + variaveis))

    if "Fechamento" in estrategia:
        st.session_state.jogos = gerar_fechamento_21_8(dezenas)
        st.session_state.classificacao = None
        st.session_state.nome_estrategia = "Fechamento 21"
    else:
        jogos, classificacao = gerar_jogos_quentes_frios(dezenas)
        st.session_state.jogos = jogos
        st.session_state.classificacao = classificacao
        st.session_state.nome_estrategia = "Quentes / Mornas / Frias"

    st.session_state.resultado_real = None
    st.session_state.resultado_ativo = False

# ================= RESULTADOS =================
if st.session_state.jogos:

    st.subheader("🎲 Jogos Gerados — 15 dezenas")

    if st.session_state.classificacao:
        st.markdown("""
        <span class="badge badge-q">🔥 Quentes</span>
        <span class="badge badge-m">🟠 Mornas</span>
        <span class="badge badge-f">❄️ Frias</span>
        """, unsafe_allow_html=True)

    # Resultado oficial
    st.subheader("📥 Resultado Oficial (opcional)")
    resultado_txt = st.text_input("Digite as 15 dezenas sorteadas")

    if st.button("📌 Aplicar Resultado"):
        r = converter_lista(resultado_txt)
        if len(r) == 15:
            st.session_state.resultado_real = r
            st.session_state.resultado_ativo = True
        else:
            st.warning("Informe exatamente 15 dezenas.")

    for i, jogo in enumerate(st.session_state.jogos, 1):

        st.markdown(f"### Jogo {i}")

        for linha in range(0, 15, 5):
            cols = st.columns(5)
            for c, n in zip(cols, jogo[linha:linha+5]):

                classe = "neutra"
                if st.session_state.classificacao:
                    if n in st.session_state.classificacao["quentes"]:
                        classe = "quente"
                    elif n in st.session_state.classificacao["mornas"]:
                        classe = "morna"
                    elif n in st.session_state.classificacao["frias"]:
                        classe = "fria"

                c.markdown(
                    f"<div class='numero {classe}'>{n:02d}</div>",
                    unsafe_allow_html=True
                )

        if st.session_state.resultado_ativo:
            acertos = len(set(jogo) & set(st.session_state.resultado_real))
            st.info(f"🎯 {acertos} pontos")

        html(
            f"""
            <button class="copy-btn"
            onclick="navigator.clipboard.writeText('{" ".join(f"{n:02d}" for n in jogo)}')">
            📋 Copiar Jogo
            </button>
            """,
            height=40
        )

# ================= AVISO FINAL =================
st.caption(
    "Este app é educacional e estatístico. "
    "Lotofácil é um jogo de azar e não há garantia de premiação."
)
