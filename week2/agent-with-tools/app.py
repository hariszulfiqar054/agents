import asyncio
import os

from agents import Agent, OpenAIChatCompletionsModel, Runner, SQLiteSession
from dotenv import load_dotenv
from openai import AsyncOpenAI


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "stealth/ox-alpha"
load_dotenv()

def create_agent() -> Agent:
    client = AsyncOpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
    model = OpenAIChatCompletionsModel(
        model=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
        openai_client=client,
    )
    return Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=model,
    )


async def main() -> None:
    session = SQLiteSession("agent_memory.db")
    agent = create_agent()
    result = await Runner.run(
        agent,
        "my name is haris",
        session=session
    )
    print(result.final_output)
    result = await Runner.run(
        agent,
        "what is my name ?",
        session=session
    )
    print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())