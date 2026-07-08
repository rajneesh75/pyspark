import os
from typing import Annotated, TypedDict
from langchain_openai import (OpenAIEmbeddings)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import (HumanMessage, BaseMessage, SystemMessage)
from langgraph.graph import (StateGraph, START, END)
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langgraph.graph.message import (add_messages)
from langgraph.prebuilt import (ToolNode)
from langgraph.checkpoint.memory import (MemorySaver)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-5.5", temperature=0, api_key=api_key)

documents = [
    "Employee Raj works on Spark and Kafka. Raj also plays cricket and listens to music",
    "Project Alpha uses Databricks Delta Lake.",
    "Production support runs daily at 10 PM."
]

embeddings = OpenAIEmbeddings(api_key=api_key)
print("\nCreating Vector DB from company documents")
vector_db = Chroma.from_texts(texts=documents, embedding=embeddings, collection_name="company_docs",
                              persist_directory="./chroma_db")
print("\nVector DB created successfully")
retriever = (vector_db.as_retriever(search_kwargs={"k": 2}))
print("\nRetriever created successfully")
system_prompt = SystemMessage(content=""" You are a company assistant. For company information, 
always use the search_documents tool. Do not guess. """)


@tool
def search_documents(question: str) -> str:
    """
    Search company documents.
    Use this tool when you need company information.
    """

    print("\nTOOL: Searching Vector DB")
    docs = retriever.invoke(question)
    return "\n".join([d.page_content for d in docs])


tools = [search_documents]


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


llm_with_tools = (llm.bind_tools(tools))


def agent(state: AgentState):
    response = (llm_with_tools.invoke(state["messages"]))
    return {"messages": [response]}


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

config = {"configurable": {"thread_id": "user1"}}


def ask(question):
    result = graph.invoke({"messages": [system_prompt, HumanMessage(content=question)]}, config=config)
    print("\nANSWER:")
    print(result["messages"][-1].content)


ask("What technology does Raj work on?")
ask("Which project uses Delta Lake?")
ask("What does Raj do in free time?")
ask("Does Raj do gardening?")
