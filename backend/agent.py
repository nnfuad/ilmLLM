from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_community.chat_models import ChatOllama

# Define the state for LangGraph. This contains the message history.
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the local LLM using Ollama
# Make sure you have run `ollama run llama3` in your terminal first.
llm = ChatOllama(model="llama3", temperature=0.7)

# Define the core chatbot node
def chatbot(state: State):
    # Pass the message history to the LLM to get a response
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build the LangGraph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile the graph into an executable application
# In a production environment, you would add a checkpointer here (e.g., SQLite/Postgres)
# to persist the state (memory) across different user sessions.
agent_app = graph_builder.compile()
