'''
Day 1 
connect to snowflake - the basics llm calls, streaming and caching
- For Day 1, our goal is to establish a connection between our Streamlit app and a Snowflake database. Once that's done, we'll run a simple query to confirm the connection is working and display the Snowflake version in the app.
'''
import streamlit as st 
import snowflake

st.title(":material/vpn_key: Day 1: Connect to Snowflake")

try:
    from snowflake.snowpark.context import get_activate_session
    session = get_activate_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()


version = session.sql("SELECT CURRENT_VERSION()").collect()[0][0]
st.sucess(f"sucesso na conexão, snowflake version: {version}")