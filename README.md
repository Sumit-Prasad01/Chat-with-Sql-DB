# 🦜 LangChain SQL Chat Application

A powerful Streamlit-based application that allows you to chat with your SQL databases using natural language. Built with LangChain, Groq AI, and modern Object-Oriented Programming principles.

## ✨ Features

- **Multi-Database Support**: Connect to SQLite, MySQL, and PostgreSQL databases
- **Natural Language Queries**: Ask questions about your data in plain English
- **Real-time Streaming**: Get responses as they're generated using Groq's streaming capabilities
- **Interactive Chat Interface**: Clean, user-friendly chat interface built with Streamlit
- **Secure Connections**: Support for password-protected database connections
- **Session Management**: Persistent chat history with clear functionality
- **Error Handling**: Robust error handling and validation

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **LLM Integration**: LangChain + Groq AI (Llama3-8b-8192)
- **Database Support**: SQLite, MySQL, PostgreSQL
- **Architecture**: Object-Oriented Programming (OOP)
- **Language**: Python 3.8+

## 📋 Prerequisites

Before running this application, make sure you have:

1. **Python 3.8 or higher** installed
2. **Groq API Key** - Get it from [Groq Console](https://console.groq.com/)
3. **Database access** (depending on your choice):
   - SQLite: A `.db` file (sample `student.db` included)
   - MySQL: Database credentials and connection details
   - PostgreSQL: Database credentials and connection details

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd langchain-sql-chat
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## 📦 Dependencies

Create a `requirements.txt` file with the following dependencies:

```txt
streamlit>=1.28.0
langchain>=0.0.340
langchain-groq>=0.0.1
sqlalchemy>=2.0.0
sqlite3
mysql-connector-python>=8.0.33
psycopg2-binary>=2.9.7
pathlib
```

## 🎯 Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Configure your database**:
   - **SQLite**: Select "Use SQLite3 Database - Student.db" (default option)
   - **MySQL**: Select MySQL option and provide connection details
   - **PostgreSQL**: Select PostgreSQL option and provide connection details

3. **Enter your Groq API Key** in the sidebar

4. **Start chatting** with your database using natural language!

## 💬 Example Queries

Here are some example queries you can try:

- "Show me all the students in the database"
- "What is the average age of students?"
- "How many students are enrolled in each course?"
- "Find students with grades above 85"
- "Show me the top 5 students by GPA"
- "What courses are available?"

## 🏗️ Architecture

The application follows modern OOP design principles:

### Core Classes

- **`DatabaseConnection`**: Abstract base class for database connections
- **`SQLiteConnection`**: SQLite-specific implementation
- **`MySQLConnection`**: MySQL-specific implementation  
- **`PostgreSQLConnection`**: PostgreSQL-specific implementation
- **`DatabaseFactory`**: Factory pattern for creating database connections
- **`LLMManager`**: Manages Groq LLM initialization and operations
- **`SQLAgent`**: Handles LangChain SQL agent creation and query execution
- **`ChatInterface`**: Manages chat session and message history
- **`StreamlitUI`**: Handles all UI components and user interactions
- **`SQLChatApp`**: Main application orchestrator

### Design Patterns Used

- **Factory Pattern**: For database connection creation
- **Abstract Base Class**: For consistent database interface
- **Single Responsibility Principle**: Each class has one clear purpose
- **Dependency Injection**: Components are loosely coupled

## 🗃️ Database Setup

### SQLite (Default)
- Place your SQLite database file as `student.db` in the project root
- The app will automatically detect and use it

### MySQL
You'll need to provide:
- Host with port (e.g., `localhost:3306`)
- Username
- Password
- Database name

### PostgreSQL
You'll need to provide:
- Host with port (e.g., `localhost:5432`)
- Username
- Password
- Database name

## 🔧 Configuration

### Environment Variables (Optional)
You can set up environment variables for default configurations:

```bash
export GROQ_API_KEY="your-groq-api-key"
export DB_TYPE="sqlite"  # or "mysql" or "postgresql"
```

### Custom Database Path
To use a custom SQLite database, modify the `SQLiteConnection` class:

```python
def __init__(self, db_file_path: Optional[Path] = None):
    self.db_file_path = db_file_path or Path("path/to/your/database.db")
```

## 🛡️ Security Features

- **Password Input Fields**: Database passwords are masked
- **API Key Protection**: Groq API key input is hidden
- **Read-Only SQLite**: SQLite connections are opened in read-only mode
- **Input Validation**: All user inputs are validated before processing

## 🐛 Troubleshooting

### Common Issues

1. **"Failed to initialize Groq LLM"**
   - Check your Groq API key
   - Ensure you have internet connectivity
   - Verify the API key has sufficient credits

2. **"Failed to connect to Database"**
   - Verify database credentials
   - Check if the database server is running
   - Ensure network connectivity to the database

3. **"No module named 'xyz'"**
   - Install missing dependencies: `pip install -r requirements.txt`
   - Ensure you're using the correct virtual environment

### Debug Mode
To enable verbose logging, modify the agent creation:
```python
verbose=True  # Already enabled in the code
```

---

- Streamlit App Link - https://sumit-prasad01-chat-with-sql-db-app-ps8ihs.streamlit.app/

**Made with using LangChain and Streamlit**
