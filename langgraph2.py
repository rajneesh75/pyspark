import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from typing import Annotated, TypedDict


load_dotenv()


# ----------------------------
# Define Agent State
# ----------------------------

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ----------------------------
# Define Tool
# ----------------------------

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


tools = [multiply]


# ----------------------------
# Define LLM
# ----------------------------

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

llm_with_tools = llm.bind_tools(tools)


# ----------------------------
# Agent Node
# ----------------------------

def call_model(state: AgentState):
    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ----------------------------
# Decide Next Step
# ----------------------------

def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


# ----------------------------
# Build Graph
# ----------------------------

graph_builder = StateGraph(AgentState)


graph_builder.add_node(
    "agent",
    call_model
)


graph_builder.add_node(
    "tools",
    ToolNode(tools)
)


graph_builder.add_edge(
    START,
    "agent"
)


graph_builder.add_conditional_edges(
    "agent",
    should_continue
)


graph_builder.add_edge(
    "tools",
    "agent"
)


graph = graph_builder.compile()


# ----------------------------
# Run Agent
# ----------------------------

result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="what is 12 times 15?"
            )
        ]
    }
)


for msg in result["messages"]:
    msg.pretty_print()