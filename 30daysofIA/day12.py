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

st.divider()
st.caption("Day 12: Streaming Responses | 30 Days of AI")