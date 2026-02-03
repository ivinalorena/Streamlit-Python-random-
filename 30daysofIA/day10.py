"""  Day 10
Your First Chatbot (with State)
For today's challenge, our goal is to combine everything we've learned about chat elements and session state 
to create a chatbot that remembers the conversation. We need to store messages in st.session_state and display 
them using st.chat_message. Once that's done, we will have a working chatbot that maintains conversation history 
across interactions. """

import streamlit as st
import json
from snowflake.snowpark.functions import ai_complete

try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

def call_llm(prompt_text: str) -> str:
    df = session.range(1).select(
        ai_complete(model="claude-3-5-sonnet", prompt=prompt_text).alias("response")
    )
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    if isinstance(response_json, dict):
        return response_json.get("choices", [{}])[0].get("messages", "")
    return str(response_json)

st.title(":material/chat: My First Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input("What would you like to know?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    

    with st.chat_message("user"):
        st.write(prompt)
    

    with st.chat_message("assistant"):
        response = call_llm(prompt)
        st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.caption("Day 10: Seu primeiro Chatbot (com State) | 30 Days of AI")