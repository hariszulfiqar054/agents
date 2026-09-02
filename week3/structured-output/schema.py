from pydantic import BaseModel, Field

class EmailReview(BaseModel):
  is_professional: bool = Field(description="Whether the email is professional or not.")
  contains_placeholder: bool = Field(description="Whether the email contains a placeholder or not.")
  summary: str = Field(description="A brief summary of the email's content.")
