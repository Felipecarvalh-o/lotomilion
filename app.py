from data.lotofacil_historico import carregar_historico
from engine import (
    gerar_fechamento_21_8,
    gerar_jogos_historico_real,
    gerar_jogos_quentes_frios
)

import streamlit as st
from streamlit.components.v1 import html
from utils import converter_lista

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
    "nome_estrategia": None,
    "resultado_real": None,
    "resultado_ativo": False,
    "estrategia_escolhida": "Fechamento",
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

.copy-btn {
    background:#9C27B0;
    color:white;
    padding:7px 18px;
    border-radius:20px;
    font-size:13px;
    border:none;
    cursor:pointer;
}

.tab-card {
    padding:14px;
    border-radius:16px;
    font-weight:700;
    text-align:center;
    cursor:pointer;
    background:#1f1f1f;
    border:2px solid transparent;
}
.tab-active {
    border-color:#9C27B0;
    background:#2a1f33;
}
</style>
""", unsafe_allow_html=True)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.caption("Ferramenta educacional e estatística • Sem vínculo com Loterias Caixa")

# ================= MENU MODERNO =================
st.subheader("🧠 Passo 1 — Estratégia")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎯 Fechamento 21", use_container_width=True):
        st.session_state.estrategia_escolhida = "Fechamento"

with col2:
    if st.button("📊 Histórico Real", use_container_width=True):
        st.session_state.estrategia_escolhida = "Historico"

if st.session_state.estrategia_escolhida == "Fechamento":
    st.info("🎯 **Fechamento 21** — Cobertura matemática com 8 jogos.")
else:
    st.info("📊 **Histórico Real** — Baseado em concursos reais da Lotofácil.")

# ================= PASSO 2 =================
st.subheader("🎯 Passo 2 — Base de 21 dezenas")
fixas_txt = st.text_area("🔒 9 dezenas FIXAS")
variaveis_txt = st.text_area("🔄 12 dezenas VARIÁVEIS")

# ================= RESULTADO GLOBAL =================
st.subheader("📥 Resultado Oficial (opcional)")
resultado_txt = st.text_input("Informe o resultado do sorteio (15 dezenas)")
if st.button("📊 Ativar Comparação"):
    resultado = converter_lista(resultado_txt)
    if len(resultado) == 15:
        st.session_state.resultado_real = resultado
        st.session_state.resultado_ativo = True
        st.success("Resultado ativado para comparação.")
    else:
        st.warning("Informe exatamente 15 dezenas.")

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

    if st.session_state.estrategia_escolhida == "Fechamento":
        jogos = gerar_fechamento_21_8(dezenas)

        # classificação interna (frequência invisível)
        _, classificacao = gerar_jogos_quentes_frios(dezenas)

        st.session_state.jogos = jogos
        st.session_state.classificacao = classificacao
        st.session_state.nome_estrategia = "Fechamento 21"

    else:
        historico = carregar_historico(qtd=50)
        jogos, classificacao = gerar_jogos_historico_real(dezenas, historico)

        st.session_state.jogos = jogos
        st.session_state.classificacao = classificacao
        st.session_state.nome_estrategia = "Histórico Real"

# ================= RESULTADOS =================
if st.session_state.jogos:

    st.subheader(f"🎲 Jogos Gerados — {st.session_state.nome_estrategia}")

    for i, jogo in enumerate(st.session_state.jogos, 1):

        st.markdown(f"### Jogo {i}")

        for linha in range(0, 15, 5):
            cols = st.columns(5)
            for c, n in zip(cols, jogo[linha:linha+5]):

                classe = "neutra"
                if st.session_state.classificacao:
                    if n in st.session_state.classificacao.get("quentes", []):
                        classe = "quente"
                    elif n in st.session_state.classificacao.get("mornas", []):
                        classe = "morna"
                    elif n in st.session_state.classificacao.get("frias", []):
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

        st.markdown("<div class='bloco-jogo'></div>", unsafe_allow_html=True)

# ================= AVISO FINAL =================
st.markdown("""
<div style="font-size:12px;color:#999;margin-top:26px">
Este aplicativo é educacional e estatístico.  
Não possui vínculo com a Caixa Econômica Federal.  
A Lotofácil é um jogo de azar e não há garantia de premiação.
</div>
""", unsafe_allow_html=True)
