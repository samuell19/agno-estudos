from agno.agent import Agent
from agno.knowledge.text import TextKnowledgeBase
from agno.models.openai import OpenAIChat
from agno.vectordb.pgvector import PgVector  
from agno.playground import Playground
from agno.playground import serve_playground_app
from agno.embedder.ollama import OllamaEmbedder
from agno.document.chunking.recursive import RecursiveChunking
from agno.document.chunking.document import DocumentChunking
import asyncio

txt_path = "transcripts"

knowledge_base = TextKnowledgeBase(
    path=txt_path,
    vector_db=PgVector(
        table_name="filmes", 
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        embedder=OllamaEmbedder(id="nomic-embed-text", dimensions=768),
    ),
    chunking_strategy=DocumentChunking(chunk_size=4000)
)

agent_big = Agent(
    name="The biggest",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="Você tem acesso a uma base gigantesca de transcrições de filmes. Te usarei como um grande explorador e analista de filmes.",
    knowledge=knowledge_base,
    search_knowledge=True,
    markdown=True,
)

app = Playground(agents=[agent_big]).get_app()

if __name__ == "__main__":
    print("📖 Carregando knowledge base de 50 mil filmes...")
    asyncio.run(knowledge_base.aload(recreate=True))
    print("✅ Knowledge base carregada! Iniciando servidor...")
    serve_playground_app("gigante:app", port=7777, host="0.0.0.0")