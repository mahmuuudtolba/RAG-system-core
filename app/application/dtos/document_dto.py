from datetime import datetime
from typing import List


from pydantic import BaseModel , Field , ConfigDict



class DocumentResponse(BaseModel):
    id : str 
    filename: str
    created_at : datetime
    user_id : str
    content_preview: str = Field(
        ...,description="First 200 character of document content"
    )

    model_config = ConfigDict(from_attributes = True)

    @classmethod
    def from_entity(cls, document) -> "DocumentResponse":
        """Create DocumentResponse from Document entity"""
        content = document.content or ""
        preview = content[:200] if len(content) > 200 else content
        
        return cls(
            id=document.id,
            filename=document.filename,
            created_at=document.created_at,
            user_id=document.user_id,
            content_preview=preview
        )




class DocumentListResponse(BaseModel):
    documents : List[DocumentResponse]
    total:int
    limit : int
    offset : int

class DocumentSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=100)
