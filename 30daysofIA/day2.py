""" For today's challenge, our goal is to run a large language model (LLM) directly within Snowflake. '
'We need to create a simple Streamlit interface that accepts a user's prompt, sends it to a Snowflake Cortex 
AI_COMPLETE function, and gets a response. Once that's done, we will display the AI's generated response back 
to the user in the app. 
Install prerequisite libraries
In forthcoming lessons we'll leverage Snowflake's Cortex AI and therefore please install the following prerequisite libraries:

> snowflake-ml-python==1.20.0
> snowflake-snowpark-python==1.44.0
    Or you could also run:
> pip install snowflake-ml-python==1.20.0 snowflake-snowpark-python==1.44.0
"""
import streamlit as st
from snowflake.snowpark.functions import ai_complete
import json

st.title(":material/smart_toy: Hello, Cortex!")

try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()
    
model = "claude-3-5-sonnet"
prompt=st.text_input("Insira seu prompt: ")

if st.button("Gerar resposta:"):
    df = session.range(1).select(
        ai_complete(model=model, prompt=prompt).alias("response")
    )
    response_raw = df.collect()[0][0]
    response = json.loads(response_raw)

    st.write(response)

st.divider()
st.caption("Day 2: Hello, Cortex! 30 dias de IA")