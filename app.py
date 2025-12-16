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
if "jogos" not in st.session_state:
    st.session_state.jogos = None

if "classificacao" not in st.session_state:
    st.session_state.classificacao = {
        "quentes": [],
        "mornas": [],
        "frias": []
    }

if "resultado_real" not in st.session_state:
    st.session_state.resultado_real = None

# ================= ESTILO =================
st.markdown("""
<style>
.numero {padding:14px;border-radius:16px;font-size:16px;font-weight:700;text-align:center;color:white;}
.quente {background:#E53935;}
.morna {background:#FB8C00;}
.fria {background:#3949AB;}
.neutra {background:#7A1FA2;}
.badge {padding:4px 12px;border-radius:14px;font-size:12px;color:white;margin-right:6px;}
.badge-quente {background:#E53935;}
.badge-morna {background:#FB8C00;}
.badge-fria {background:#3949AB;}
.copy-btn {background:#9C27B0;color:white;padding:7px 18px;border-radius:20px;border:none;cursor:pointer;}
</style>
""", unsafe_allow_html=True)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.caption("Ferramenta educacional • Sem vínculo com Loterias Caixa")

# ================= ESTRATÉGIA =================
estrategia = st.radio(
    "Estratégia",
    ["🎯 Fechamento 21", "🔥 Quentes / Mornas / Frias"],
    horizontal=True
)

# ================= ENTRADA =================
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
        st.session_state.classificacao = {
            "quentes": [],
            "mornas": [],
            "frias": []
        }
    else:
        jogos, classificacao = gerar_jogos_quentes_frios(dezenas)
        st.session_state.jogos = jogos
        st.session_state.classificacao = classificacao

# ================= RESULTADOS =================
if st.session_state.jogos:

    st.markdown("""
    <span class="badge badge-quente">🔥 Quentes</span>
    <span class="badge badge-morna">🟠 Mornas</span>
    <span class="badge badge-fria">❄️ Frias</span>
    """, unsafe_allow_html=True)

    for i, jogo in enumerate(st.session_state.jogos, 1):
        st.markdown(f"### Jogo {i}")

        for linha in range(0, 15, 5):
            cols = st.columns(5)
            for c, n in zip(cols, jogo[linha:linha+5]):
                if n in st.session_state.classificacao["quentes"]:
                    classe = "quente"
                elif n in st.session_state.classificacao["mornas"]:
                    classe = "morna"
                elif n in st.session_state.classificacao["frias"]:
                    classe = "fria"
                else:
                    classe = "neutra"

                c.markdown(f"<div class='numero {classe}'>{n:02d}</div>", unsafe_allow_html=True)

        html(
            f"<button class='copy-btn' onclick=\"navigator.clipboard.writeText('{ ' '.join(f'{n:02d}' for n in jogo) }')\">📋 Copiar Jogo</button>",
            height=40
        )
