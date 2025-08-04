from agno.agent.agent import Agent
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.groq import Groq
from rich.pretty import pprint
from agno.playground import Playground, serve_playground_app

memory_db = SqliteMemoryDb(table_name="memory", db_file="tmp/memory.db")
# No need to set the model, it gets set to the model of the agent
memory = Memory(db=memory_db, delete_memories=True, clear_memories=True)

# Reset the memory for this example
memory.clear()

# User ID for the memory
john_doe_id = "john_doe@example.com"
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    memory=memory,
    # This will trigger the MemoryManager after each user message
    enable_user_memories=True,
)

# Send a message to the agent that would require the memory to be used
agent.print_response(
    "My name is John Doe and I like to hike in the mountains on weekends.",
    stream=True,
    user_id=john_doe_id,
)

# Send a message to the agent that checks the memory is working
agent.print_response("What are my hobbies?", stream=True, user_id=john_doe_id)

# Print the memories for the user
memories = memory.get_user_memories(user_id=john_doe_id)
print("Memories about John Doe:")
pprint(memories)

# Send a message to the agent that removes all memories for the user
agent.print_response(
    "Remove all existing memories of me.",
    stream=True,
    user_id=john_doe_id,
)
memories = memory.get_user_memories(user_id=john_doe_id)
print("Memories about John Doe:")
pprint(memories)
