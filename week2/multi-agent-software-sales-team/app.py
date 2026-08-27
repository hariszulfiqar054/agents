import asyncio

from dotenv import load_dotenv

load_dotenv(override=True)
from agent_orchestration import email_sender



def main():
    asyncio.run(email_sender())

    # email_sender = EmailSender()
    # recipient_email = "hariszulfiqar054@gmail.com"
    # subject = "Test Email"
    # body = "This is a test email sent from the multi-agent sales team application."
    # email_sender.send_email(recipient_email, subject, body)

if __name__ == "__main__":
    main()