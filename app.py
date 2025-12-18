import streamlit.components.v1 as components

if not st.session_state.logado:

    components.html(
    """
    <html>
    <head>
    <style>
    body {
        margin: 0;
        padding: 0;
        background: transparent;
    }

    .card {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 90%;
        max-width: 420px;
        padding: 30px;
        border-radius: 26px;
        background: rgba(24,0,38,.78);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(168,85,247,.45);
        box-shadow: 0 0 120px rgba(168,85,247,.9);
        text-align: center;
        font-family: sans-serif;
    }

    input {
        width: 100%;
        padding: 14px;
        margin-top: 14px;
        border-radius: 12px;
        border: none;
        background: rgba(255,255,255,.08);
        color: white;
        font-size: 15px;
    }

    button {
        margin-top: 18px;
        width: 100%;
        padding: 14px;
        border-radius: 14px;
        border: none;
        font-weight: bold;
        font-size: 15px;
        background: linear-gradient(90deg,#7C3AED,#A855F7);
        color: white;
        cursor: pointer;
    }
    </style>
    </head>

    <body>
        <form method="post">
            <div class="card">
                <h2>🍀 Lotomilion Estrategista</h2>
                <p style="opacity:.85">
                    Inteligência estatística aplicada à Lotofácil<br>
                    <b>Acesso Premium</b>
                </p>

                <input name="email" placeholder="seu@email.com" />
                <button>Entrar no Painel Premium</button>

                <p style="font-size:12px;opacity:.6;margin-top:12px">
                    🔒 Sistema estatístico • Não garante premiação
                </p>
            </div>
        </form>
    </body>
    </html>
    """,
    height=0
    )

    # Captura do POST
    email = st.query_params.get("email")

    if email:
        ok, msg = verificar_usuario(email)
        if not ok:
            st.error(msg)
            st.stop()

        st.session_state.logado = True
        st.session_state.email = email
        st.rerun()

    st.stop()
