from agno.agent import Agent
from agno.tools.gmail import GmailTools

agent = Agent(tools=[GmailTools()], show_tool_calls=True)
agent.print_response("Show me my latest 5 unread emails", markdown=True)