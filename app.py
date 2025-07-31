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
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class DatabaseConfig:
    """Configuration class for database types"""
    LOCALDB = "USE_LOCALDB"
    MYSQL = "USE_MYSQL"
    POSTGRES = "USE_POSTGRES"


class DatabaseConnection(ABC):
    """Abstract base class for database connections"""
    
    @abstractmethod
    def create_connection(self) -> SQLDatabase:
        """Create and return a database connection"""
        pass
    
    @abstractmethod
    def validate_credentials(self) -> bool:
        """Validate database credentials"""
        pass


class SQLiteConnection(DatabaseConnection):
    """SQLite database connection handler"""
    
    def __init__(self, db_file_path: Optional[Path] = None):
        self.db_file_path = db_file_path or (Path(__file__).parent / "student.db").absolute()
    
    def create_connection(self) -> SQLDatabase:
        """Create SQLite connection"""
        try:
            creator = lambda: sqlite3.connect(f"file:{self.db_file_path}?mode=ro", uri=True)
            return SQLDatabase(create_engine("sqlite:///", creator=creator))
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SQLite database: {e}")
    
    def validate_credentials(self) -> bool:
        """SQLite doesn't require credentials validation"""
        return True


class MySQLConnection(DatabaseConnection):
    """MySQL database connection handler"""
    
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    def create_connection(self) -> SQLDatabase:
        """Create MySQL connection"""
        try:
            connection_string = f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}"
            return SQLDatabase(create_engine(connection_string))
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MySQL database: {e}")
    
    def validate_credentials(self) -> bool:
        """Validate MySQL credentials"""
        return all([self.host, self.user, self.password, self.database])


