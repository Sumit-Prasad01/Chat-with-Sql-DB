import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.callbacks import StreamlitCallbackHandler
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
import sqlite3

st.set_page_config(page_title="LangChain : Chat with SQL DB", page_icon="🦜")
st.title("🦜LangChain : Chat with SQL DB")


LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"
POSTGRES = "USE_POSTGRES"

radio_opt = ["Use SQLite3 Database - Student.db","Connect to your MySQL Database","Connect to your Postgres Sql Database"]

selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat",options = radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL user")
    mysql_password = st.sidebar.text_input("MySQL Password",type = "password")
    mysql_db = st.sidebar.text_input("MySQL Database")

elif radio_opt.index(selected_opt) == 2:
    db_uri = POSTGRES  
    pg_host = st.sidebar.text_input("PostgreSQL Host")
    pg_user = st.sidebar.text_input("PostgreSQL User")
    pg_password = st.sidebar.text_input("PostgreSQL Password", type="password")
    pg_db = st.sidebar.text_input("PostgreSQL Database")

else:
    db_uri = LOCALDB


api_key = st.sidebar.text_input(label="Groq Api Key", type = "password")

if not db_uri:
    st.info("Please enter the database information and uri.")
if not api_key:
    st.info("Please enter the Groq api key.")

ChatGroq(groq_api_key=api_key, model_name = "Llama3-8b-8192", streaming = True)

@st.cache_resource(ttl='2h')
def configure_db(db_uri,host = None,user = None, password = None,db = None):
    try:
        if db_uri == LOCALDB:
            db_file_path = (Path(__file__).parent/"student.db").absolute()
            creator = lambda : sqlite3.coonect(f"file:{db_file_path}?mode=ro",uri = True)
            return SQLDatabase(create_engine("sqlite:///", creator = creator))
        
        elif db_uri == MYSQL:
            if not (host and user and password and db):
                st.error("Please provide all MySQL connection details.")
                st.stop()
            return SQLDatabase(create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db}"))
        elif db_uri == POSTGRES:
            if not (host and user and password and db):
                st.error("Please provide all PostgreSQL connection details.")
                st.stop()
            return SQLDatabase(create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:5432/{db}"))
 
    except Exception as e:
        st.error(f"Failed to connect to Database: {e}")
        st.stop()

if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)

elif db_uri == POSTGRES:
    db = configure_db(db_uri, pg_host, pg_user, pg_password, pg_db)

else: 
    configure_db(db_uri)