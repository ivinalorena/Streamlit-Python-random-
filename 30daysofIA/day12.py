""" Day 12
Streaming Responses
Building on Day 11's foundation (conversation history and sidebar stats), today we're adding streaming responses 
to create a more dynamic and responsive chat experience. Instead of waiting for the complete response, users will 
see the AI's reply appear word-by-word in real-time, just like modern chat applications. """
import streamlit as st
import json
from snowflake.snowpark.functions import ai_complete
import time

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

st.title(":material/chat: Chatbot with Streaming")

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

    conversacao="\n\n".join([
        f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
        for msg in st.session_state.messages
    ])
    full_prompt = f"{conversacao}\n\nAssistant:"

    def stream_generator():
        response_text = call_llm(full_prompt)
        for word in response_text.split(" "):
            yield word + " "
            time.sleep(0.02)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = st.write_stream(stream_generator)

    st.session_state.messages.append({"role":"assistant","content": response})
    st.rerun()

st.divider()
st.caption("Day 12: Streaming Responses | 30 Days of AI")