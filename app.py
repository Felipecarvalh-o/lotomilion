from data.lotofacil_historico import carregar_historico
from engine import gerar_fechamento_21_8, gerar_historico_21_automatico
from simulador import simular_cenario
from utils import converter_lista
from auth import verificar_usuario

import streamlit as st

# ================= CONFIG =================
st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🟣",
    layout="centered"
)

# ================= LOGIN STATE =================
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.email = None

# ================= LOGIN PREMIUM =================
if not st.session_state.logado:
    st.markdown("""
    <style>
    body {
        background: radial-gradient(circle at top, #1B0A2A, #050007);
    }

    .login-bg {
        position: fixed;
        inset: 0;
        overflow: hidden;
        z-index: -1;
    }

    .float {
        position: absolute;
        font-size: 48px;
        opacity: 0.08;
        animation: float 18s infinite linear;
        color: #9C27B0;
    }

    @keyframes float {
        from { transform: translateY(110vh) rotate(0deg); }
        to { transform: translateY(-120vh) rotate(360deg); }
    }

    .login-box {
        background: linear-gradient(145deg, #14001F, #1F0030);
        padding: 34px;
        border-radius: 26px;
        border: 1px solid #3A0A52;
        max-width: 420px;
        margin: 12vh auto;
        text-align: center;
        box-shadow: 0 0 40px rgba(156,39,176,.35);
    }

    .login-title {
        font-size: 28px;
        font-weight: 900;
        color: #E1BEE7;
        margin-bottom: 6px;
        letter-spacing: .5px;
    }

    .login-sub {
        color: #B388EB;
        font-size: 14px;
        margin-bottom: 22px;
    }

    .login-foot {
        font-size: 12px;
        color: #888;
        margin-top: 16px;
    }
    </style>

    <div class="login-bg">
        <div class="float" style="left:10%">🍀</div>
        <div class="float" style="left:30%; animation-delay:2s;">07</div>
        <div class="float" style="left:50%; animation-delay:6s;">🍀</div>
        <div class="float" style="left:70%; animation-delay:4s;">13</div>
        <div class="float" style="left:85%; animation-delay:8s;">🍀</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-box">
        <div class="login-title">🍀 Lotomilion Estrategista</div>
        <div class="login-sub">
            Inteligência estatística aplicada à Lotofácil<br>
            <b>Acesso exclusivo para membros</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input("📧 Email usado na compra")

    if st.button("🔓 Acessar painel premium", use_container_width=True):
        ok, resultado = verificar_usuario(email)

        if not ok:
            st.error(resultado)
            st.stop()

        st.session_state.logado = True
        st.session_state.email = email
        st.rerun()

    st.markdown("<div class='login-foot'>🔒 Sistema estatístico • Não garante premiação</div>", unsafe_allow_html=True)
    st.stop()


# ================= SESSION STATE APP =================
defaults = {
    "estrategia": None,
    "jogos": None,
    "classificacao": None,
    "resultado_real": None,
    "comparacao_ativa": False,
    "nome_estrategia": None,
    "resumo_simulacao": None
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ================= ESTILO =================
st.markdown("""
<style>
.badge {
    background:#2A0934;
    padding:10px 16px;
    border-radius:16px;
    font-size:14px;
    margin-bottom:14px;
}
.numero {
    padding:14px;
    border-radius:16px;
    font-size:16px;
    font-weight:700;
    text-align:center;
    color:white;
    background:#6A1B9A;
    position:relative;
}
.acerto {
    border:2px solid #00E676;
    box-shadow:0 0 14px rgba(0,230,118,.8);
}
.trofeu {
    position:absolute;
    top:-6px;
    right:-6px;
    font-size:14px;
}
.painel {
    background:#0F0F0F;
    padding:20px;
    border-radius:18px;
    margin-top:20px;
    border:1px solid #2A0934;
}
</style>
""", unsafe_allow_html=True)

# ================= TOPO =================
st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Acesso ativo • {st.session_state.email}")

# ================= MENU =================
if not st.session_state.estrategia:
    st.subheader("🎯 Escolha a Estratégia")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎯 Fechamento 21", use_container_width=True):
            st.session_state.estrategia = "fechamento"
            st.session_state.nome_estrategia = "Fechamento 21"
            st.rerun()

    with c2:
        if st.button("📊 Histórico Real Automático", use_container_width=True):
            st.session_state.estrategia = "historico"
            st.session_state.nome_estrategia = "Histórico Real"
            st.rerun()

# ================= BADGE =================
if st.session_state.estrategia:
    st.markdown(
        f"<div class='badge'>📌 Estratégia ativa: <b>{st.session_state.nome_estrategia}</b></div>",
        unsafe_allow_html=True
    )

    if st.button("🔄 Trocar estratégia"):
        for k in defaults:
            st.session_state[k] = defaults[k]
        st.rerun()

    # ================= RESULTADO =================
    st.subheader("📥 Resultado Oficial (opcional)")
    resultado_txt = st.text_input("Resultado do sorteio (15 dezenas)")

    if st.button("📊 Ativar Comparação"):
        resultado = converter_lista(resultado_txt)
        if len(resultado) == 15:
            st.session_state.resultado_real = resultado
            st.session_state.comparacao_ativa = True
        else:
            st.warning("Informe exatamente 15 dezenas.")

    # ================= FECHAMENTO =================
    if st.session_state.estrategia == "fechamento":
        st.subheader("🧩 Base de 21 dezenas")
        fixas_txt = st.text_area("🔒 9 FIXAS")
        variaveis_txt = st.text_area("🔄 12 VARIÁVEIS")

        if st.button("🧠 Gerar Jogos"):
            dezenas = sorted(set(converter_lista(fixas_txt) + converter_lista(variaveis_txt)))
            if len(dezenas) != 21:
                st.error("Use exatamente 21 dezenas.")
                st.stop()

            jogos = gerar_fechamento_21_8(dezenas)
            st.session_state.jogos = jogos
            st.session_state.resumo_simulacao = simular_cenario(jogos)

    # ================= HISTÓRICO =================
    if st.session_state.estrategia == "historico":
        if st.button("🧠 Analisar histórico e gerar jogos"):
            historico = carregar_historico(qtd=50)
            jogos, classificacao = gerar_historico_21_automatico(historico)

            st.session_state.jogos = jogos
            st.session_state.classificacao = classificacao
            st.session_state.resumo_simulacao = simular_cenario(jogos)

# ================= PAINEL =================
if st.session_state.resumo_simulacao:
    r = st.session_state.resumo_simulacao
    st.markdown("<div class='painel'>", unsafe_allow_html=True)
    st.subheader("📊 Performance Estatística")

    c1, c2, c3 = st.columns(3)
    c1.metric("🎯 Média", r["media"])
    c2.metric("🏆 Máximo", r["maximo"])
    c3.metric("📉 Risco", r["desvio"])

    f1, f2, f3 = st.columns(3)
    f1.metric("11+", f"{r['freq_11']}%")
    f2.metric("12+", f"{r['freq_12']}%")
    f3.metric("13+", f"{r['freq_13']}%")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= JOGOS =================
if st.session_state.jogos:
    st.subheader("🎲 Jogos Gerados")

    for i, jogo in enumerate(st.session_state.jogos, 1):
        st.markdown(f"### Jogo {i}")
        cols = st.columns(5)

        for c, n in zip(cols * 3, jogo):
            acerto = (
                st.session_state.comparacao_ativa
                and n in (st.session_state.resultado_real or [])
            )
            c.markdown(
                f"""
                <div class="numero {'acerto' if acerto else ''}">
                    {n:02d}
                    <span class="trofeu">{'🏆' if acerto else ''}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.session_state.comparacao_ativa:
            pontos = len(set(jogo) & set(st.session_state.resultado_real))
            st.success(f"🎯 {pontos} pontos")

