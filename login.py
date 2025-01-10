import streamlit as st
import streamlit_authenticator as stauth
from stdash import main

st.set_page_config(layout = 'wide')

# ✅ Copiar as credenciais para um dicionário completamente independente
credentials = {
    "usernames": {
        username: {
            "email": user["email"],
            "name": user["name"],
            "password": user["password"],
            "logged_in": user.get("logged_in", False)
        } for username, user in st.secrets["credentials"]["usernames"].items()
    }
}

cookie = {
    "expiry_days": st.secrets["cookie"]["expiry_days"],
    "key": st.secrets["cookie"]["key"],
    "name": st.secrets["cookie"]["name"]
}

# 🔐 Configuração do Autenticador
authenticator = stauth.Authenticate(
    credentials,
    cookie["name"],
    cookie["key"],
    cookie["expiry_days"]
)

# 🔒 Tela de login
authenticator.login()

# ✅ Verificação de autenticação
if st.session_state["authentication_status"]:
    main()  # Carrega o dashboard
    authenticator.logout()
elif st.session_state["authentication_status"] is False:
    st.error("Usuário/Senha inválido")
elif st.session_state["authentication_status"] is None:
    st.warning("Por favor, insira seu usuário e senha!")
