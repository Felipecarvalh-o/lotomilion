# ======================================================
# Lotomilion Estrategista — Login Premium (VERSÃO CERTA)
# ======================================================

import streamlit as st
import streamlit.components.v1 as components
from auth import verificar_usuario

st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🍀",
    layout="wide"
)

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.email = None

# ======================================================
# LOGIN EM HTML (SEM STREAMLIT UI)
# ======================================================

if not st.session_state.logado:

    components.html(
    """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    html, body {
        margin: 0;
        padding: 0;
        height: 100%;
        background:
            radial-gradient(circle at top, rgba(168,85,247,.35), transparent 55%),
            linear-gradient(180deg, #12001B, #050007);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        font-family: sans-serif;
    }

    .card {
        width: 100%;
        max-width: 420px;
        padding: 28px;
        border-radius: 26px;
        background: rgba(24,0,38,.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(168,85,247,.45);
        box-shadow: 0 0 140px rgba(168,85,247,.9);
        text-align: center;
        color: #fff;
    }

    h1 {
        font-size: 26px;
        margin-bottom: 6px;
    }

    p {
        font-size: 14px;
        opacity: .85;
        margin-bottom: 18px;
    }

    input {
        width: 100%;
        padding: 12px;
        border-radius: 10px;
        border: none;
        margin-bottom: 14px;
        background: rgba(255,255,255,.1);
        color: white;
        font-size: 14px;
    }

    button {
        width: 100%;
        padding: 12px;
        border-radius: 12px;
        border: none;
        background: linear-gradient(90deg,#7C3AED,#A855F7);
        color: white;
        font-weight: bold;
        font-size: 15px;
        cursor: pointer;
    }

    .caption {
        margin-top: 14px;
        font-size: 12px;
        opacity: .6;
    }
    </style>
    </head>

    <body>
        <form class="card" method="POST">
            <h1>🍀 Lotomilion Estrategista</h1>
            <p>Inteligência estatística aplicada à Lotofácil<br><b>Acesso Premium</b></p>
            <input name="email" placeholder="seu@email.com" />
            <button type="submit">Entrar no Painel Premium</button>
            <div class="caption">🔒 Sistema estatístico • Não garante premiação</div>
        </form>
    </body>
    </html>
    """,
    height=520
    )

    # captura do email
    email = st.experimental_get_query_params().get("email")
    if email:
        ok, msg = verificar_usuario(email[0])
        if ok:
            st.session_state.logado = True
            st.session_state.email = email[0]
            st.rerun()
        else:
            st.error(msg)

    st.stop()

# ======================================================
# APP PRINCIPAL
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Logado como {st.session_state.email}")
