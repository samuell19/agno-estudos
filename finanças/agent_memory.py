from agno.agent import Agent
from agno.models.groq import Groq
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app



memory_db= SqliteMemoryDb(
    table_name="agent_memories",
    db_file="temp/memory_db",
)

session_id = "sqlite_memories"
user_id = "sqlite_user"

memory=Memory(db=memory_db)

memory.clear()

session_id="sqlite_memories"
user_id="sqlite_user"

agent=Agent(
    name="Agent with memory",
    model=Groq(id="llama-3.3-70b-versatile"),
    memory=memory,
    storage=SqliteStorage(
        table_name="agent_sessions",
        db_file="temp/memory.db"
    ),
    enable_user_memories=True,
    enable_session_summaries=True,
)

app=Playground(agents=[agent]).get_app()

if __name__=="__main__":
    serve_playground_app("agent_memory:app", reload=True)