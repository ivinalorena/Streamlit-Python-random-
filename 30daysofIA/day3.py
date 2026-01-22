""" 
documentação: https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql#complete

Write streams
For today's challenge, our goal is to run a Snowflake Cortex LLM using the snowflake.cortex.Complete Python API. '
'We need to build a Streamlit app that lets a user select a model, enter a prompt, and then stream the response back. '
'Once that's done, we will display the AI's response in real-time, word by word, as it's being generated. """
import streamlit as st
from snowflake.cortex import Complete
import time

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
    help="Escolha como mostrar a resposta"
)

if st.button("Gerar a resposta")
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

""" Por que o streaming é importante: Sem streaming, os usuários ficam olhando para uma tela em branco por vários 
segundos enquanto o LLM gera a resposta completa. Com streaming, eles veem as palavras aparecerem imediatamente, 
fazendo com que o aplicativo pareça mais rápido e responsivo, mesmo que o tempo total seja o mesmo. """