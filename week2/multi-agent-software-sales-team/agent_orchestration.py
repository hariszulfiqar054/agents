
import os

from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, Runner, function_tool
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


def setup_agents_prompts():
  instructions = "The goal is to make people opt in for your software development services for the mobile and web development also ai powered applications. You will be crafting the email"
  funny_agent = instructions + " Your email style is a funny agent and you have to make the conversation funny and interesting."
  professional_agent = instructions + " Your email style is a professional agent and you have to make the conversation professional and interesting."
  strategic_agent = instructions + " Your email style is a strategic agent and you have to make the conversation strategic and interesting."
  return funny_agent, professional_agent, strategic_agent

async def setup():
  funny_agent, professional_agent, strategic_agent = setup_agents_prompts()
  funny_agent_runner = create_agent(name="Ali agent", instructions=funny_agent)
  professional_agent_runner = create_agent(name="Haris agent", instructions=professional_agent)
  strategic_agent_runner = create_agent(name="Atif agent", instructions=strategic_agent)
  results = await asyncio.gather(
    Runner.run(funny_agent_runner, "Write an email to a potential client to opt in for our software development services for the mobile and web development also ai powered applications. Name of the client is Bohdan"),
    Runner.run(professional_agent_runner, "Write an email to a potential client to opt in for our software development services for the mobile and web development also ai powered applications. Name of the client is Bohdan"),
    Runner.run(strategic_agent_runner, "Write an email to a potential client to opt in for our software development services for the mobile and web development also ai powered applications. Name of the client is Bohdan")
  )
   
  all_results = [result.final_output for result in results]
  return all_results

async def email_sender():
  all_results = await setup()
  email_sender_agent = create_agent(name="Email sender Agent", instructions="You are an email sender agent. Your task is to send the best email from the given emails. You have to send the best email based on the quality of the email and the style of the email.",model_settings = ModelSettings(tool_choice="required"),tools=[send_email])
  email_sender_result = await Runner.run(email_sender_agent, f"Here are the emails: {all_results}. Send the best email from the given emails. only extract the email don't add any other thing or text and send the email using the tool send_email. The email should be sent to the recipient email: hariszulfiqar054@gmail.com")
  print(f"Best email: {email_sender_result.final_output}")
  return email_sender_result.final_output


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