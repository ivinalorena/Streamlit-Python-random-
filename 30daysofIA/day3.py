import streamlit as st
import time
from snowflake.cortex import Complete

st.title(":material/airwave: Write Streams")

try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()
    
llm_models = ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"]
model = st.selectbox("Selecione um modelo", llm_models)

example_prompt = "O que é python?"
prompt=st.text_area("Insira um prompt: ", example_prompt)

streaming_method = st.radio(
    "Streaming method: ",
    ["Direct (stream=True)", "Custom Generator"],
    help="Choose how to stream the response"
)

if st.button("Gerar a resposta"):
    if streaming_method == "Direct(stream=True)":
        with st.spinner(f"Gerando resposta com {model}"):
            stream_generator = Complete(
                session=session,
                model=model,
                prompt=prompt,
                stream=True # stream=True: A abordagem mais simples. 
                #Indica ao Complete para retornar um gerador que produz tokens à medida que chegam.
            )
            st.write_stream(stream_generator)
    else:
        def custom_stream_generator():
            output=Complete(
                session=session,
                model=model,
                prompt=prompt
            )
            for chunk in output:
                yield chunk # gerador python faz um retorno incremental
                time.sleep(0.01)
                
        with st.spinner(f"Gerando resposta com {model}"):
            st.write_stream(custom_stream_generator)
            

            
st.divider()
st.caption("Day 3: Write streams 30 dias de IA")