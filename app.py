# ======================================================
# Lotomilion Estrategista — Login Premium REAL
# ======================================================

import streamlit as st
import streamlit.components.v1 as components
import random

from auth import verificar_usuario

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🍀",
    layout="centered"
)

# ======================================================
# SESSION
# ======================================================

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.email = None

# ======================================================
# CSS GLOBAL
# ======================================================

st.markdown("""
<style>
[data-testid="stApp"] {
    background: radial-gradient(circle at top, #1B0A2A, #050007);
    color: #EDE9FE;
}

input, button {
    position: relative;
    z-index: 5;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logado:

    # -------- FUNDO ANIMADO (HTML REAL) --------
    elementos = []

    for _ in range(14):
        elementos.append(
            f"""
            <div class="float trevo"
                 style="
                    left:{random.randint(0,100)}%;
                    font-size:{random.choice([42,54,66,78])}px;
                    animation-delay:{random.randint(0,25)}s;">
                🍀
            </div>
            """
        )

    for _ in range(10):
        elementos.append(
            f"""
            <div class="float numero {random.choice(['n1','n2','n3','n4'])}"
                 style="
                    left:{random.randint(0,100)}%;
                    font-size:{random.choice([36,44,52])}px;
                    animation-delay:{random.randint(0,30)}s;">
                {random.choice(['07','10','13','18','21','25'])}
            </div>
            """
        )

    components.html(
        f"""
        <style>
        .login-bg {{
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }}

        .float {{
            position: absolute;
            bottom: -120px;
            opacity: 0.14;
            animation: subir 30s linear infinite;
            filter: blur(0.6px);
        }}

        .trevo {{
            color: #A855F7;
            text-shadow: 0 0 24px rgba(168,85,247,.8);
        }}

        .n1 {{ color:#FACC15; }}
        .n2 {{ color:#3B82F6; }}
        .n3 {{ color:#22C55E; }}
        .n4 {{ color:#EC4899; }}

        @keyframes subir {{
            from {{ transform: translateY(0) rotate(0deg); }}
            to {{ transform: translateY(-140vh) rotate(360deg); }}
        }}

        .card {{
            margin: 12vh auto;
            max-width: 420px;
            padding: 32px;
            border-radius: 26px;
            background: linear-gradient(160deg, #14001F, #1F0030);
            box-shadow: 0 0 70px rgba(168,85,247,.45);
            border: 1px solid #2E1065;
            text-align: center;
            position: relative;
            z-index: 3;
        }}
        </style>

        <div class="login-bg">
            {''.join(elementos)}
        </div>

        <div class="card">
            <h2>🍀 Lotomilion Estrategista</h2>
            <p>Inteligência estatística aplicada à Lotofácil<br>
            <b>Acesso Premium</b></p>
        </div>
        """,
        height=0
    )

    # -------- FORM --------
    email = st.text_input(
        "Email",
        placeholder="seu@email.com",
        label_visibility="collapsed"
    )

    if st.button("Entrar no Painel Premium", use_container_width=True):
        ok, msg = verificar_usuario(email)
        if not ok:
            st.error(msg)
            st.stop()

        st.session_state.logado = True
        st.session_state.email = email
        st.rerun()

    st.caption("🔒 Sistema estatístico • Não garante premiação")
    st.stop()

# ======================================================
# APP NORMAL
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Logado como {st.session_state.email}")
