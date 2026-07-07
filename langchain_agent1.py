import langchain
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

langchain.debug = True
load_dotenv()
api_key = str(os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(temperature=0, model="gpt-4.1-mini", api_key=api_key)


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


agent = create_agent( model=llm,  tools=[multiply])

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content="what is 12 times 15?"
            )
        ]
    }
)

for message in result["messages"]:
    message.pretty_print()
