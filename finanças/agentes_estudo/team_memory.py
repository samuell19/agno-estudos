from agno.agent import Agent
from agno.team import Team
from agno.models.groq import Groq
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from agno.tools.hackernews import HackerNewsTools
from agno.tools.duckduckgo import DuckDuckGoTools
from textwrap import dedent
from agno.playground import Playground, serve_playground_app

# Memory setup
memory_db = SqliteMemoryDb(
    table_name="team_memories",
    db_file="tmp/tmemory.db",
)
memory = Memory(db=memory_db)
memory.clear()

# Agentes especializados com roles e instruções mais claras
hack_agent = Agent(
    name="HackerNews Specialist",
    model=Groq(id="llama-3.1-8b-instant"),
    role="Search and analyze HackerNews posts",
    tools=[HackerNewsTools()],
    add_name_to_instructions=True,
    instructions=dedent("""
    You are a HackerNews specialist. When given a topic:
    1. Search for the most relevant and recent posts
    2. Focus on high-quality discussions and trending topics
    3. Provide concise summaries with key insights
    4. Include post scores and comment counts when relevant
    """),
)

duck_agent = Agent(
    name="Web Research Specialist", 
    model=Groq(id="llama-3.1-8b-instant"),
    role="Search and analyze web content",
    tools=[DuckDuckGoTools()],
    add_name_to_instructions=True,
    instructions=dedent("""
    You are a web research specialist. When given a topic:
    1. Search for comprehensive, up-to-date information
    2. Focus on authoritative sources and recent developments
    3. Provide detailed analysis with key findings
    4. Include relevant links and sources
    """),
)

# Team otimizado
team = Team(
    name="Research Team",
    mode="coordinate",  # Mais eficiente que collaborate
    model=Groq(id="llama-3.1-8b-instant"),
    memory=memory,
    storage=SqliteStorage(
        table_name="team_sessions",
        db_file="tmp/tmemory.db"
    ),
    members=[hack_agent, duck_agent],
    instructions=[
        "You coordinate research between HackerNews and web search specialists",
        "First delegate HackerNews search, then web search",
        "You have to stop the discussion when you think the team has reached a consensus",
        "If the user wants do discuss about the news, you can access your memory and talk with him"
        
    ],
    success_criteria="Complete research report with insights from both HackerNews and web sources",
    show_tool_calls=False,
    enable_agentic_context=True,
    markdown=True,
    show_members_responses=False,
)

app = Playground(teams=[team]).get_app()

if __name__ == "__main__":
    serve_playground_app("team_memory:app", reload=True)