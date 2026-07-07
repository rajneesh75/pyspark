import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
load_dotenv()


async def main() -> None:
    client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.environ["OPENAI_API_KEY"],  # hard fail if missing
    )
    agent = AssistantAgent("assistant", client)
    print(await agent.run(task="Say 'Hello World!'"))


asyncio.run(main())
