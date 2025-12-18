# ======================================================
# Lotomilion Estrategista — App Premium
# ======================================================

from data.lotofacil_historico import carregar_historico
from engine import gerar_fechamento_21_8, gerar_historico_21_automatico
from simulador import simular_cenario
from utils import converter_lista
from auth import verificar_usuario

import streamlit as st

# ======================================================
# CONFIGURAÇÃO GLOBAL
# ======================================================

st.set_page_config(
    page_title="Lotomilion Estrategista",
    page_icon="🟣",
    layout="centered"
)

# ======================================================
# SESSION STATE — AUTH
# ======================================================

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.email = None

# ======================================================
# ESTILO GLOBAL — DESIGN SYSTEM
# ======================================================

st.markdown("""
<style>
:root {
    --bg: #050007;
    --card: #14001F;
    --card-2: #1F0030;
    --primary: #C026D3;
    --secondary: #7C3AED;
    --text: #EDE9FE;
    --muted: #A78BFA;
    --border: #2E1065;
    --success: #00E676;
}

html, body, [data-testid="stApp"] {
    background: radial-gradient(circle at top, #1B0A2A, var(--bg));
    color: var(--text);
}

.card {
    background: linear-gradient(160deg, var(--card), var(--card-2));
    border-radius: 26px;
    padding: 26px;
    border: 1px solid var(--border);
    box-shadow: 0 0 50px rgba(192,38,211,.25);
    margin-bottom: 24px;
}

.card-title {
    font-size: 22px;
    font-weight: 900;
    margin-bottom: 6px;
}

.card-sub {
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 18px;
}

.badge {
    background: #2A0934;
    padding: 10px 16px;
    border-radius: 16px;
    font-size: 14px;
    margin-bottom: 14px;
}

.numero {
    background: linear-gradient(145deg, var(--secondary), var(--primary));
    padding: 14px;
    border-radius: 18px;
    font-size: 16px;
    font-weight: 800;
    text-align: center;
    position: relative;
}

.acerto {
    outline: 3px solid var(--success);
    box-shadow: 0 0 18px rgba(0,230,118,.7);
}

.trofeu {
    position: absolute;
    top: -6px;
    right: -6px;
    font-size: 14px;
}

.footer {
    font-size: 12px;
    color: #888;
    text-align: center;
    margin-top: 24px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN PREMIUM
# ======================================================

if not st.session_state.logado:
    st.markdown("""
    <div class="card" style="max-width:420px;margin:12vh auto;text-align:center">
        <div class="card-title">🍀 Lotomilion Estrategista</div>
        <div class="card-sub">
            Inteligência estatística aplicada à Lotofácil<br>
            <b>Acesso exclusivo para membros</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("<div class='footer'>🔒 Sistema estatístico • Não garante premiação</div>", unsafe_allow_html=True)
    st.stop()

# ======================================================
# SESSION STATE — APP
# ======================================================

defaults = {
    "estrategia": None,
    "nome_estrategia": None,
    "jogos": None,
    "classificacao": None,
    "resultado_real": None,
    "comparacao_ativa": False,
    "resumo_simulacao": None
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ======================================================
# HEADER
# ======================================================

st.title("🟣 Lotomilion Estrategista")
st.caption(f"🔐 Acesso ativo • {st.session_state.email}")

# ======================================================
# ESCOLHA DE ESTRATÉGIA
# ======================================================

if not st.session_state.estrategia:
    st.markdown("""
    <div class="card">
        <div class="card-title">🎯 Escolha sua Estratégia</div>
        <div class="card-sub">Selecione o modelo estatístico desejado</div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("🎯 Fechamento 21", use_container_width=True):
            st.session_state.estrategia = "fechamento"
            st.session_state.nome_estrategia = "Fechamento 21"
            st.rerun()

    with c2:
        if st.button("📊 Histórico Inteligente", use_container_width=True):
            st.session_state.estrategia = "historico"
            st.session_state.nome_estrategia = "Histórico Real"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# ESTRATÉGIA ATIVA
# ======================================================

if st.session_state.estrategia:
    st.markdown(
        f"<div class='badge'>📌 Estratégia ativa: <b>{st.session_state.nome_estrategia}</b></div>",
        unsafe_allow_html=True
    )

    if st.button("🔄 Trocar estratégia"):
        for k in defaults:
            st.session_state[k] = defaults[k]
        st.rerun()

    # --------------------------------------------------
    # RESULTADO OFICIAL
    # --------------------------------------------------

    st.markdown("""
    <div class="card">
        <div class="card-title">📥 Resultado Oficial (opcional)</div>
        <div class="card-sub">Use para comparar o desempenho</div>
    """, unsafe_allow_html=True)

    resultado_txt = st.text_input(
        "Resultado",
        placeholder="01 02 03 04 ...",
        label_visibility="collapsed"
    )

    if st.button("Ativar Comparação"):
        resultado = converter_lista(resultado_txt)
        if len(resultado) == 15:
            st.session_state.resultado_real = resultado
            st.session_state.comparacao_ativa = True
            st.success("Comparação ativada")
        else:
            st.warning("Informe exatamente 15 dezenas.")

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # FECHAMENTO
    # --------------------------------------------------

    if st.session_state.estrategia == "fechamento":
        st.markdown("""
        <div class="card">
            <div class="card-title">🧩 Base de 21 dezenas</div>
            <div class="card-sub">Informe fixas e variáveis</div>
        """, unsafe_allow_html=True)

        fixas_txt = st.text_area("Fixas", placeholder="9 dezenas", label_visibility="collapsed")
        variaveis_txt = st.text_area("Variáveis", placeholder="12 dezenas", label_visibility="collapsed")

        if st.button("🧠 Gerar Jogos"):
            dezenas = sorted(set(converter_lista(fixas_txt) + converter_lista(variaveis_txt)))
            if len(dezenas) != 21:
                st.error("Use exatamente 21 dezenas.")
                st.stop()

            jogos = gerar_fechamento_21_8(dezenas)
            st.session_state.jogos = jogos
            st.session_state.resumo_simulacao = simular_cenario(jogos)

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # HISTÓRICO
    # --------------------------------------------------

    if st.session_state.estrategia == "historico":
        st.markdown("""
        <div class="card">
            <div class="card-title">📊 Análise Histórica</div>
            <div class="card-sub">Baseado nos últimos concursos</div>
        """, unsafe_allow_html=True)

        if st.button("🧠 Analisar histórico e gerar jogos"):
            historico = carregar_historico(qtd=50)
            jogos, classificacao = gerar_historico_21_automatico(historico)

            st.session_state.jogos = jogos
            st.session_state.classificacao = classificacao
            st.session_state.resumo_simulacao = simular_cenario(jogos)

        st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# PERFORMANCE
# ======================================================

if st.session_state.resumo_simulacao:
    r = st.session_state.resumo_simulacao

    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Performance Estatística</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("🎯 Média", r["media"])
    c2.metric("🏆 Máximo", r["maximo"])
    c3.metric("📉 Risco", r["desvio"])

    f1, f2, f3 = st.columns(3)
    f1.metric("11+", f"{r['freq_11']}%")
    f2.metric("12+", f"{r['freq_12']}%")
    f3.metric("13+", f"{r['freq_13']}%")

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# JOGOS GERADOS
# ======================================================

if st.session_state.jogos:
    st.markdown("""
    <div class="card">
        <div class="card-title">🎲 Jogos Gerados</div>
    """, unsafe_allow_html=True)

    for i, jogo in enumerate(st.session_state.jogos, 1):
        st.markdown(f"**Jogo {i}**")
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

    st.markdown("</div>", unsafe_allow_html=True)