class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL database connection handler"""
    
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    def create_connection(self) -> SQLDatabase:
        """Create PostgreSQL connection"""
        try:
            connection_string = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}/{self.database}"
            return SQLDatabase(create_engine(connection_string))
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL database: {e}")
    
    def validate_credentials(self) -> bool:
        """Validate PostgreSQL credentials"""
        return all([self.host, self.user, self.password, self.database])


class DatabaseFactory:
    """Factory class for creating database connections"""
    
    @staticmethod
    def create_connection(db_type: str, **kwargs) -> DatabaseConnection:
        """Create appropriate database connection based on type"""
        if db_type == DatabaseConfig.LOCALDB:
            return SQLiteConnection()
        elif db_type == DatabaseConfig.MYSQL:
            return MySQLConnection(
                host=kwargs.get('host'),
                user=kwargs.get('user'),
                password=kwargs.get('password'),
                database=kwargs.get('database')
            )
        elif db_type == DatabaseConfig.POSTGRES:
            return PostgreSQLConnection(
                host=kwargs.get('host'),
                user=kwargs.get('user'),
                password=kwargs.get('password'),
                database=kwargs.get('database')
            )
        else:
            raise ValueError(f"Unsupported database type: {db_type}")


class LLMManager:
    """Manager class for Language Learning Model operations"""
    
    def __init__(self, api_key: str, model_name: str = "Llama3-8b-8192"):
        self.api_key = api_key
        self.model_name = model_name
        self._llm = None
    
    @property
    def llm(self) -> ChatGroq:
        """Get or create LLM instance"""
        if self._llm is None:
            self._llm = self._create_llm()
        return self._llm
    
    def _create_llm(self) -> ChatGroq:
        """Create ChatGroq LLM instance"""
        try:
            return ChatGroq(
                groq_api_key=self.api_key,
                model_name=self.model_name,
                streaming=True
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Groq LLM: {e}")
    
    def validate_api_key(self) -> bool:
        """Validate API key"""
        return bool(self.api_key and self.api_key.strip())


class SQLAgent:
    """SQL Agent wrapper class"""
    
    def __init__(self, database: SQLDatabase, llm: ChatGroq):
        self.database = database
        self.llm = llm
        self._agent = None
    
    @property
    def agent(self):
        """Get or create SQL agent"""
        if self._agent is None:
            self._agent = self._create_agent()
        return self._agent
    
    def _create_agent(self):
        """Create SQL agent with toolkit"""
        toolkit = SQLDatabaseToolkit(db=self.database, llm=self.llm)
        return create_sql_agent(
            llm=self.llm,
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
        )
    
    def run_query(self, query: str, callback_handler) -> str:
        """Execute query using the agent"""
        try:
            return self.agent.run(query, callbacks=[callback_handler])
        except Exception as e:
            return f"Error executing query: {str(e)}"


class ChatInterface:
    """Chat interface manager"""
    
    def __init__(self):
        self.session_key = "messages"
        self._initialize_session()
    
    def _initialize_session(self):
        """Initialize chat session"""
        if self.session_key not in st.session_state or st.sidebar.button("Clear message history"):
            st.session_state[self.session_key] = [
                {"role": "assistant", "content": "Hello! How can I help you?"}
            ]
    
    def display_messages(self):
        """Display chat messages"""
        for msg in st.session_state[self.session_key]:
            st.chat_message(msg["role"]).write(msg["content"])
    
    def add_message(self, role: str, content: str):
        """Add message to chat history"""
        st.session_state[self.session_key].append({"role": role, "content": content})
    
    def get_user_input(self) -> Optional[str]:
        """Get user input from chat"""
        return st.chat_input(placeholder="Ask anything from your selected database.")


class StreamlitUI:
    """Streamlit UI components manager"""
    
    def __init__(self):
        self.radio_options = [
            "Use SQLite3 Database - Student.db",
            "Connect to your MySQL Database",
            "Connect to your Postgres Sql Database"
        ]
    
    def setup_page(self):
        """Setup page configuration"""
        st.set_page_config(page_title="LangChain : Chat with SQL DB", page_icon="🦜")
        st.title("🦜LangChain : Chat with SQL DB")
    
    def get_database_selection(self) -> tuple:
        """Get database selection from sidebar"""
        selected_opt = st.sidebar.radio(
            label="Choose the DB which you want to chat",
            options=self.radio_options
        )
        db_type_index = self.radio_options.index(selected_opt)
        return selected_opt, db_type_index
    
    def get_mysql_credentials(self) -> Dict[str, str]:
        """Get MySQL credentials from sidebar"""
        return {
            'host': st.sidebar.text_input("MySQL Host with port"),
            'user': st.sidebar.text_input("MySQL user"),
            'password': st.sidebar.text_input("MySQL Password", type="password"),
            'database': st.sidebar.text_input("MySQL Database")
        }
    
    def get_postgres_credentials(self) -> Dict[str, str]:
        """Get PostgreSQL credentials from sidebar"""
        return {
            'host': st.sidebar.text_input("PostgreSQL Host with port"),
            'user': st.sidebar.text_input("PostgreSQL User"),
            'password': st.sidebar.text_input("PostgreSQL Password", type="password"),
            'database': st.sidebar.text_input("PostgreSQL Database")
        }
    
    def get_api_key(self) -> str:
        """Get API key from sidebar"""
        return st.sidebar.text_input(label="Groq Api Key", type="password")
    
    def show_info(self, message: str):
        """Show info message"""
        st.info(message)
    
    def show_error(self, message: str):
        """Show error message"""
        st.error(message)


class SQLChatApp:
    """Main application class"""
    
    def __init__(self):
        self.ui = StreamlitUI()
        self.chat = ChatInterface()
        self.database_connection = None
        self.llm_manager = None
        self.sql_agent = None
    
    def run(self):
        """Run the main application"""
        self.ui.setup_page()
        
        # Get user inputs
        selected_opt, db_type_index = self.ui.get_database_selection()
        api_key = self.ui.get_api_key()
        
        # Determine database type and get credentials
        db_type, db_credentials = self._get_database_config(db_type_index)
        
        # Validate inputs
        if not self._validate_inputs(api_key, db_credentials):
            return
        
        # Initialize components
        try:
            self._initialize_components(db_type, db_credentials, api_key)
        except Exception as e:
            self.ui.show_error(str(e))
            return
        
        # Handle chat interface
        self._handle_chat()
    
    def _get_database_config(self, db_type_index: int) -> tuple:
        """Get database configuration based on selection"""
        if db_type_index == 1:  # MySQL
            return DatabaseConfig.MYSQL, self.ui.get_mysql_credentials()
        elif db_type_index == 2:  # PostgreSQL
            return DatabaseConfig.POSTGRES, self.ui.get_postgres_credentials()
        else:  # SQLite
            return DatabaseConfig.LOCALDB, {}
    
    def _validate_inputs(self, api_key: str, db_credentials: Dict[str, str]) -> bool:
        """Validate user inputs"""
        if not api_key:
            self.ui.show_info("Please enter the Groq api key.")
            return False
        
        if db_credentials and not all(db_credentials.values()):
            self.ui.show_info("Please enter all database connection details.")
            return False
        
        return True
    
    @st.cache_resource(ttl='2h')
    def _create_database_connection(_self, db_type: str, **credentials) -> SQLDatabase:
        """Create database connection (cached)"""
        connection = DatabaseFactory.create_connection(db_type, **credentials)
        if not connection.validate_credentials():
            raise ValueError("Invalid database credentials")
        return connection.create_connection()
    
    def _initialize_components(self, db_type: str, db_credentials: Dict[str, str], api_key: str):
        """Initialize application components"""
        # Initialize database connection
        database = self._create_database_connection(db_type, **db_credentials)
        
        # Initialize LLM manager
        self.llm_manager = LLMManager(api_key)
        if not self.llm_manager.validate_api_key():
            raise ValueError("Invalid API key")
        
        # Initialize SQL agent
        self.sql_agent = SQLAgent(database, self.llm_manager.llm)
    
    def _handle_chat(self):
        """Handle chat interface interactions"""
        self.chat.display_messages()
        
        user_query = self.chat.get_user_input()
        if user_query:
            # Add user message
            self.chat.add_message("user", user_query)
            st.chat_message("user").write(user_query)
            
            # Process query and get response
            with st.chat_message("assistant"):
                streamlit_callback = StreamlitCallbackHandler(st.container())
                response = self.sql_agent.run_query(user_query, streamlit_callback)
                self.chat.add_message("assistant", response)
                st.write(response)


# Application entry point
if __name__ == "__main__":
    app = SQLChatApp()
    app.run()