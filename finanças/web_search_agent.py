from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.playground import Playground, serve_playground_app


agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    description="You are an enthusiastic news reporter with a flair for storytelling!",
    tools=[DuckDuckGoTools()],      
    show_tool_calls=True,           
    markdown=True                   
)


agent.print_response("Tell me about a breaking news story from New York.", stream=True)


app = Playground(agents=[agent]).get_app()


if __name__ == "__main__":
    serve_playground_app("web_search_agent:app", reload=True)