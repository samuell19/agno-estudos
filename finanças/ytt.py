from agno.models.openai import OpenAIChat
from agno.agent import Agent
from agno.tools.youtube import YouTubeTools
from agno.playground import Playground, serve_playground_app
from textwrap import dedent
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage
from agno.tools.sql import SQLTools
from fastapi.middleware.cors import CORSMiddleware

memory_db = SqliteMemoryDb(
    table_name="yt_memories",
    db_file="yt/ytm.db"
)
memory = Memory(db=memory_db)

session_storage = SqliteStorage(
    table_name="yt_sessions",
    db_file="yt/yts.db"
)


user_id = "puss_boots"

print(f"🔍 CONFIGURAÇÃO INICIAL:")
print(f"   User ID definido: {user_id}")

agent = Agent(
    name="shrek",
    model=OpenAIChat(id="gpt-4o-mini"),
    markdown=True,
    memory=memory,
    storage=session_storage,
    agent_id="shrek_agent",
    #user_id=user_id,
    tools=[YouTubeTools()],
    instructions=dedent("""\
        You are an expert YouTube content analyst with a keen eye for detail! 🎓
        Follow these steps for comprehensive video analysis:
        1. Video Overview
           - Check video length and basic metadata
           - Identify video type (tutorial, review, lecture, etc.)
           - Note the content structure
        2. Timestamp Creation
           - Create precise, meaningful timestamps
           - Focus on major topic transitions
           - Highlight key moments and demonstrations
           - Format: [start_time, end_time, detailed_summary]
        3. Content Organization
           - Group related segments
           - Identify main themes
           - Track topic progression

        Your analysis style:
        - Begin with a video overview
        - Use clear, descriptive segment titles
        - Include relevant emojis for content types:
          📚 Educational
          💻 Technical
          🎮 Gaming
          📱 Tech Review
          🎨 Creative
        - Highlight key learning points
        - Note practical demonstrations
        - Mark important references

        Quality Guidelines:
        - Verify timestamp accuracy
        - Avoid timestamp hallucination
        - Ensure comprehensive coverage
        - Maintain consistent detail level
        - Focus on valuable content markers
    """),
    enable_user_memories=True,
    enable_session_summaries=True,
    enable_agentic_memory=True,  
)

# 🔍 LOGS DE DEBUG
print(f"\n🔍 AGENT CRIADO:")
print(f"   Agent name: {agent.name}")
print(f"   Agent session_id: {agent.session_id}")
print(f"   Agent user_id: {agent.user_id}")

# Teste recuperação de sessões
try:
    sessions = session_storage.get_all_sessions()
    print(f"\n🔍 SESSÕES NO BANCO:")
    print(f"   Total sessions: {len(sessions)}")
    for session in sessions:
        print(f"   - Session ID: {session.session_id}")
        print(f"     User ID: {session.user_id}")
        print(f"     Agent ID: {session.agent_id}")
        print(f"     Created: {session.created_at}")
        print("   ---")
except Exception as e:
    print(f"❌ Erro ao recuperar sessões: {e}")

app = Playground(agents=[agent]).get_app()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

if __name__ == "__main__":
    print(f"\n🚀 INICIANDO SERVIDOR...")
    serve_playground_app("ytt:app", reload=True, host="localhost", port=7777)