# ======================================================
# Lotomilion Estrategista — Login Premium Fullscreen
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
    z-index: 10;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logado:

    # -------- ELEMENTOS DE FUNDO (FULLSCREEN) --------
    elementos = []

    # Trevos (mais quantidade)
    for _ in range(24):
        elementos.append(
            f"""
            <div class="float trevo"
                 style="
                    left:{random.randint(0,100)}%;
                    font-size:{random.choice([36,48,60,72,90])}px;
                    animation-delay:{random.randint(0,40)}s;
                    animation-duration:{random.randint(22,40)}s;">
                🍀
            </div>
            """
        )

    # Números
    for _ in range(18):
        elementos.append(
            f"""
            <div class="float numero {random.choice(['n1','n2','n3','n4'])}"
                 style="
                    left:{random.randint(0,100)}%;
                    font-size:{random.choice([32,40,48,56])}px;
                    animation-delay:{random.randint(0,45)}s;
                    animation-duration:{random.randint(26,44)}s;">
                {random.choice(['01','03','07','10','13','15','18','21','25'])}
            </div>
            """
        )

    components.html(
        f"""
        <style>
        .login-bg {{
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            z-index: 1;
            pointer-events: none;
            overflow: hidden;
        }}

        .float {{
            position: absolute;
            bottom: -120px;
            opacity: 0.18;
            animation-name: subir;
            animation-timing-function: linear;
            animation-iteration-count: infinite;
            filter: blur(0.3px);
        }}

        .trevo {{
            color: #A855F7;
            text-shadow: 0 0 28px rgba(168,85,247,.9);
        }}

        .numero {{
            font-weight: 800;
            text-shadow: 0 0 18px rgba(255,255,255,.25);
        }}

        .n1 {{ color:#FACC15; }}
        .n2 {{ color:#3B82F6; }}
        .n3 {{ color:#22C55E; }}
        .n4 {{ color:#EC4899; }}

        @keyframes subir {{
            from {{
                transform: translateY(0) rotate(0deg);
            }}
            to {{
                transform: translateY(-160vh) rotate(360deg);
            }}
        }}

        @media (max-width: 768px) {{
            .float {{
                opacity: 0.12;
                filter: blur(0.6px);
            }}
        }}
        </style>

        <div class="login-bg">
            {''.join(elementos)}
        </div>
        """,
        height=800
    )

    # -------- CARD LOGIN --------
    st.markdown("""
    <div style="
        max-width:420px;
        margin:8vh auto 0 auto;
        padding:34px;
        border-radius:28px;
        background:linear-gradient(160deg,#14001F,#1F0030);
        box-shadow:0 0 90px rgba(168,85,247,.45);
        border:1px solid #2E1065;
        text-align:center;
        position:relative;
        z-index:10;
    ">
        <h2 style="margin-bottom:6px;">🍀 Lotomilion Estrategista</h2>
        <p style="opacity:.85;">
            Inteligência estatística aplicada à Lotofácil<br>
            <b>Acesso Premium</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "",
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
# APP PRINCIPAL
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Logado como {st.session_state.email}")
