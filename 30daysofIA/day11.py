""" Day 11
Displaying Chat History
For today's challenge, our goal is to enhance our chatbot with better history management. We need to add a welcome message, '
'display conversation statistics in the sidebar, and provide a way to clear the chat history. Once that's done, we will have 
a more polished chatbot experience with visible conversation tracking.

Note: We also add st.rerun() after the assistant's response to ensure the sidebar stats update immediately. """
import streamlit as st
import json
from snowflake.snowpark.functions import ai_complete

try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

def call_llm(prompt_text:str)->str:
    df=session.range(1).select(
         ai_complete(model="claude-3-5-sonnet", 
        prompt=prompt_text).alias("response")
    )
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)

    if isinstance(response_json, dict):
        return response_json.get("choices", [{}])[0].get("messages","")
    return str(response_json)

st.title(":material/chat: Chatbot com histórico")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá, eu sou sua IA assistente. Como eu posso ajudar você hoje?"}
    ]

with st.sidebar:
    st.header("Conversation Stats")
    user_msgs = len([m for m in st.session_state.messages if m["role"]== "user"])
    assistant_msgs = len([m for m in st.session_state.messages if m["role"]== "assistant"])

    st.metric("Suas mensagens", user_msgs)
    st.metric("IA respostas", assistant_msgs)

    if st.button("Limpar histórico"):
        st.session_state.messages = [
        {"role": "assistant", "content": "Olá, eu sou sua IA assistente. Como eu posso ajudar você hoje?"}
        ]
        st.rerun()
        
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("O que você gostaria de saber?"):
    st.session_state.messages.append({"role":"user", "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            conversacao="\n\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in st.session_state.messages
            ])
            full_prompt = f"{conversacao}\n\nAssistant:"

            response = call_llm(full_prompt)
        st.markdown(response)

    st.session_state.messages.append({"role":"assistant","content": response})
    st.rerun()
    
st.divider()
st.caption("Day 11: Displaying Chat History | 30 Days of AI")