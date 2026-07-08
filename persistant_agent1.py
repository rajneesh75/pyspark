import os
import sqlite3
import langgraph
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import (HumanMessage, BaseMessage)
from langgraph.graph import (StateGraph, START, END)
from langgraph.graph.message import add_messages


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
connection = sqlite3.connect("agent_memory.db", check_same_thread=False)
memory = SqliteSaver(connection)
graph = builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "raj_session"}}
while True:

    question = input("\nYou: ")
    if question.lower() == "exit":
        break

    result = graph.invoke({"messages": [HumanMessage(content=question)]}, config=config)
    print("\nAI:", result["messages"][-1].content)
