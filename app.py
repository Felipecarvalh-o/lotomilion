# ======================================================
# Lotomilion Estrategista — Login Premium (FINAL ESTÁVEL)
# ======================================================

import streamlit as st
import random
import streamlit.components.v1 as components
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
# FUNDO ANIMADO (ISOLADO — SEM BUG)
# ======================================================

elementos = ""

for _ in range(14):
    elementos += f"""
    <div class="float trevo"
         style="left:{random.randint(0,100)}%;
                font-size:{random.choice([26,34,42])}px;
                animation-duration:{random.randint(28,44)}s;">
        🍀
    </div>
    """

for _ in range(12):
    elementos += f"""
    <div class="float numero"
         style="left:{random.randint(0,100)}%;
                font-size:{random.choice([22,28,34])}px;
                animation-duration:{random.randint(30,46)}s;">
        {random.choice(['01','03','05','07','10','13','15','18','21','25'])}
    </div>
    """

components.html(
f"""
<!DOCTYPE html>
<html>
<head>
<style>
html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
}}

.bg {{
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at top, rgba(168,85,247,.25), transparent 55%),
        linear-gradient(180deg, #12001B, #050007);
    overflow: hidden;
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
    text-shadow: 0 0 24px rgba(168,85,247,.9);
}}

.numero {{
    color: #22C55E;
    font-weight: 700;
    text-shadow: 0 0 18px rgba(34,197,94,.7);
}}
</style>
</head>
<body>
<div class="bg">
    {elementos}
</div>
</body>
</html>
""",
height=0,
)

# ======================================================
# LOGIN (STREAMLIT PURO — SEM HTML QUEBRADO)
# ======================================================

if not st.session_state.logado:

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    with st.container():
        st.markdown("## 🍀 Lotomilion Estrategista")
        st.caption("Inteligência estatística aplicada à Lotofácil — **Acesso Premium**")

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
