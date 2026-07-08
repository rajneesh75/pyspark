import os
import langgraph
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import (HumanMessage, BaseMessage)
from langgraph.graph import (StateGraph, START, END)
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-5.5", temperature=0, api_key=api_key)
langgraph.debug = True


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


@tool
def get_orders(customer_id: int) -> list:
    """
    Get orders for a customer.
    """

    print(f"\nTOOL EXECUTING get_orders({customer_id})")
    database = {
        101: [
            {
                "order": "Laptop",
                "amount": 80000
            },
            {
                "order": "Mouse",
                "amount": 2000
            }
        ],

        102: [
            {
                "order": "Phone",
                "amount": 50000
            }
        ]
    }

    return database.get(customer_id, [])


tools = [get_orders]
llm_with_tools = (llm.bind_tools(tools))


def agent(state: AgentState):
    result = (llm_with_tools.invoke(state["messages"]))
    return {"messages": [result]}


def router(state: AgentState):
    last_message = (state["messages"][-1])
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END


builder = StateGraph(AgentState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", router)
builder.add_edge("tools", "agent")
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "customer_chat_1"}}
response = graph.invoke({"messages": [HumanMessage(content="My customer id is 113")]}, config=config)
print(response["messages"][-1].content)

response = graph.invoke({"messages": [HumanMessage(content="Show me my orders")]}, config=config)
print(response["messages"][-1].content)
