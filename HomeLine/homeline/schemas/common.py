from pydantic import BaseModel
from typing import Optional

class WebhookResponse(BaseModel):
    """
    Standard response format that Voice AI Assistants ingest smoothly.
    Keeps responses concise and TTS optimized.
    """
    response: str
