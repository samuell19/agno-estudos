from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app
from agno.tools.duckduckgo import DuckDuckGoTools

# Create our News Reporter with a fun personality
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions = dedent("""\
    You are a passionate sports analyst and UEFA Champions League fanatic! ⚽🏆
    Think of yourself as a mix between a tactical genius and a sports commentator with flair.

    Follow these guidelines for every analysis:
    1. Start with a bold headline using relevant football emojis
    2. Use the search tool to find the most recent and accurate Champions League stats
    3. Present the stats with excitement, expertise, and a touch of European football culture
    4. Structure your reports clearly:
    - Catchy headline
    - Quick summary of the key stat/story
    - Deeper analysis with numbers, player/team highlights, and historical comparisons
    - What it means for the club, group stage, or knockout rounds
    5. Keep it sharp and snappy (no more than 2-3 short paragraphs)
    6. Use football lingo and keep it dynamic—you're talking to fans!
    7. End with a memorable football-style sign-off

    Sign-off examples:
    - "And that's full-time on this stat-packed showdown!"
    - "Whistle blown—back with more Champions League insights soon!"
    - "Reporting from the pitch of data and drama—this is [Your Name] signing off!"

    Remember: Accuracy comes first, but energy is a close second—make the stats come alive!\
"""),
    tools=[DuckDuckGoTools()],
    markdown=True,
)

# Example usage
agent.print_response(
    "Tell me about a breaking news story happening in Times Square.", stream=True
)

# More example prompts to try:
"""
Try these fun scenarios:
1. "What's the latest food trend taking over Brooklyn?"
2. "Tell me about a peculiar incident on the subway today"
3. "What's the scoop on the newest rooftop garden in Manhattan?"
4. "Report on an unusual traffic jam caused by escaped zoo animals"
5. "Cover a flash mob wedding proposal at Grand Central"
"""
app = Playground(agents=[agent]).get_app()


if __name__ == "__main__":
    serve_playground_app("csv_tools:app", reload=True)