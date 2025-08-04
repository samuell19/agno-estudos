from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.sql import SQLTools
from agno.storage.sqlite import SqliteStorage
import sqlite3
import os


db_path = "/workspaces/agno-estudos/finanças/biblioteca.db"

class EnhancedSQLTools(SQLTools):
    def schema(self):
        base_schema = super().schema()
        for func in base_schema.get("functions", []):
            if func.get("name") == "run_sql_query":
                properties = func.get("parameters", {}).get("properties", {})
                if "limit" in properties:
                    del properties["limit"]
                if "query" in properties:
                    properties["query"]["description"] += " Use SQL LIMIT clause for row limits."
        return base_schema


db_path = "/workspaces/agno-estudos/finanças/biblioteca.db"


agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[EnhancedSQLTools(db_url=f"sqlite:///{db_path}")],
    storage=SqliteStorage(
        table_name="agent_sessions", 
        db_url="sqlite:///agent_storage.db"
    ),
    instructions="""You are a helpful librarian assistant with access to a books database.
    
    Database schema:
    - books: id, title, author, year_published, genre, pages, rating
    - authors: id, name, birth_year, nationality  
    - loans: id, book_id, borrower_name, loan_date, return_date
    When writing SQL queries:
    - Use LIMIT clause directly in your SQL (e.g., "SELECT * FROM books ORDER BY year_published LIMIT 5")
    
    - Always provide clear explanations of your results
    - Format results in readable tables when possible""",
    markdown=True,
    add_history_to_messages=True,
    retries=3,
)


print("🔍 Testing the library database...")
agent.print_response(
    "Show me the 5 youngest authors in the database. ordered by birth year.",
    stream=True
)