from data.lotofacil_historico import carregar_historico
from engine import (
    gerar_fechamento_21_8,
    gerar_jogos_historico_real,
    gerar_classificacao_simulada
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
    "mostrar_frequencia": False
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
    transition: all 0.4s ease;
}
.quente {background:#E53935;}
.morna {background:#FB8C00;}
.fria {background:#3949AB;}
.neutra {background:#7A1FA2;}

.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}
@keyframes fadeIn {
    from {opacity:0; transform:translateY(6px);}
    to {opacity:1; transform:translateY(0);}
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
.rank-box {
    padding:12px;
    border-radius:14px;
    background:#1f1f1f;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.caption("Ferramenta educacional e estatística • Sem vínculo com Loterias Caixa")

# ================= MENU =================
st.subheader("🧠 Passo 1 — Estratégia")

col1, col2 = st.columns(2)
with col1:
    if st.button("🎯 Fechamento 21", use_container_width=True):
        st.session_state.estrategia_escolhida = "Fechamento"
with col2:
    if st.button("📊 Histórico Real", use_container_width=True):
        st.session_state.estrategia_escolhida = "Historico"

# ================= PASSO 2 =================
st.subheader("🎯 Passo 2 — Base de 21 dezenas")
fixas_txt = st.text_area("🔒 9 dezenas FIXAS")
variaveis_txt = st.text_area("🔄 12 dezenas VARIÁVEIS")

# ================= RESULTADO =================
st.subheader("📥 Resultado Oficial (opcional)")
resultado_txt = st.text_input("Informe o resultado do sorteio (15 dezenas)")

if st.button("📊 Ativar Comparação"):
    resultado = converter_lista(resultado_txt)
    if len(resultado) == 15:
        st.session_state.resultado_real = resultado
        st.session_state.resultado_ativo = True
        st.success("Comparação ativada.")
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
        classificacao = gerar_classificacao_simulada(dezenas)
        nome = "Fechamento 21"
    else:
        historico = carregar_historico(qtd=50)
        jogos, classificacao = gerar_jogos_historico_real(dezenas, historico)
        nome = "Histórico Real"

    st.session_state.jogos = jogos
    st.session_state.classificacao = classificacao
    st.session_state.nome_estrategia = nome
    st.session_state.resultado_ativo = False

# ================= TOGGLE =================
if st.session_state.jogos:
    st.session_state.mostrar_frequencia = st.toggle(
        "🔄 Mostrar análise de frequência",
        value=st.session_state.mostrar_frequencia
    )

# ================= RESULTADOS =================
if st.session_state.jogos:

    st.subheader(f"🎲 Jogos Gerados — {st.session_state.nome_estrategia}")

    for i, jogo in enumerate(st.session_state.jogos, 1):

        st.markdown(f"### Jogo {i}")

        for linha in range(0, 15, 5):
            cols = st.columns(5)
            for c, n in zip(cols, jogo[linha:linha+5]):

                classe = "neutra"
                if (
                    st.session_state.resultado_ativo
                    and st.session_state.mostrar_frequencia
                ):
                    if n in st.session_state.classificacao["quentes"]:
                        classe = "quente"
                    elif n in st.session_state.classificacao["mornas"]:
                        classe = "morna"
                    elif n in st.session_state.classificacao["frias"]:
                        classe = "fria"

                c.markdown(
                    f"<div class='numero {classe} fade-in'>{n:02d}</div>",
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

    # ================= LEGENDA =================
    if st.session_state.mostrar_frequencia:
        st.markdown("### 📊 Legenda")
        st.markdown("""
- 🔴 **Quente**: maior incidência  
- 🟠 **Morna**: incidência média  
- 🔵 **Fria**: menor incidência
""")

    # ================= RANKING =================
    if st.session_state.resultado_ativo:
        st.markdown("### 🧠 Ranking das Dezenas")
        ranking = (
            st.session_state.classificacao["quentes"]
            + st.session_state.classificacao["mornas"]
            + st.session_state.classificacao["frias"]
        )

        st.markdown(
            "<div class='rank-box'>" +
            " • ".join(f"{n:02d}" for n in ranking) +
            "</div>",
            unsafe_allow_html=True
        )

# ================= AVISO FINAL =================
st.markdown("""
<div style="font-size:12px;color:#999;margin-top:26px">
Este aplicativo é educacional e estatístico.  
Não possui vínculo com a Caixa Econômica Federal.  
A Lotofácil é um jogo de azar e não há garantia de premiação.
</div>
""", unsafe_allow_html=True)
