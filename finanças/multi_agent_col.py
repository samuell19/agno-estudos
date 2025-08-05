import asyncio
from textwrap import dedent
from agno.agent import Agent
from agno.models.groq import Groq
from agno.team import Team
from agno.tools.arxiv import ArxivTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.hackernews import HackerNewsTools

reddit_reseacher = Agent(
    name="Reddit Reseacher",
    model=Groq(id="llama-3.3-70b-versatile"),
    role="Research a topic in reddit",
    tools=[DuckDuckGoTools()],
    add_name_to_instructions=True,
    instructions=dedent("""
    You are a Reddit researcher.
    You will be given a topic to research on Reddit.
    You will need to find the most relevant posts on Reddit.
    """),

)

hackernews_reseacher= Agent(
    name= "HackerNews Reseacher",
    model=Groq(id="llama-3.3-70b-versatile"),
    role= "Research a topic in hackernews",
    tools=[HackerNewsTools()],
    add_name_to_instructions=True,
    instructions=dedent("""
    You are a HackerNews researcher.
    You will be given a topic to research on HackerNews.
    You will need to find the most relevant posts on HackerNews.
    """),
)

academic_paper= Agent(
    name="Academic Reseacher",
    model=Groq(id="llama-3.3-70b-versatile"),
    role= "Research trending discussions and real-time updates",
    tools=[GoogleSearchTools(), ArxivTools()],
    add_name_to_instructions=True,
    instructions=dedent("""
    You are a academic paper researcher.
    You will be given a topic to research in academic literature.
    You will need to find relevant scholarly articles, papers, and academic discussions.
    Focus on peer-reviewed content and citations from reputable sources.
    Provide brief summaries of key findings and methodologies.
    """),
)

twitter_reseacher= Agent(
    name="Twitter Reseacher",
    model=Groq(id="llama-3.3-70b-versatile"),
    role="Research trending discussions and real time updates",
    tools=[DuckDuckGoTools()],
    add_name_to_instructions=True,
    instructions=dedent("""
    You are a Twitter/X researcher.
    You will be given a topic to research on Twitter/X.
    You will need to find trending discussions, influential voices, and real-time updates.
    Focus on verified accounts and credible sources when possible.
    Track relevant hashtags and ongoing conversations.
    """),
)

agent_team = Team(
    name="Discussion Team",
    members=[reddit_reseacher, hackernews_reseacher, twitter_reseacher, academic_paper],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions="You are a discussion master coordinating research from multiple sources.",
    markdown=True,
)

if __name__=="__main__":
  
        agent_team.print_response(
            message="Start the discussion on the topic: 'What is the best way to learn code?'",
            stream=True,
            stream_intermediate_steps=True,
        )
    