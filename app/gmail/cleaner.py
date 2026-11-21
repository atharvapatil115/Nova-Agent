import re
from html import unescape


def clean_email_body(body: str) -> str:
    """
    Converts raw email content into cleaner plain text.
    """

    # Decode HTML entities such as &amp; and &nbsp;
    body = unescape(body)

    # Remove HTML tags
    body = re.sub(r"<[^>]+>", " ", body)

    # Remove invisible Unicode characters
    body = re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", body)

    # Normalize whitespace
    body = re.sub(r"[ \t]+", " ", body)

    # Remove excessive blank lines
    body = re.sub(r"\n\s*\n+", "\n\n", body)

    return body.strip()