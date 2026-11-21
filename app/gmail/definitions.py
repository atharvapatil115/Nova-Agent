READ_UNREAD_EMAILS_DEFINITION = {
    "type": "function",
    "function": {
        "name": "read_unread_emails",
        "description": (
            "Read the user's unread emails from Gmail. "
            "Use this when the user asks about unread, "
            "new, or pending emails."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": (
                        "Maximum number of unread emails "
                        "to retrieve."
                    ),
                    "default": 4,
                }
            },
            "required": [],
        },
    },
}

COMPOSE_EMAIL_TOOL = {
    "type": "function",
    "function": {
        "name": "compose_email",
        "description": (
            "Create an email and save it directly to the user's Gmail "
            "Drafts. This tool does not send the email."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string",
                    "description": (
                        "The recipient's email address. "
                        "Never invent an email address."
                    ),
                },
                "subject": {
                    "type": "string",
                    "description": (
                        "A clear, concise subject for the email."
                    ),
                },
                "body": {
                    "type": "string",
                    "description": (
                        "The complete natural email body."
                    ),
                },
            },
            "required": [
                "recipient",
                "subject",
                "body",
            ],
        },
    },
}