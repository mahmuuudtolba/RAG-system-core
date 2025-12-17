from abc import ABC , abstractmethod
from typing import List , Optional
from app.domain.entities.conversation import Conversation
from app.domain.entities.chat_message import ChatMessage


class IConversationRepository(ABC):
    """Repository interface for conversation operations"""

    @abstractmethod
    async def save(self , conversation : Conversation) -> Conversation:
        """Save or update conversation metadata (without messages)"""
        pass

    @abstractmethod
    async def get_by_id(self, conversation_id: str, include_messages: bool = True) -> Optional[Conversation]:
        """Get conversation by ID, optionally including messages"""
        pass

    @abstractmethod
    async def delete(self, conversation_id: str) -> None:
        """Delete a conversation and all its messages"""
        pass

    @abstractmethod
    async def exists(self, conversation_id: str) -> bool:
        """Check if conversation exists"""
        pass

    @abstractmethod
    async def list_by_user(self, user_id: str, limit: int = 50, offset: int = 0) -> List[Conversation]:
        """List conversations for a user with pagination (without messages)"""
        pass

    @abstractmethod
    async def count_by_user(self, user_id: str) -> int:
        """Count total conversations for a user"""
        pass

    @abstractmethod
    async def add_message(self, conversation_id: str, message: ChatMessage) -> ChatMessage:
        """Add a single message to a conversation"""
        pass

    @abstractmethod
    async def get_messages(self, conversation_id: str, limit: int = 100, offset: int = 0) -> List[ChatMessage]:
        """Get messages for a conversation with pagination"""
        pass

    @abstractmethod
    async def get_recent_messages(self, conversation_id: str, limit: int = 50) -> List[ChatMessage]:
        """Get the most recent N messages from a conversation"""
        pass