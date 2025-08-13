from agno.agent import Agent
from agno.models.openai import OpenAIChat 
from agno.tools.sql import SQLTools  
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.playground import Playground, serve_playground_app
from agno.vectordb.chroma import ChromaDb
from agno.agent import AgentKnowledge
import sqlite3



db_path = "biblioteca.db"
db_url=f"sqlite:///{db_path}"

vector_db=ChromaDb(
    collection="biblioteca_vetorial",
    path="tmp/chromab_biblioteca",
    persistent_client=True
)

knowledge_base= AgentKnowledge(
    vector_db=vector_db
)

def vetorizar_biblioteca():
    conn=sqlite3.connect(db_path)
    query = """
    SELECT 
        b.title as titulo,
        b.isbn,
        a.name as autor,
        b.publication_year as ano,
        l.loan_date as emprestimo,
        l.return_date as devolucao,
        l.user_name as usuario
    FROM books b
    LEFT JOIN authors a ON b.author_id = a.id  
    LEFT JOIN loans l ON b.id = l.book_id
    """
    cursor=conn.execute(query)
    dados=cursor.fetchall()

    for row in dados:
        texto = f"Livro: {row[0]}, ISBN: {row[1]}, Autor: {row[2]}, Ano: {row[3]}, Empréstimo: {row[4]}, Devolução: {row[5]}, Usuário: {row[6]}"
        knowledge_base.load_text(texto)

    conn.close()
    print(f"✅ Vetorizados {len(dados)} registros da biblioteca")


session_storage=SqliteStorage(
    table_name="session_d"
)


memory_db = SqliteMemoryDb(
    table_name="memorias",
    db_file="tempo/memoria.db",
)

memory = Memory(db=memory_db)


session_id = "sqlite_memories"
user_id = "funny_user"

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"), 
    memory=memory,
    knowledge=knowledge_base,
    tools=[SQLTools(db_url=f"sqlite:///{db_path}")],  
    storage=SqliteStorage(
        table_name="agent_sessions", 
        db_file="tempo/memoria.db"
    ),
    instructions="""Você é um assistente bibliotecário com acesso a um banco de dados de livros.
    
    Ao escrever consultas SQL:
    - Use cláusula LIMIT diretamente no SQL (ex: "SELECT * FROM books ORDER BY year_published LIMIT 5")
    - Sempre forneça explicações claras dos resultados
    - Formate resultados em tabelas legíveis quando possível""",
    markdown=True,
    enable_user_memories=True,
    enable_session_summaries=True,
    add_history_to_messages=True,
    retries=3,
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    print("🚀 Starting biblioteca playground...")
    print("📊 Database:", db_path)
    print("🌐 Playground will be available at http://0.0.0.0:7777")
    vetorizar_biblioteca()
    
    serve_playground_app(
        app="biblioteca:app", 
        host="0.0.0.0", 
        port=7777,
        reload=False 
    )