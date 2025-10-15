import streamlit as st

st.title("Sistema do Grupo de Pesquisa")

senha = st.text_input("Digite a senha:", type="password")


if senha != st.secrets["app_password"]:
    st.warning("Senha incorreta. Acesso negado.")
    st.stop()

st.success("Senha correta. Acesso concedido.")
st.write("Bem-vindo ao sistema do grupo de pesquisa!")
st.write("Aqui você pode acessar as funcionalidades do sistema.")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/S%C3%ADmbolo_da_UNILAB.png/1022px-S%C3%ADmbolo_da_UNILAB.png")