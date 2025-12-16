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
for key, default in {
    "jogos": None,
    "classificacao": None,
    "nome_estrategia": None,
    "simulado": None,
    "resultado_real": None,
    "resultado_ativo": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

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

.bloco-jogo {
    margin-bottom:26px;
    padding-bottom:18px;
    border-bottom:1px solid #2a2a2a;
}

.badge {padding:4px 12px; border-radius:14px; font-size:12px; color:white;}
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
}
</style>
""", unsafe_allow_html=True)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.caption("Ferramenta educacional e estatística • Sem vínculo com Loterias Caixa")

# ================= PASSO 1 =================
st.subheader("🧠 Passo 1 — Estratégia")
estrategia = st.radio(
    "",
    ["🎯 Fechamento 21 (15 dezenas)", "🔥 Frequencial (15 dezenas)"],
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
    if len(dezenas) != 21:
        st.error("Não repita dezenas.")
        st.stop()

    if "Fechamento" in estrategia:
        st.session_state.jogos = gerar_fechamento_21_8(dezenas)
        st.session_state.classificacao = None
        st.session_state.nome_estrategia = "Fechamento 21"
    else:
        jogos, classificacao = gerar_jogos_quentes_frios(dezenas)
        quentes = classificacao["quentes"]
        frias = classificacao["frias"]
        mornas = [n for n in dezenas if n not in quentes and n not in frias]

        st.session_state.jogos = jogos
        st.session_state.classificacao = {
            "quentes": quentes,
            "mornas": mornas,
            "frias": frias
        }
        st.session_state.nome_estrategia = "Quentes e Frios"

    st.session_state.resultado_real = None
    st.session_state.resultado_ativo = False

# ================= RESULTADOS =================
if st.session_state.jogos:

    st.subheader("🎲 Passo 3 — Jogos (15 dezenas cada)")

    # ===== RESULTADO REAL =====
    st.subheader("📥 Resultado Oficial (opcional)")
    resultado_txt = st.text_input("Digite as 15 dezenas sorteadas")

    if st.button("📌 Aplicar Resultado"):
        resultado = converter_lista(resultado_txt)
        if len(resultado) == 15:
            st.session_state.resultado_real = resultado
            st.session_state.resultado_ativo = True
        else:
            st.warning("Informe exatamente 15 dezenas.")

    # ===== JOGOS =====
    for i, jogo in enumerate(st.session_state.jogos, 1):

        st.markdown(f"### Jogo {i} — 15 dezenas")

        for linha in range(0, 15, 5):
            cols = st.columns(5)
            for c, n in zip(cols, jogo[linha:linha+5]):

                classe = "neutra"
                if st.session_state.classificacao:
                    if n in st.session_state.classificacao["quentes"]:
                        classe = "quente"
                    elif n in st.session_state.classificacao["frias"]:
                        classe = "fria"
                    else:
                        classe = "morna"

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

        st.markdown("<div class='bloco-jogo'></div>", unsafe_allow_html=True)
