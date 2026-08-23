import asyncio
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, ResultMessage, StreamEvent
# from langsmith.integrations.claude_agent_sdk import configure_claude_agent_sdk

load_dotenv(override=True)

# configure_claude_agent_sdk()


async def main():
    options = ClaudeAgentOptions(
        system_prompt="you are a joke teller",
        model="claude-haiku-4-5-20251001",
        include_partial_messages=True,
    )
    async with ClaudeSDKClient(options=options) as client:
        await client.query("tell me 5 jokes")
        async for message in client.receive_response():
            if isinstance(message, StreamEvent):
                event = message.event
                if event.get("type") == "content_block_delta":
                    text = event.get("delta", {}).get("text")
                    if text:
                        print(text, end="", flush=True)
            elif isinstance(message, ResultMessage):
                print()


asyncio.run(main())
