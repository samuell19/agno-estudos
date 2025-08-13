from agno.knowledge.combined import CombinedKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.chroma import ChromaDb
from agno.playground import Playground
from agno.playground import serve_playground_app
from agno.models.openai import OpenAIChat
from agno.agent import Agent
pdf_path = "livro14.pdf"

knowledge_base = CombinedKnowledgeBase(
    sources=[
        PDFKnowledgeBase(
            vector_db=ChromaDb(collection="uploads_pdf"), 
            path=pdf_path
        ),
    ],
    vector_db=ChromaDb(collection="combined_uploads"),
)

agent = Agent(
    name="Upload Agent",
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    add_history_to_messages=True,
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    print("📖 Carregando knowledge base...")
    knowledge_base.load(recreate=False)
    
    print("🚀 Starting playground...")
    serve_playground_app(app="upload:app", host="0.0.0.0", port=7777)