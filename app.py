# ======================================================
# Lotomilion Estrategista — Login Premium FINAL (UX FIX)
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

for _ in range(28):
    elementos.append(
        f"""<div class="float trevo"
             style="left:{random.randint(0,100)}%;
                    font-size:{random.choice([40,54,70])}px;
                    animation-duration:{random.randint(28,44)}s;">
            🍀
        </div>"""
    )

for _ in range(20):
    elementos.append(
        f"""<div class="float numero {random.choice(['n1','n2','n3','n4'])}"
             style="left:{random.randint(0,100)}%;
                    font-size:{random.choice([30,38,46])}px;
                    animation-duration:{random.randint(30,48)}s;">
            {random.choice(['01','03','05','07','10','13','15','18','21','25'])}
        </div>"""
    )

st.markdown(f"""
<style>

/* RESET */
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
    pointer-events: none;
    background: radial-gradient(circle at top, #1B0A2A, #050007);
}}

.float {{
    position: absolute;
    bottom: -140px;
    opacity: 0.22;
    animation: subir linear infinite;
}}

@keyframes subir {{
    from {{ transform: translateY(0); }}
    to {{ transform: translateY(-170vh); }}
}}

.trevo {{
    color: #A855F7;
    text-shadow: 0 0 28px rgba(168,85,247,.9);
}}

.numero {{
    font-weight: 800;
    text-shadow: 0 0 18px rgba(255,255,255,.35);
}}

.n1 {{ color:#FACC15; }}
.n2 {{ color:#3B82F6; }}
.n3 {{ color:#22C55E; }}
.n4 {{ color:#EC4899; }}

/* LOGIN */
.login-wrapper {{
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 5;
}}

.login-card {{
    width: 100%;
    max-width: 420px;
    padding: 34px;
    border-radius: 26px;
    background: linear-gradient(160deg,#14001F,#1F0030);
    box-shadow: 0 0 100px rgba(168,85,247,.6);
    border: 1px solid #2E1065;
    text-align: center;
}}

.login-card input {{
    margin-top: 14px;
}}

.login-card button {{
    margin-top: 16px;
}}

.login-caption {{
    margin-top: 14px;
    font-size: 13px;
    opacity: .7;
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

    with st.container():
        st.markdown('<div class="login-wrapper"><div class="login-card">', unsafe_allow_html=True)

        st.markdown("""
            <h2>🍀 Lotomilion Estrategista</h2>
            <p style="opacity:.85;">
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

        st.markdown('<div class="login-caption">🔒 Sistema estatístico • Não garante premiação</div>', unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)
        st.stop()

# ======================================================
# APP
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Logado como {st.session_state.email}")
