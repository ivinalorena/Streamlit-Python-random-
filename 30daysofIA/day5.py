import streamlit as st
import time
import json
from snowflake.snowpark.functions import ai_complete

st.title(":material/post: LinkedIn Post Generator")

try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

@st.cache_data
def call_cortex_llm(prompt_text):
    model = 'claude-3-5-sonnet'
    df = session.range(1).select(
        ai_complete(model=model,
                   prompt=prompt_text).alias("response")
    )

    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    return response_json

#prompt=st.text_input("Insira seu prompt", "Por que o céu é azul?")

content = st.text_input("Content URL", "https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql")
tone = st.selectbox("Tons: ", ["Profissional", "Casual", "Engraçado"])
word_count = st.slider("Aproximadamente a contagem de palavras: ", 50,100,200)

if st.button("Generate Post"):
    # regras pra llm
    prompt = f"""
    You are an expert social media manager. Generate a LinkedIn post based on the following:

    Tone: {tone}
    Desired Length: Approximately {word_count} words
    Use content from this URL: {content}

    Generate only the LinkedIn post text. Use dash for bullet points.
    """
    response = call_cortex_llm(prompt)
    st.subheader("Generate post: ")
    st.markdown(response)