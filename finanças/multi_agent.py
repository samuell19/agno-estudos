from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.playground import Playground, serve_playground_app
from agno.team import Team

web_agent= Agent (
    name="Web Agent",
    role="Search the web for information",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGoTools()],
    instructions="Always include sources",
    show_tool_calls=True,
    markdown=True,
)

financial_agent= Agent(
    name="financial agent",
    role="Get financial data",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions="use tables to show data",
    show_tool_calls=True,
    markdown=True,
)

agent_team= Team(
    mode="cordinate",
    members=[web_agent, financial_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    success_criteria="A comprehensive financial news report with clear sections and data-driven insights.",
    instructions=["Always include sources", "use tables to show data"],
    show_tool_calls=True,
    markdown=True,
)



app = Playground(teams=[agent_team]).get_app()

if __name__ == "__main__":
    serve_playground_app("multi_agent:app", reload=True, host="0.0.0.0", port=7777)