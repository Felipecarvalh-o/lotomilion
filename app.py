import streamlit as st
from streamlit.components.v1 import html

from utils import converter_lista
from engine import gerar_fechamento_21_8, gerar_jogos_quentes_frios
from simulador import simular_cenario

# ================= CONFIG =================
st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🟣",
    layout="centered"
)

# ================= SESSION STATE =================
for k in ["jogos", "classificacao", "resultado_real"]:
    if k not in st.session_state:
        st.session_state[k] = None

# ================= ESTILO =================
st.markdown("""
<style>
.numero {padding:14px;border-radius:16px;font-weight:700;color:white;text-align:center}
.quente {background:#E53935}
.morna {background:#FB8C00}
.fria {background:#3949AB}
.neutra {background:#7A1FA2}

.badge {padding:4px 12px;border-radius:14px;color:white;font-size:12px;margin-right:6px}
.badge-quente {background:#E53935}
.badge-morna {background:#FB8C00}
.badge-fria {background:#3949AB}

.copy-btn {
    background:#9C27B0;color:white;padding:6px 16px;
    border-radius:18px;border:none;cursor:pointer
}
</style>
""", unsafe_allow_html=True)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.caption("Ferramenta educacional • Sem vínculo com Loterias Caixa")

# ================= PASSO 1 =================
estrategia = st.radio(
    "🧠 Escolha a estratégia",
    ["🎯 Fechamento 21", "🔥 Quentes & Frios"],
    horizontal=True
)

# ================= PASSO 2 =================
fixas_txt = st.text_area("🔒 9 FIXAS")
variaveis_txt = st.text_area("🔄 12 VARIÁVEIS")

if st.button("🧠 Gerar Jogos"):
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
        st.session_state.jogos = gerar_fechamento_21_8(dezenas)
        st.session_state.classificacao = None
    else:
        jogos, classificacao = gerar_jogos_quentes_frios(dezenas)
        st.session_state.jogos = jogos
        st.session_state.classificacao = classificacao

    st.session_state.resultado_real = None

# ================= RESULTADOS =================
if st.session_state.jogos:

    st.subheader("🎲 Jogos Gerados (15 dezenas)")

    # LEGENDA
    if st.session_state.classificacao:
        st.markdown("""
        <span class="badge badge-quente">🔥 Quentes</span>
        <span class="badge badge-morna">🟠 Mornas</span>
        <span class="badge badge-fria">❄️ Frias</span>
        """, unsafe_allow_html=True)

    # RESULTADO OFICIAL
    resultado_txt = st.text_input("📥 Resultado oficial (15 dezenas, opcional)")
    if st.button("📌 Aplicar Resultado"):
        r = converter_lista(resultado_txt)
        if len(r) == 15:
            st.session_state.resultado_real = r

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
                    else:
                        classe = "fria"

                c.markdown(f"<div class='numero {classe}'>{n:02d}</div>", unsafe_allow_html=True)

        if st.session_state.resultado_real:
            acertos = len(set(jogo) & set(st.session_state.resultado_real))
            st.info(f"🎯 {acertos} pontos")

        html(
            f"<button class='copy-btn' onclick=\"navigator.clipboard.writeText('{ ' '.join(f'{n:02d}' for n in jogo) }')\">📋 Copiar</button>",
            height=40
        )
