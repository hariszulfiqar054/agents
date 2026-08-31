
import os

from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, Runner, function_tool
from agents.extensions.visualization import draw_graph
import asyncio
from smtp import EmailSender
from openai import AsyncOpenAI
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "inclusionai/ling-3.0-flash-fin:free"

def create_agent(name, instructions, model_settings=ModelSettings(max_tokens=10000),tools=[]) -> Agent:
    client = AsyncOpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
    model = OpenAIChatCompletionsModel(
        model=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
        openai_client=client,
    )
    return Agent(
        name=name,
        instructions=instructions,
        model=model,
        model_settings=model_settings,
        tools=tools
    )



def setup():
  funny_email_tool = create_agent(name="Ali agent", instructions="Your tone will be funny").as_tool(tool_name="funny_email_tool",tool_description="This tool is used to generate emails with funny tone")
  professional_email_tool = create_agent(name="Haris agent", instructions="Your tone will be professional").as_tool(tool_name="professional_email_tool",tool_description="This tool is used to generate emails with professional tone.")
  strategic_email_tool = create_agent(name="Atif agent", instructions="Your tone will be strategic").as_tool(tool_name="strategic_email_tool",tool_description="This tool is used to generate emails with strategic tone")

  return [funny_email_tool, professional_email_tool, strategic_email_tool]

async def email_sender():
  funny_email_tool, professional_email_tool, strategic_email_tool =  setup()
  sales_agent = create_agent(name="Sales Agent", instructions="You're a sales agent responsible for sending emails. Select the tone that best fits the situation. You will be selling the software development services and you will curate a complete email by filling all the relevant fields.",model_settings = ModelSettings(tool_choice="required"),tools=[send_email,funny_email_tool, professional_email_tool, strategic_email_tool])

  sales_agent_result = await Runner.run(sales_agent, f"Curate the best email to send to a potential client who is interested in our software development services. The person name is Bohdan and the recipient email is hariszulfiqar054@gmail.com and send the email to the client you have tools to complete the job ")
  print(f"Best email: {sales_agent_result.final_output}")
  return sales_agent_result.final_output


@function_tool
def send_email(recipient_email: str, subject: str, body: str):
    """
    Send an email to the specified recipient with the given subject and body.

    Args:
        recipient_email (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The body of the email.
    """
    email_sender = EmailSender()
    email_sender.send_email(recipient_email, subject, body)
    return f"Email sent to {recipient_email} with subject '{subject}'."