from pydantic import BaseModel, Field


class EmailDraft(BaseModel):
    recipient: str = Field(description="Email address of the recipient")
    subject: str = Field(description="Clear and concise email subject")
    body: str = Field(description="Complete email body")


class EmailAction(BaseModel):
    action: str = Field(
        description="What to do with the email: draft or send"
    )
    email: EmailDraft