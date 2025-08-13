from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.sql import SQLTools
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.playground import Playground, serve_playground_app
from agno.tools.googlesearch import GoogleSearchTools
from agno.team import Team
from agno.tools.exa import ExaTools


db_path = "biblioteca.db"


session_storage=SqliteStorage(
    table_name="bib_sessions",
    db_file="bib/bsessions.db",
)

memory_db = SqliteMemoryDb(
    table_name="bmemories",
    db_file="bib/bmemoria.db",
)

memory = Memory(db=memory_db)


session_id = "sqlite_memories"
user_id = "funny_user"

agent_b = Agent(
    name="Funcionário",
    role="Funcionário da biblioteca, tem acesso ao banco e pode analisar ele",
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Você é um funcionário com acesso a biblioteca, seu dever é buscar dentro do banco de dados informações sobre a biblioteca.", 
    memory=memory,
    tools=[SQLTools(db_url=f"sqlite:///{db_path}")],  
    instructions="""Você é um assistente bibliotecário com acesso a um banco de dados de livros.
    
    Ao escrever consultas SQL:
    - Use cláusula LIMIT diretamente no SQL (ex: "SELECT * FROM books ORDER BY year_published LIMIT 5")
    - Sempre forneça explicações claras dos resultados
    - Formate resultados em tabelas legíveis quando possível""",
    markdown=True,
    retries=3,
)

agent_r= Agent(
    name="Recomendador",
    model=OpenAIChat(id="gpt-4o-mini"), 
    tools=[GoogleSearchTools()],
    role="Agente recomendador de livros",
    instructions=[
        "Primeiro, analise o que o usuário está falando, principalmente sobre books e authors"
        "Em seguida, pesquise livros ou autores parecidos na internet com base no contexto com o usuário"
        "Depois, faça algumas recomendações, de uma a cinco (se o usuário pedir mais, você pesquisa mais)"
        "Por último, recomende os livros ou autores que o usuário pode gostar"
    ],
    add_datetime_to_instructions=True,
)


agent_a= Agent(
    name="Analista",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[ExaTools()],
    role="Agente analisador de livros",
    instructions=[
        "Você é um mestre analista, primeiramente analise o se o usuário quer uma análise de um livro ou autor"
        "Em seguida, busque usando o EXA e faça uma análise"
        "Depois, compare com outras obras parecidas"
        "Por fim, forneça uma análise equilibrada para o usuário"
    ],
    add_datetime_to_instructions=True,
)

leader=Team(
    name="Gerente",
    mode="coordinate",
    team_id="gerente_id",
    model=OpenAIChat(id="gpt-4o-mini"),
    memory=memory,
    storage=session_storage,
    members=[agent_b, agent_r, agent_a],
    description="Você é o gerente de uma biblioteca, de acordo com o usuário, você deve pesquisar dados dentro do seu banco de dados, recomendar livros ou fazer",
    instructions=[
        "Verifique se o usuário está pedindo recomendações de livros, procurando algo na biblioteca ou pedindo uma análise de livros"
        "Caso a pergunta/busca que ele fez na biblioteca, não tenha no banco de dados"
    ],
    enable_team_history=True,
    enable_user_memories=True,
    enable_agentic_memory=True,
    enable_session_summaries=True,
)

app = Playground(teams=[leader]).get_app()

if __name__ == "__main__":
    print("🚀 Starting biblioteca playground...")
    print("📊 Database:", db_path)
    print("🌐 Playground will be available at http://0.0.0.0:7777")
    
    serve_playground_app(
        app="biblioteca_new:app", 
        host="0.0.0.0", 
        port=7777,
        reload=False 
    )