""" Day 8
Meet the Chat Elements
Welcome to Week 2! Let's reflect on what we've learned so far.

In Week 1, you built linear apps: Input → Process → Output. Now we'll learn to use chat elements to build a chatbot. 
This is where Streamlit really shines, but it requires the app to eventually "remember" context.

For today's challenge, our goal is to focus purely on the chat user interface (UI). Here, we'll render a visual chat 
conversation using chat elements before we worry about memory or API calls. Once that's done, we'll have the visual 
skeleton of a chatbot. Although it won't be a full functional chatbot but it's a great start towards that path. """

import streamlit as st

st.title(":material/chat: Meet the Chat Elements")

with st.chat_message("user"):
    st.write("Oi! você consegue explicar o que o streamlit é?")

with st.chat_message("assistant"):
    st.write("Streamlit is an open-source Python framework for building data apps.")
    st.bar_chart([10,20,30,40])

prompt = st.chat_input("Insira sua mensagem aqui...")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        st.write(f"Você acabou de dizer:\n\n '{prompt}' \n\n(eu não tenho memória ainda!)")

st.divider()
st.caption("Day 8: Meet the Chat Elements | 30 Days of AI")