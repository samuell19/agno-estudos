from agno.agent import Agent
from agno.knowledge.text import TextKnowledgeBase
from agno.models.openai import OpenAIChat
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.combined import CombinedKnowledgeBase
from agno.playground import Playground
from agno.playground import serve_playground_app

txt_path = "maildir"

knowledge_base = CombinedKnowledgeBase(
    sources=[
        TextKnowledgeBase(
            path=txt_path,  
            formats=[".txt", ""],
            vector_db=ChromaDb(collection="emails"),
        ),
    ],
    vector_db=ChromaDb(collection="combined_uploads"),
)

agent_big = Agent(
    name="The biggest",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="Você vai ter acesso a uma base gigantesca de emails, te usarei como um grande explorador de arquivos",
    knowledge=knowledge_base,
    search_knowledge=True, 
    markdown=True,
)



app=Playground(agents=[agent_big]).get_app()

if __name__== "__main__":
    print("📖 Carregando knowledge base...")
    knowledge_base.load(recreate=True)
    serve_playground_app("gigante:app", port=7777, host="0.0.0.0")