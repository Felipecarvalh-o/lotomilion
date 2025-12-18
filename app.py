# ======================================================
# Lotomilion Estrategista — Login Premium (BELEZA FINAL)
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

for _ in range(22):
    elementos.append(
        f"""<div class="float trevo"
             style="left:{random.randint(0,100)}%;
                    font-size:{random.choice([36,48,60])}px;
                    animation-duration:{random.randint(30,48)}s;">
            🍀
        </div>"""
    )

for _ in range(16):
    elementos.append(
        f"""<div class="float numero {random.choice(['n1','n2','n3','n4'])}"
             style="left:{random.randint(0,100)}%;
                    font-size:{random.choice([28,36,42])}px;
                    animation-duration:{random.randint(32,50)}s;">
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
    background:
        radial-gradient(circle at top, rgba(168,85,247,.25), transparent 55%),
        linear-gradient(180deg, #12001B, #050007);
}}

.float {{
    position: absolute;
    bottom: -140px;
    opacity: 0.12;
    filter: blur(0.4px);
    animation: subir linear infinite;
}}

@keyframes subir {{
    from {{ transform: translateY(0); }}
    to {{ transform: translateY(-180vh); }}
}}

.trevo {{
    color: #A855F7;
}}

.numero {{
    font-weight: 700;
}}

.n1 {{ color:#FACC15; }}
.n2 {{ color:#3B82F6; }}
.n3 {{ color:#22C55E; }}
.n4 {{ color:#EC4899; }}

/* VINHETA */
.vignette {{
    position: fixed;
    inset: 0;
    z-index: 1;
    pointer-events: none;
    background: radial-gradient(circle, transparent 45%, rgba(0,0,0,.65));
}}

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
    padding: 38px;
    border-radius: 28px;
    background: rgba(20,0,31,.55);
    backdrop-filter: blur(14px);
    box-shadow:
        0 0 140px rgba(168,85,247,.85),
        inset 0 0 40px rgba(255,255,255,.05);
    border: 1px solid rgba(168,85,247,.35);
    text-align: center;
}}

.login-card h2 {{
    margin-bottom: 8px;
}}

.login-card p {{
    opacity: .9;
}}

.login-card input {{
    margin-top: 18px;
    background: rgba(255,255,255,.06);
}}

.login-card button {{
    margin-top: 18px;
    background: linear-gradient(90deg,#7C3AED,#A855F7);
    border: none;
}}

.login-card button:hover {{
    filter: brightness(1.1);
}}

.login-caption {{
    margin-top: 16px;
    font-size: 13px;
    opacity: .65;
}}

</style>

<div class="login-bg">
    {''.join(elementos)}
</div>
<div class="vignette"></div>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logado:

    st.markdown('<div class="login-wrapper"><div class="login-card">', unsafe_allow_html=True)

    st.markdown("""
        <h2>🍀 Lotomilion Estrategista</h2>
        <p>
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
