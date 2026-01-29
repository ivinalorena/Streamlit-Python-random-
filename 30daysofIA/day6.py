""" Day 6
Status UI for Long-Running Task
For today's challenge, our goal is to build a v2 of the "LinkedIn Post Generator" web app. Here, we'll integrate 
a Streamlit frontend with Snowflake's Cortex AI to generate text based on user-defined parameters. Particularly, 
    the tool drafts social media content using the Claude 3.5 Sonnet model. """

import streamlit as st
import time
import json
from snowflake.snowpark.functions import ai_complete

st.title(":material/post: LinkedIn Post Generator v2")

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

    with st.status("iniciando a engine...", expanded=True) as Status:
        st.write(":material/psychology: Thinking: Analyzing constraints and tone...")
        # regras pra llm
        prompt = f"""
        You are an expert social media manager. Generate a LinkedIn post based on the following:
    
        Tone: {tone}
        Desired Length: Approximately {word_count} words
        Use content from this URL: {content}
    
        Generate only the LinkedIn post text. Use dash for bullet points.
        """
        # chamando a api
        st.write(":material/flash_on: Generating: contacting Snowflake Cortex...")
        response = call_cortex_llm(prompt)
        
        # passo 3: Update Status to Complete
        st.write(":material/check_circle: Post generation completed!")
        Status.update(label="Post generated Sucessfuly!", state="complete", expanded=False)
    
    st.subheader("Generate post: ")
    st.markdown(response)
    
st.divider()
st.caption("Day 6: Status UI for Long-Running Task | 30 Days of AI")
    