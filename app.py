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
defaults = {
    "jogos": None,
    "classificacao": {"quentes": [], "mornas": [], "frias": []},
    "nome_estrategia": "",
    "resultado_real": None,
    "resultado_ativo": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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

.badge {padding:4px 12px;border-radius:14px;font-size:12px;color:white;}
.badge-quente {background:#E53935;}
.badge-morna {background:#FB8C00;}
.badge-fria {background:#3949AB;}

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

# ================= PASSO 1 =================
estrategia = st.radio(
    "🧠 Estratégia",
    ["🎯 Fechamento 21", "🔥 Frequencial (quentes, mornas e frias)"],
    horizontal=True
)

# ================= PASSO 2 =================
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
    if len(dezenas) != 21:
        st.error("Não repita dezenas.")
        st.stop()

    if "Fechamento" in estrategia:
        st.session_state.jogos = gerar_fechamento_21_8(dezenas)
        st.session_state.classificacao = {"quentes": [], "mornas": [], "frias": []}
        st.session_state.nome_estrategia = "Fechamento 21"
    else:
        jogos, classificacao = gerar_jogos_quentes_frios(dezenas)
        st.session_state.jogos = jogos
        st.session_state.classificacao = classificacao
        st.session_state.nome_estrategia = "Quentes • Mornas • Frias"

    st.session_state.resultado_real = None
    st.session_state.resultado_ativo = False

# ================= RESULTADOS =================
if st.session_state.jogos:

    st.subheader("🎲 Jogos Gerados — 15 dezenas")

    st.markdown("""
    <span class="badge badge-quente">🔥 Quentes</span>
    <span class="badge badge-morna">🟠 Mornas</span>
    <span class="badge badge-fria">❄️ Frias</span>
    """, unsafe_allow_html=True)

    resultado_txt = st.text_input("📥 Resultado oficial (opcional)")
    if st.button("📌 Aplicar Resultado"):
        r = converter_lista(resultado_txt)
        if len(r) == 15:
            st.session_state.resultado_real = r
            st.session_state.resultado_ativo = True

    for i, jogo in enumerate(st.session_state.jogos, 1):
        st.markdown(f"### Jogo {i}")

        for linha in range(0, 15, 5):
            cols = st.columns(5)
            for c, n in zip(cols, jogo[linha:linha+5]):
                if n in st.session_state.classificacao["quentes"]:
                    classe = "quente"
                elif n in st.session_state.classificacao["frias"]:
                    classe = "fria"
                elif n in st.session_state.classificacao["mornas"]:
                    classe = "morna"
                else:
                    classe = "neutra"

                c.markdown(f"<div class='numero {classe}'>{n:02d}</div>", unsafe_allow_html=True)

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
