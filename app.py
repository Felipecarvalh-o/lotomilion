import streamlit as st
import random

from engine import gerar_fechamento_21_8, gerar_jogos_historico_real
from data.lotofacil_historico import carregar_historico
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

st.session_state.setdefault("autenticado", False)
st.session_state.setdefault("email", "")

st.session_state.setdefault("estrategia", None)
st.session_state.setdefault("nome_estrategia", None)
st.session_state.setdefault("jogos", [])

st.session_state.setdefault("resultado_oficial", [])
st.session_state.setdefault("comparar", False)

# ======================================================
# ESTILO PREMIUM
# ======================================================

st.markdown("""
<style>
header, footer { display:none; }

[data-testid="stApp"]{
    background:
    radial-gradient(circle at center, rgba(168,85,247,.25), transparent 55%),
    linear-gradient(180deg,#050007,#0B0B12);
}

.hero-wrapper{
    display:flex;
    justify-content:center;
    margin-top:18vh;
}

.hero{
    max-width:820px;
    padding:64px;
    text-align:center;
    border-radius:36px;
    background:linear-gradient(180deg,#2a0045,#12001f);
    box-shadow:0 40px 120px rgba(0,0,0,.8);
}

.hero h1{font-size:44px;font-weight:900;}
.hero p{opacity:.9;}

.numero{
    width:56px;height:56px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:800;
    color:white;
    background:radial-gradient(circle at top,#A855F7,#6A1B9A);
}

.acerto{
    border:2px solid #00E676;
    box-shadow:0 0 22px rgba(0,230,118,.9);
}

.trofeu{ margin-left:6px; }

.badge{
    background:#2A0934;
    padding:10px 16px;
    border-radius:16px;
    margin-bottom:12px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN (CORRIGIDO COM FORM)
# ======================================================

if not st.session_state.autenticado:
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero">
            <h1>🍀 Lotomilion Estrategista</h1>
            <p>Acesso inteligente para quem joga com estratégia</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("📧 Digite seu email")
        entrar = st.form_submit_button("🔓 Entrar")

    if entrar:
        if not email or "@" not in email:
            st.error("Digite um email válido")
        else:
            # 🔓 LIBERA QUALQUER EMAIL (BANCO ENTRA DEPOIS)
            st.session_state.autenticado = True
            st.session_state.email = email
            st.success("Acesso liberado")
            st.rerun()

    st.stop()

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("🍀 Lotomilion")
st.sidebar.caption(f"👤 {st.session_state.email}")

menu = st.sidebar.radio(
    "Menu",
    ["📊 Estratégias Avançadas", "🎯 Gerador Simples"]
)

# ======================================================
# COMPARAR SORTEIO OFICIAL (SEMPRE VISÍVEL)
# ======================================================

st.markdown("### 🏆 Comparar com Sorteio Oficial")

with st.form("resultado_form"):
    entrada = st.text_input("Digite as 15 dezenas do sorteio oficial")
    comparar = st.form_submit_button("📊 Aplicar Resultado")

if comparar:
    dezenas = converter_lista(entrada)
    if len(dezenas) != 15:
        st.error("Digite exatamente 15 dezenas")
    else:
        st.session_state.resultado_oficial = dezenas
        st.session_state.comparar = True
        st.success("Resultado aplicado")

st.divider()

# ======================================================
# ESTRATÉGIAS
# ======================================================

if menu == "📊 Estratégias Avançadas":

    if st.session_state.estrategia is None:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎯 Fechamento 21", use_container_width=True):
                st.session_state.estrategia = "fechamento"
                st.session_state.nome_estrategia = "Fechamento 21"
                st.rerun()
        with c2:
            if st.button("📊 Histórico Real", use_container_width=True):
                st.session_state.estrategia = "historico"
                st.session_state.nome_estrategia = "Histórico Real"
                st.rerun()

    else:
        st.markdown(
            f"<div class='badge'>📌 {st.session_state.nome_estrategia}</div>",
            unsafe_allow_html=True
        )

        if st.button("🔁 Trocar Estratégia"):
            st.session_state.estrategia = None
            st.session_state.jogos = []
            st.rerun()

        # ================= FECHAMENTO =================
        if st.session_state.estrategia == "fechamento":
            fixas = st.text_area("🔒 9 fixas")
            variaveis = st.text_area("🔄 12 variáveis")

            if st.button("🧠 Gerar Jogos"):
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
        for jogo in st.session_state.jogos:
            for i in range(0, 15, 5):
                cols = st.columns(5)
                for c, n in zip(cols, jogo[i:i+5]):
                    acerto = st.session_state.comparar and n in st.session_state.resultado_oficial
                    classe = "numero acerto" if acerto else "numero"
                    trofeu = "🏆" if acerto else ""
                    c.markdown(
                        f"<div class='{classe}'>{n:02d} {trofeu}</div>",
                        unsafe_allow_html=True
                    )

# ======================================================
# GERADOR SIMPLES
# ======================================================

elif menu == "🎯 Gerador Simples":
    if st.button("🎲 Gerar Jogo"):
        jogo = sorted(random.sample(range(1, 26), 15))
        for i in range(0, 15, 5):
            cols = st.columns(5)
            for c, n in zip(cols, jogo[i:i+5]):
                acerto = st.session_state.comparar and n in st.session_state.resultado_oficial
                classe = "numero acerto" if acerto else "numero"
                trofeu = "🏆" if acerto else ""
                c.markdown(
                    f"<div class='{classe}'>{n:02d} {trofeu}</div>",
                    unsafe_allow_html=True
                )
