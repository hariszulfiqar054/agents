from schema import EmailReview
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel,Runner
from dotenv import load_dotenv
import asyncio
import os
load_dotenv()


def agentModelSetup():
  client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
  model = OpenAIChatCompletionsModel(openai_client=client, model="dots-studio/dots-3-note-preview:free")
  return model


async def main():
  email = "Hey there, I hope you're doing well. Just wanted to check in and see if you had a chance to look at the proposal I sent over. Let me know your thoughts when you get a chance. Thanks!"
  model = agentModelSetup()
  email_review_agent = Agent(name="Email Review Agent", instructions="You are an email review agent. Your task is to analyze the given email and provide a structured output based on the EmailReview schema.", model=model, output_type=EmailReview)
  result = await Runner.run(email_review_agent, email)
  print(result.final_output)



if __name__ == "__main__":
  asyncio.run(main())