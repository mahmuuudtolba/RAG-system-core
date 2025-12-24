from datetime import datetime
from typing import List , Optional

from pydantic import BaseModel , Field , ConfigDict

class ConversationResponse(BaseModel):
    id:str 
    user_id : str
    title : str
    created_at : datetime
    updated_at : datetime
    message_count: int 

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls , conversation) -> "ConversationResponse":
        " output DTO "
        return cls(
            id = conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            created_at = conversation.created_at,
            updated_at=conversation.updated_at ,
            message_count=len(conversation.messages),
        )


class ConversationCreateRequest(BaseModel):
    """Request model for creating a new conversation"""
    title:Optional[str] = Field(None,description="Optional custom title (auto-generated if not provided)")

class ConversationUpdateRequest(BaseModel):
    """Request model for updating a conversation"""
    title: str = Field(..., min_length=1, max_length=200, description="New conversation title")




class ConversationListResponse(BaseModel):
    """Response model for paginated conversation list"""
    conversations: List[ConversationResponse]
    total: int
    limit: int
    offset: int


