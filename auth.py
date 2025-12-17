from supabase import create_client
from datetime import date
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def verificar_usuario(email):
    resp = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .single()
        .execute()
    )

    if not resp.data:
        return False, "Usuário não encontrado"

    user = resp.data

    if user["status"] != "ativo":
        return False, "Assinatura inativa"

    if user["expira_em"]:
        if date.fromisoformat(user["expira_em"]) < date.today():
            return False, "Assinatura expirada"

    return True, user
