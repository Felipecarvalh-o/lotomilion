import streamlit as st
import random
from auth import verificar_usuario

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🍀",
    layout="wide"
)

# ======================================================
# SESSION
# ======================================================

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.email = None

# ======================================================
# ESTILO
# ======================================================

st.markdown("""
<style>
header, footer { display: none; }

[data-testid="stApp"] {
    background: linear-gradient(180deg, #0B0B12, #050007);
}

.login-card {
    max-width: 460px;
    margin: 12vh auto;
    padding: 36px 32px;
    border-radius: 26px;
    background: linear-gradient(180deg, #1A002B, #0E0018);
    border: 1px solid rgba(168,85,247,.45);
    box-shadow: 0 0 120px rgba(168,85,247,.6);
    text-align: center;
}

.login-title {
    font-size: 28px;
    font-weight: 800;
}

.login-sub {
    font-size: 14px;
    opacity: .85;
    margin-bottom: 26px;
}

div[data-testid="stTextInput"] input {
    height: 48px;
    border-radius: 12px;
    background: rgba(255,255,255,.08);
}

div[data-testid="stButton"] button {
    height: 50px;
    border-radius: 14px;
    font-weight: 700;
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logado:

    st.markdown("""
    <div class="login-card">
        <div class="login-title">🍀 Lotomilion Estrategista</div>
        <div class="login-sub">
            Inteligência estatística aplicada à Lotofácil<br>
            <b>Acesso Premium</b>
        </div>
    """, unsafe_allow_html=True)

    email = st.text_input("", placeholder="seu@email.com", label_visibility="collapsed")

    if st.button("Entrar no Painel Premium", use_container_width=True):
        ok, msg = verificar_usuario(email)
        if not ok:
            st.error(msg)
            st.stop()

        st.session_state.logado = True
        st.session_state.email = email
        st.rerun()

    st.markdown("""
        <div style="margin-top:16px;font-size:12px;opacity:.6">
            🔒 Sistema estatístico • Não garante premiação
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ======================================================
# MENU LATERAL
# ======================================================

st.sidebar.title("🍀 Lotomilion")
st.sidebar.caption(st.session_state.email)

menu = st.sidebar.radio(
    "Menu",
    ["📊 Estratégia Lotofácil", "🎯 Gerador de Jogos", "ℹ️ Sobre"]
)

# ======================================================
# CONTEÚDO
# ======================================================

if menu == "📊 Estratégia Lotofácil":
    st.title("📊 Estratégia Lotofácil")

    st.markdown("""
    ### 🔥 Estratégia Base (Exemplo)

    - Trabalhar com **15 números**
    - Misturar:
        - 8 pares
        - 7 ímpares
    - Garantir:
        - 7 números entre 1–10
        - 8 números entre 11–25
    """)

    if st.button("Gerar Jogo Estratégico"):
        jogo = sorted(random.sample(range(1, 26), 15))
        st.success("🎯 Jogo gerado:")
        st.write(" ".join(f"{n:02d}" for n in jogo))

elif menu == "🎯 Gerador de Jogos":
    st.title("🎯 Gerador de Jogos")

    qtd = st.slider("Quantidade de jogos", 1, 10, 3)

    if st.button("Gerar"):
        for i in range(qtd):
            jogo = sorted(random.sample(range(1, 26), 15))
            st.write(f"Jogo {i+1}: ", " ".join(f"{n:02d}" for n in jogo))

elif menu == "ℹ️ Sobre":
    st.title("ℹ️ Sobre o Lotomilion")

    st.markdown("""
    **Lotomilion Estrategista** é um sistema de apoio estatístico  
    voltado para a Lotofácil.

    ⚠️ Não garante premiação.  
    📊 Baseado em padrões históricos e combinações.
    """)

