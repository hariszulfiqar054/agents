import asyncio
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, ResultMessage, StreamEvent,create_sdk_mcp_server,tool

load_dotenv(override=True)

async def main():
  options= ClaudeAgentOptions(
    system_prompt="you are a assistant",
    model="claude-haiku-4-5-20251001",
  )
  async with ClaudeSDKClient(options=options) as client:
    await client.query("do you know my name ?")
    async for message in client.receive_response():
      if isinstance(message, ResultMessage) and message.result:
        print(message.result)


asyncio.run(main())
