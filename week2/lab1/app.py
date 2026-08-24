import asyncio
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, ResultMessage, StreamEvent,create_sdk_mcp_server,tool
# from langsmith.integrations.claude_agent_sdk import configure_claude_agent_sdk

load_dotenv(override=True)

# configure_claude_agent_sdk()

@tool("joke_teller_tool","A tool that tells jokes",{"query":str})
async def joke_teller_tool(args):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "Why did the math book look sad? Because it had too many problems.",
        "Why did the tomato turn red? Because it saw the salad dressing!"
    ]
    return {"content":[{"type":"text","text":"\n".join(jokes)}]}


async def main():
    local_mcp_server =  create_sdk_mcp_server(name="joke-teller", tools=[joke_teller_tool])
    options = ClaudeAgentOptions(
        system_prompt="you are a joke teller",
        model="claude-haiku-4-5-20251001",
        include_partial_messages=True,
        mcp_servers={"joke": local_mcp_server},
        allowed_tools=["mcp__joke__joke_teller_tool"],
    )
    async with ClaudeSDKClient(options=options) as client:
        await client.query("tell me 3 jokes")
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
