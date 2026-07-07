import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import (HumanMessage, BaseMessage, SystemMessage)
from langgraph.graph import (StateGraph, START, END)
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers.
    """

    print(f"\nTOOL EXECUTING: multiply({a}, {b})")
    return a * b


@tool
def add(a: int, b: int) -> int:
    """
    Add two numbers.
    """

    print(f"\nTOOL EXECUTING: add({a}, {b})")
    return a + b


tools = [multiply, add]
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=api_key)
llm_with_tools = llm.bind_tools(tools)


def print_messages(state: AgentState):
    print("\n----- CURRENT STATE -----")

    for message in state["messages"]:
        print(type(message).__name__, ":", message.content)
    print("-------------------------\n")


def call_model(state: AgentState):
    print("\nNODE: Agent")
    print_messages(state)
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def should_continue(state: AgentState):
    print("\nNODE: Router")

    last_message = (state["messages"][-1])
    if getattr(last_message, "tool_calls", None):
        print("Decision: Call tools")
        return "tools"

    print("Decision: Finish")
    return END


print("Building graph...")
graph_builder = StateGraph(AgentState)
graph_builder.add_node("agent", call_model)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges("agent", should_continue)
graph_builder.add_edge("tools", "agent")
graph = graph_builder.compile()

print("\nExecution starts\n")
result = graph.invoke({"messages": [
    SystemMessage(content=""" You are a calculator agent. Never calculate yourself. Always use available tools.
     If tool is not there to calculate, say 'I cannot calculate that.' """),
    HumanMessage(content="what is 12 times 15?")]})
print("\nFINAL RESULT")
for msg in result["messages"]:
    msg.pretty_print()

result = graph.invoke({"messages": [
    SystemMessage(content=""" You are a calculator agent. Never calculate yourself. Always use available tools.
     If tool is not there to calculate, say 'I cannot calculate that.'"""),
    HumanMessage(content="what is 12 plus 15?")]})
print("\nFINAL RESULT")
for msg in result["messages"]:
    msg.pretty_print()


result = graph.invoke({"messages": [
    SystemMessage(content=""" You are a calculator agent. Never calculate yourself. Always use available tools.
     If tool is not there to calculate, say 'I cannot calculate that.'"""),
    HumanMessage(content="what is 12 divided by 15?")]})
print("\nFINAL RESULT")
for msg in result["messages"]:
    msg.pretty_print()


result = graph.invoke({"messages": [
    SystemMessage(content=""" You are a calculator agent. Never calculate yourself. Always use available tools.
     If tool is not there to calculate, say 'I cannot calculate that.'"""),
    HumanMessage(content="what is (12 plus 15) times 10?")]})
print("\nFINAL RESULT")
for msg in result["messages"]:
    msg.pretty_print()
