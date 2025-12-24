from datetime import datetime
from typing import List , Optional
from app.domain.entities.chat_message import MessageRole 

from pydantic import BaseModel , Field , ConfigDict

class ChatMessageResponse(BaseModel):
    role : MessageRole
    content: str
    id:str
    created_at:datetime


    model_config = ConfigDict(from_attributes=True)


    @classmethod
    def from_entity(cls , chatmessage) -> "ChatMessageResponse":
        "Create ChatResponse from ChatMessage entity"

        return cls(
            role = chatmessage.role,
            content = chatmessage.content ,
            id = chatmessage.id,
            created_at=chatmessage.created_at,

            
        )

class ChatContextResponse(BaseModel):
    document_id: str
    filename: str
    chunk_text: str
    relevance_score: float = Field(...,ge=0.0 , le=1.0 , description="Similarity score (0-1)")

class ChatMessageRequest(BaseModel):
    """For incoming chat request"""
    message:str = Field(...,min_length=1 , max_length=10000)
    conversation_id : Optional[str] = None


class ChatResponse(BaseModel):
    message : ChatMessageResponse
    context : List[ChatContextResponse] = Field(default_factory=list)