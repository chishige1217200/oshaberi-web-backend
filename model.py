from pydantic import BaseModel

class CreateChatRequest(BaseModel):
    character_id: int
