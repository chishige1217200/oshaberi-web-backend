from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class Message:
    def __init__(self, chat_id: int, id: int, language_id: str, role: str, content: str, audio_path: str, upd_datetime: str):
        self.chat_id = chat_id
        self.id = id
        self.language_id = language_id
        self.role = role
        self.content = content
        self.audio_path = audio_path
        self.upd_datetime = upd_datetime


class CreateChatRequest(BaseModel):
    character_id: int


class ChatRequest(BaseModel):
    chat_id: int
    content: str


class OllamaMessageRequest(BaseModel):
    role: str
    content: str
