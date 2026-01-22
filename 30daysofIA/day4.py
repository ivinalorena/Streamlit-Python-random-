""" 
DAY 4: Caching your App
Armazenando seu aplicativo em cache
Para o desafio de hoje, nosso objetivo é criar um aplicativo web Streamlit que invoque um Modelo de Linguagem Grande (LLM) 
do Snowflake Cortex. Precisamos construir uma interface onde o usuário possa inserir uma solicitação, enviá-la para um modelo 
de IA poderoso (como o Claude 3.5 Sonnet) executado com segurança dentro do Snowflake e obter uma resposta. Assim que isso for 
concluído, exibiremos a resposta da IA ​​diretamente no aplicativo web, juntamente com a duração da solicitação. """

import streamlit as st
import time
import json
from snowflake.snowpark.functions import ai_complete

st.title(":material/cached: Caching your App")

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

prompt=st.text_input("Insira seu prompt", "Por que o céu é azul?")

if st.button("Submit"):
    temp_inicio = time.time()
    response = call_cortex_llm(prompt)
    temp_fim = time.time()

    st.success(f'tempo da call {temp_fim - temp_inicio: .2f} segundos')
    st.write(response)
    
st.divider()
st.caption("Day 4: Caching your App | 30 dias de IA")