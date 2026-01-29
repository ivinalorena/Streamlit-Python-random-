"""  
Day 7
Theming and Layout
For today's challenge, we're building upon the app from Day 6 but this time we'll focus on theming and layout. 
We need to transform the standard functional interface into a polished, branded experience using Streamlit's '
'configuration and layout tools. Once that's done, we will have a "Dark Mode" app with a clean sidebar navigation 
and custom color, creating a more professional look and feel. """

import streamlit as st
import time
import json
from snowflake.snowpark.functions import ai_complete

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

st.subheader(":material/input: Input content")

with st.sidebar:
    st.title(":material/post: LinkedIn Post Generator v3")
    st.success("Um app para gerar posts do linkedin utilizando conteúdos URL") 
    tone = st.selectbox("Tons: ", ["Profissional", "Casual", "Engraçado"])
    word_count = st.slider("Aproximadamente a contagem de palavras: ", 50,100,200)


content = st.text_input("Content URL", "https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql")

if st.button("Generate Post"):

    with st.status("iniciando a engine...", expanded=True) as Status:
        st.write(":material/psychology: Thinking: Analyzing constraints and tone...")
        
        time.sleep(2)
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
        time.sleep(2)
        response = call_cortex_llm(prompt)
        
        # passo 3: Update Status to Complete
        st.write(":material/check_circle: Post generation completed!")
        Status.update(label="Post generated Sucessfuly!", state="complete", expanded=False)
   
    with st.container(border=True):
        st.subheader("Generate post: ")
        st.markdown(response)
    
st.divider()
st.caption("Day 6: Status UI for Long-Running Task | 30 Days of AI")
    