from agno.agent import Agent
from agno.tools.jina import JinaReaderTools
from agno.models.openai import OpenAIChat
from agno.playground import Playground
from agno.playground import serve_playground_app

agent_web=Agent(
    name="Web Reader",
    tools=[JinaReaderTools()],
    model=OpenAIChat(id="gpt-4o-mini"), 
    instructions="Você deve atender aos pedidos do usuário, visitando e analisando o link do site, forncendo informações uteis, resumindo e tirando suas dúvidas.",
    markdown=True,
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
)


app=Playground(agents=[agent_web]).get_app()

if __name__=="__main__":
    serve_playground_app("jina:app", host="0.0.0.0", port=7777, reload=True)

