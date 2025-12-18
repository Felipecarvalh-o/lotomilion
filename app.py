# ======================================================
# Lotomilion Estrategista — Login Premium FINAL
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
html, body, [data-testid="stApp"] {
    height: 100%;
}

[data-testid="stAppViewContainer"] > .main {
    padding: 0;
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

    # -------- FUNDO ANIMADO FIXO --------
    elementos = []

    for _ in range(26):
        elementos.append(
            f"""<div class="float trevo"
                 style="left:{random.randint(0,100)}%;
                        font-size:{random.choice([32,44,56,68])}px;
                        animation-duration:{random.randint(22,36)}s;">
                🍀
            </div>"""
        )

    for _ in range(18):
        elementos.append(
            f"""<div class="float numero {random.choice(['n1','n2','n3','n4'])}"
                 style="left:{random.randint(0,100)}%;
                        font-size:{random.choice([28,36,44])}px;
                        animation-duration:{random.randint(24,38)}s;">
                {random.choice(['01','03','07','10','13','15','18','21','25'])}
            </div>"""
        )

    components.html(
        f"""
        <style>
        .login-bg {{
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            z-index: 0;
            pointer-events: none;
            background: radial-gradient(circle at top, #1B0A2A, #050007);
        }}

        .float {{
            position: absolute;
            bottom: -120px;
            opacity: 0.18;
            animation-name: subir;
            animation-timing-function: linear;
            animation-iteration-count: infinite;
        }}

        .trevo {{
            color: #A855F7;
            text-shadow: 0 0 26px rgba(168,85,247,.9);
        }}

        .numero {{
            font-weight: 800;
            text-shadow: 0 0 16px rgba(255,255,255,.25);
        }}

        .n1 {{ color:#FACC15; }}
        .n2 {{ color:#3B82F6; }}
        .n3 {{ color:#22C55E; }}
        .n4 {{ color:#EC4899; }}

        @keyframes subir {{
            from {{ transform: translateY(0); }}
            to {{ transform: translateY(-160vh); }}
        }}
        </style>

        <div class="login-bg">
            {''.join(elementos)}
        </div>
        """,
        height=0
    )

    # -------- LOGIN CENTRAL --------
    st.markdown("""
    <div style="
        min-height:100vh;
        display:flex;
        align-items:center;
        justify-content:center;
        position:relative;
        z-index:5;
    ">
        <div style="
            width:100%;
            max-width:420px;
            padding:36px;
            border-radius:26px;
            background:linear-gradient(160deg,#14001F,#1F0030);
            box-shadow:0 0 100px rgba(168,85,247,.55);
            border:1px solid #2E1065;
            text-align:center;
        ">
            <h2>🍀 Lotomilion Estrategista</h2>
            <p style="opacity:.85;margin-bottom:20px;">
                Inteligência estatística aplicada à Lotofácil<br>
                <b>Acesso Premium</b>
            </p>
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

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# ======================================================
# APP PRINCIPAL
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Logado como {st.session_state.email}")
