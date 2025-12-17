from supabase import create_client
from datetime import date
import streamlit as st

# ================= CONFIG SUPABASE =================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= AUTENTICAÇÃO =================
def verificar_usuario(email: str):
    """
    Verifica se o usuário existe, está ativo
    e se a assinatura não está expirada.
    Retorna (True, mensagem) ou (False, erro)
    """

    try:
        resp = (
            supabase
            .table("users")
            .select("email, status, expira_em")
            .eq("email", email.lower().strip())
            .limit(1)
            .execute()
        )
    except Exception:
        return False, "Erro ao conectar com o servidor"

    if not resp.data or len(resp.data) == 0:
        return False, "Email não encontrado. Use o email da compra."

    user = resp.data[0]

    # Status da assinatura
    if user.get("status") != "ativo":
        return False, "Assinatura inativa ou cancelada"

    # Validação de expiração (se existir)
    expira_em = user.get("expira_em")
    if expira_em:
        try:
            if date.fromisoformat(expira_em) < date.today():
                return False, "Assinatura expirada"
        except Exception:
            return False, "Erro ao validar data da assinatura"

    return True, "Acesso liberado"
