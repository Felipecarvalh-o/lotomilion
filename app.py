import streamlit as st
import random

from data.lotofacil_historico import carregar_historico
from engine import gerar_fechamento_21_8, gerar_jogos_historico_real
from utils import converter_lista

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🍀",
    layout="wide"
)

# ======================================================
# SESSION STATE
# ======================================================

st.session_state.setdefault("modo", None)
st.session_state.setdefault("estrategia", None)
st.session_state.setdefault("jogos", [])
st.session_state.setdefault("resultado_real", [])
st.session_state.setdefault("comparar", False)
st.session_state.setdefault("nome_estrategia", None)

# PRO
st.session_state.setdefault("email_pro", None)
st.session_state.setdefault("pro_autenticado", False)

# ======================================================
# ESTILO
# ======================================================

st.markdown("""
<style>
header, footer { display: none; }

.numero {
    width:56px;height:56px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    font-weight:800;color:white;
    background: radial-gradient(circle at top, #A855F7, #6A1B9A);
}

.acerto {
    border:2px solid #00E676;
    box-shadow:0 0 18px rgba(0,230,118,.8);
}

.badge {
    background:#2A0934;
    padding:10px 16px;
    border-radius:16px;
    margin-bottom:12px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# HOME
# ======================================================

if st.session_state.modo is None:
    st.title("🍀 Lotomilion Estrategista")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 Modo Demonstração"):
            st.session_state.modo = "demo"
            st.rerun()
    with c2:
        if st.button("🔒 Sou PRO"):
            st.session_state.modo = "pro"
            st.rerun()

    st.stop()

# ======================================================
# AUTH PRO
# ======================================================

if st.session_state.modo == "pro" and not st.session_state.pro_autenticado:
    st.subheader("🔐 Acesso PRO")

    email = st.text_input("Email PRO")

    if st.button("Validar acesso"):
        emails_ativos = ["teste@pro.com", "admin@lotomilion.com"]

        if email in emails_ativos:
            st.session_state.email_pro = email
            st.session_state.pro_autenticado = True
            st.success("PRO liberado")
            st.rerun()
        else:
            st.error("Email não encontrado ou inativo")

    st.stop()

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("🍀 Lotomilion")

menu = st.sidebar.radio(
    "Menu",
    ["📊 Estratégias Avançadas", "🎯 Gerador Simples"]
)

# ======================================================
# BOTÃO FIXO — COMPARAR RESULTADO (SEMPRE VISÍVEL)
# ======================================================

st.markdown("### 📊 Resultado Oficial")

if st.button("📥 Comparar com resultado oficial"):
    historico = carregar_historico(qtd=1)

    if not historico:
        st.error("❌ Resultado oficial não encontrado")
    else:
        # garante compatibilidade
        resultado = historico[0]
        if isinstance(resultado, dict):
            resultado = resultado.get("dezenas", [])
        st.session_state.resultado_real = resultado
        st.session_state.comparar = True
        st.success("Resultado carregado")

st.divider()

# ======================================================
# ESTRATÉGIAS
# ======================================================

if menu == "📊 Estratégias Avançadas":

    if st.session_state.estrategia is None:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎯 Fechamento 21"):
                st.session_state.estrategia = "fechamento"
                st.session_state.nome_estrategia = "Fechamento 21"
                st.rerun()
        with c2:
            if st.button("📊 Histórico Real"):
                st.session_state.estrategia = "historico"
                st.session_state.nome_estrategia = "Histórico Real"
                st.rerun()

    else:
        st.markdown(f"<div class='badge'>📌 {st.session_state.nome_estrategia}</div>",
                    unsafe_allow_html=True)

        if st.button("🔁 Trocar Estratégia"):
            st.session_state.estrategia = None
            st.session_state.jogos = []
            st.rerun()

        # ================= FECHAMENTO =================
        if st.session_state.estrategia == "fechamento":

            fixas = st.text_area("🔒 9 fixas")
            variaveis = st.text_area("🔄 12 variáveis")

            if st.button("🧠 Gerar Jogos"):
                if st.session_state.modo == "demo" and len(st.session_state.jogos) >= 2:
                    st.error("Demo permite apenas 2 jogos")
                    st.stop()

                dezenas = sorted(set(converter_lista(fixas) + converter_lista(variaveis)))
                if len(dezenas) != 21:
                    st.error("Use exatamente 21 dezenas")
                    st.stop()

                jogos = gerar_fechamento_21_8(dezenas)
                st.session_state.jogos = [sorted(j[:15]) for j in jogos][:8]

        # ================= HISTÓRICO =================
        if st.session_state.estrategia == "historico":

            if st.button("🧠 Gerar Jogo"):
                historico = carregar_historico(qtd=50)
                base = list(range(1, 22))
                jogos, _ = gerar_jogos_historico_real(base, historico)
                st.session_state.jogos = [sorted(jogos[0][:15])]

    # ================= EXIBIÇÃO =================
    if st.session_state.jogos:
        limite = 2 if st.session_state.modo == "demo" else len(st.session_state.jogos)

        for jogo in st.session_state.jogos[:limite]:
            for i in range(0, 15, 5):
                cols = st.columns(5)
                for c, n in zip(cols, jogo[i:i+5]):
                    classe = "numero"
                    if st.session_state.comparar and n in st.session_state.resultado_real:
                        classe += " acerto"
                    c.markdown(f"<div class='{classe}'>{n:02d}</div>",
                               unsafe_allow_html=True)

# ======================================================
# GERADOR SIMPLES
# ======================================================

elif menu == "🎯 Gerador Simples":
    if st.button("Gerar jogo"):
        jogo = sorted(random.sample(range(1, 26), 15))
        for i in range(0, 15, 5):
            cols = st.columns(5)
            for c, n in zip(cols, jogo[i:i+5]):
                classe = "numero"
                if st.session_state.comparar and n in st.session_state.resultado_real:
                    classe += " acerto"
                c.markdown(f"<div class='{classe}'>{n:02d}</div>",
                           unsafe_allow_html=True)
