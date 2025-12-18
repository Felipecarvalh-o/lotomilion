# ======================================================
# Lotomilion Estrategista — Login Premium (FINAL ESTÁVEL)
# ======================================================

import streamlit as st
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
# FUNDO ANIMADO
# ======================================================

elementos = []

for _ in range(14):
    elementos.append(
        f"""
        <div class="float trevo"
             style="left:{random.randint(0,100)}%;
                    font-size:{random.choice([26,34,42])}px;
                    animation-duration:{random.randint(26,42)}s;">
            🍀
        </div>
        """
    )

for _ in range(12):
    elementos.append(
        f"""
        <div class="float numero"
             style="left:{random.randint(0,100)}%;
                    font-size:{random.choice([22,28,34])}px;
                    animation-duration:{random.randint(28,44)}s;">
            {random.choice(['01','03','05','07','10','13','15','18','21','25'])}
        </div>
        """
    )

st.markdown(f"""
<style>

/* RESET STREAMLIT */
html, body, [data-testid="stApp"] {{
    height: 100%;
}}

[data-testid="stAppViewContainer"] > .main {{
    padding: 0;
}}

header, footer {{
    display: none;
}}

/* FUNDO */
.login-bg {{
    position: fixed;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    background:
        radial-gradient(circle at top, rgba(168,85,247,.25), transparent 55%),
        linear-gradient(180deg, #12001B, #050007);
}}

.float {{
    position: absolute;
    bottom: -120px;
    opacity: 0.18;
    animation: subir linear infinite;
    pointer-events: none;
}}

@keyframes subir {{
    from {{ transform: translateY(0); }}
    to {{ transform: translateY(-160vh); }}
}}

.trevo {{
    color: #A855F7;
    text-shadow: 0 0 24px rgba(168,85,247,.8);
}}

.numero {{
    color: #22C55E;
    font-weight: 700;
    text-shadow: 0 0 18px rgba(34,197,94,.6);
}}

/* WRAPPER */
.login-wrapper {{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 5;
    padding: 12px;
}}

/* CARD */
.login-card {{
    width: 100%;
    max-width: 420px;
    padding: 26px;
    border-radius: 26px;
    background: rgba(24,0,38,.7);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(168,85,247,.45);
    box-shadow: 0 0 140px rgba(168,85,247,.9);
    text-align: center;
}}

/* TEXTO */
.login-title {{
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 6px;
}}

.login-sub {{
    font-size: 14px;
    opacity: .85;
    margin-bottom: 14px;
}}

/* INPUT */
div[data-testid="stTextInput"] input {{
    background: rgba(255,255,255,.08);
    border-radius: 10px;
}}

/* BOTÃO */
div[data-testid="stButton"] button {{
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    border: none;
    border-radius: 12px;
}}

/* CAPTION */
.login-caption {{
    margin-top: 12px;
    font-size: 12px;
    opacity: .6;
}}

</style>

<div class="login-bg">
    {''.join(elementos)}
</div>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logado:

    st.markdown("""
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-title">🍀 Lotomilion Estrategista</div>
            <div class="login-sub">
                Inteligência estatística aplicada à Lotofácil<br>
                <b>Acesso Premium</b>
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

    st.markdown("""
            <div class="login-caption">
                🔒 Sistema estatístico • Não garante premiação
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ======================================================
# APP PRINCIPAL
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Logado como {st.session_state.email}")
