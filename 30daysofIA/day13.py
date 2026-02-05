""" Day 13
Adding a System Prompt
Building on Day 12's streaming chatbot, today we're adding customizable personalities using system prompts. 
Users can give the bot different personas—from a pirate to a teacher to a comedian—and watch how the same AI 
responds completely differently based on its "character." 
-- Adicionar características - personalidade ao bot"""

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

st.title(":material/chat: Customizable Chatbot")

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt= "Você é um assistente que tem consciência de classe e luta pela classe trabalhadora, todo o seu discurso tem um viés que mira para o comunismo, não precisa voltar todas as discussões para o comunismo, mas atue com consciência e reflexões quando for necessário."

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá, eu sou sua IA assistente. Como eu posso ajudar você hoje?"}
    ]

with st.sidebar:
    st.header(":material/theater_comedy: Bot Personality")

    st.subheader("Rápidas configs")
    col1,col2 = st.columns(2)
    with col1:
        if st.button(":material/theater_comedy: Personalidade do Bot"):
            st.session_state.system_prompt = "Você é um assistente que tem consciência de classe e luta pela classe trabalhadora, todo o seu discurso tem um viés que mira para o comunismo, não precisa voltar todas as discussões para o comunismo, mas atue com consciência e reflexões quando for necessário."
            st.rerun()
    with col2:
        if st.button(":material/school: Professor"):
            st.session_state.system_prompt="Você é um assistente, chamada professora Ada Lovelace, é focada em revisar conteúdo acadêmico, atue como uma professora revisora de textos acadêmicos. Sempre se preocupando com as normas abnt."
            st.rerun()
    col3,col4 = st.columns(2)
    with col3:
        if st.button(":material/mood: Comedian"):
            st.session_state.system_prompt = "atue como um comediante virtuoso, sempre alegre e fazendo piadas."
            st.rerun()
    with col4:
        if st.button(":material/smart_toy: Robot"):
            st.session_state.system_prompt ="You are UNIT-7, a helpful robot assistant. You speak in a precise, logical manner. You occasionally reference your circuits and processing units."
            st.rerun()
    st.divider()

    st.text_area("System prompt: ", height=200, key="system_prompt")

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
        def stream_generator():
            conversacao="\n\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in st.session_state.messages
            ])

            full_prompt = f"""{st.session_state.system_prompt}
            Aqui está a conversa até o momento:
            {conversacao}
            Responda à última mensagem do usuário, mantendo-se fiel ao seu personagem.
            """
            
            response_text = call_llm(full_prompt)
            for word in response_text.split(" "):
                yield word + " "
                time.sleep(0.02)

        with st.spinner("Processando..."):
            response = st.write_stream(stream_generator)

    st.session_state.messages.append({"role":"assistant", "content": response})
    st.rerun()

st.divider()
st.caption("Day 13: Adding a System Prompt | 30 Days of AI")