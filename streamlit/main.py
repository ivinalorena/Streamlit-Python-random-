import streamlit as st
import generateUsers

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.write("Por favor, faça login para continuar.")
        
    st.title("Sistema do Grupo de Pesquisa")
    #@st.cache_data(ddl = "1day")


    with st.form('Login'):
        username = st.text_input("Digite o nome de usuário:")
        senha = st.text_input("Digite a senha:", type="password")
        submit = st.form_submit_button(label = "Entrar",type="primary",use_container_width=True)
        google_submit = st.form_submit_button(label = "Entrar com Google",type="secondary", icon =':material/mail:', use_container_width=True)

    if submit:
        if generateUsers.validate_user(username,senha):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Bem-vindo, {username}!")
            st.write("Bem-vindo ao sistema do grupo de pesquisa!")
            st.write("Aqui você pode acessar as funcionalidades do sistema.")
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/S%C3%ADmbolo_da_UNILAB.png/1022px-S%C3%ADmbolo_da_UNILAB.png")
        else:
            st.error("Credenciais incorretas. Acesso negado.")
        """ if username == st.secrets["username"] and senha == st.secrets["password"]:
            st.success("Credenciais corretas. Acesso concedido.")
            st.write("Bem-vindo ao sistema do grupo de pesquisa!")
            st.write("Aqui você pode acessar as funcionalidades do sistema.")
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/S%C3%ADmbolo_da_UNILAB.png/1022px-S%C3%ADmbolo_da_UNILAB.png")
        else:
            st.error("Credenciais incorretas. Acesso negado.")
            st.stop() """