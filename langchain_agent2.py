import os
import langchain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

langchain.debug = True
load_dotenv()


@tool
def get_customer(customer_id: int) -> dict:
    """
    Get customer information using customer id.
    """

    customers = {
        101: {
            "name": "Raj",
            "tier": "gold"
        },
        102: {
            "name": "Amit",
            "tier": "silver"
        }
    }

    return customers.get(customer_id, {"error": "customer not found"})


@tool
def get_orders(customer_id: int) -> list:
    """
    Get all orders for a customer.
    """

    orders = {
        101: [
            {
                "order_id": 5001,
                "amount": 10000
            },
            {
                "order_id": 5002,
                "amount": 5000
            }
        ]
    }

    return orders.get(customer_id, [])


@tool
def calculate_discount(amount: int, tier: str) -> float:
    """
    Calculate customer discount based on tier.
    """

    if tier == "gold":
        return amount * 0.20

    if tier == "silver":
        return amount * 0.10

    return 0


llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
agent = create_agent(model=llm, tools=[get_customer, get_orders, calculate_discount])

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content="""
                Customer 101 wants to buy again. Find his customer tier, check previous order total,
                and calculate eligible discount.
                """
            )
        ]
    }
)

for msg in result["messages"]:
    msg.pretty_print()
