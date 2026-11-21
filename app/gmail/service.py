from app.gmail.auth import get_gmail_service
import base64
from app.gmail.cleaner import clean_email_body
from app.gmail.schemas import Email
from email.message import EmailMessage
def get_recent_emails(limit: int = 5):
    service = get_gmail_service()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=["INBOX"],
            maxResults=limit,
        )
        .execute()
    )

    messages = response.get("messages", [])

    emails = []

    for message in messages:
        message_id = message["id"]

        email = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="metadata",
                metadataHeaders=[
                    "From",
                    "Subject",
                    "Date",
                ],
            )
            .execute()
        )

        headers = email["payload"]["headers"]

        email_data = {
            "id": message_id,
            "from": None,
            "subject": None,
            "date": None,
            "snippet": email.get("snippet", ""),
        }

        for header in headers:
            name = header["name"]
            value = header["value"]

            if name == "From":
                email_data["from"] = value

            elif name == "Subject":
                email_data["subject"] = value

            elif name == "Date":
                email_data["date"] = value

        emails.append(email_data)

    return emails

def get_unread_emails(limit: int = 4):
    service = get_gmail_service()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=["INBOX", "UNREAD"],
            maxResults=limit,
        )
        .execute()
    )

    messages = response.get("messages", [])

    emails = []

    for message in messages:
        message_id = message["id"]

        email = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="metadata",
                metadataHeaders=[
                    "From",
                    "Subject",
                    "Date",
                ],
            )
            .execute()
        )

        headers = email["payload"]["headers"]

        email_data = {
            "id": message_id,
            "from": None,
            "subject": None,
            "date": None,
            "snippet": email.get("snippet", ""),
        }

        for header in headers:
            name = header["name"]
            value = header["value"]

            if name == "From":
                email_data["from"] = value

            elif name == "Subject":
                email_data["subject"] = value

            elif name == "Date":
                email_data["date"] = value

        emails.append(email_data)

    return emails


def extract_email_body(payload):
    """
    Recursively extracts the email body from Gmail's MIME payload.
    Prefers plain text and falls back to HTML.
    """

    # Case 1: This part directly contains the body
    mime_type = payload.get("mimeType")
    body_data = payload.get("body", {}).get("data")

    if body_data and mime_type == "text/plain":
        decoded = base64.urlsafe_b64decode(body_data)
        return decoded.decode("utf-8", errors="ignore")

    # Case 2: Multipart email
    parts = payload.get("parts", [])

    for part in parts:
        body = extract_email_body(part)

        if body:
            return body

    # Case 3: If there is no plain text, try HTML
    if body_data and mime_type == "text/html":
        decoded = base64.urlsafe_b64decode(body_data)
        return decoded.decode("utf-8", errors="ignore")

    return ""


def get_email(message_id: str):
    """
    Fetches the complete email using its Gmail message ID.
    """

    service = get_gmail_service()

    email = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="full",
        )
        .execute()
    )

    headers = email["payload"]["headers"]

    email_data = {
        "id": message_id,
        "from": None,
        "to": None,
        "subject": None,
        "date": None,
        "snippet": email.get("snippet", ""),
        "body": "",
    }

    for header in headers:
        name = header["name"]
        value = header["value"]

        if name == "From":
            email_data["from"] = value

        elif name == "To":
            email_data["to"] = value

        elif name == "Subject":
            email_data["subject"] = value

        elif name == "Date":
            email_data["date"] = value

    email_data["body"] = clean_email_body(
    extract_email_body(email["payload"])
)

    return Email(
        id=email_data["id"],
        sender=email_data["from"],
        recipient=email_data["to"],
        subject=email_data["subject"],
        date=email_data["date"],
        snippet=email_data["snippet"],
        body=email_data["body"],
    )



def create_draft(
    recipient: str,
    subject: str,
    body: str,
):
    """
    Creates a real Gmail draft.
    Does NOT send the email.
    """

    service = get_gmail_service()

    message = EmailMessage()

    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(body)

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    draft_body = {
        "message": {
            "raw": encoded_message
        }
    }

    draft = (
        service.users()
        .drafts()
        .create(
            userId="me",
            body=draft_body,
        )
        .execute()
    )

    return {
        "draft_id": draft["id"],
        "message_id": draft["message"]["id"],
        "recipient": recipient,
        "subject": subject,
        "body": body,
    }