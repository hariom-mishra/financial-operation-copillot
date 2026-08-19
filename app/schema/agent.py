from pydantic import BaseModel
from typing import Any


class AgentChatRequest(BaseModel):
    message: str


class AgentChatResponse(BaseModel):
    reply: str
    tool_calls_made: list[str] = []
