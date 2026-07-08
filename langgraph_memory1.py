import os
import langgraph
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import (HumanMessage, BaseMessage)
from langgraph.graph import (StateGraph, START, END)
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-5.5", temperature=0, api_key=api_key)
langgraph.debug = True


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chatbot(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(AgentState)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "user_123"}}
result = graph.invoke({"messages": [HumanMessage(content="My name is Rajneesh and I like cricket.")]},
                      config=config)
for msg in result["messages"]:
    msg.pretty_print()

result = graph.invoke({"messages": [HumanMessage(content="What is my name and what sport do I like?")]},
                      config=config)
for msg in result["messages"]:
    msg.pretty_print()
