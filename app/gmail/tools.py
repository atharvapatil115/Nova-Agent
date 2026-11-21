
from app.gmail.service import (
    get_unread_emails,
    get_email,
    create_draft,
)


def read_unread_emails(limit: int = 4):
    """Tool used by the agent to retrieve unread emails."""
    return get_unread_emails(limit=limit)


def read_email(message_id: str):
    """Tool used by the agent to retrieve the full content of a specific email."""
    return get_email(message_id)


def compose_email(
    recipient: str,
    subject: str,
    body: str,
):
    """
    Creates and saves an email as a Gmail draft.
    Does not send the email.
    """

    return create_draft(
        recipient=recipient,
        subject=subject,
        body=body,
    )