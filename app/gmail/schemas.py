from pydantic import BaseModel

class Email(BaseModel):
    id                  : str
    sender              : str
    recipient           : str
    subject             : str
    date                : str
    snippet             : str
    body                : str