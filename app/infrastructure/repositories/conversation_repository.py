from typing import List , Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select , delete as sql_delete ,func
from datetime import datetime

from app.domain.exceptions import ConversationNotFoundError


from app.application.interfaces.conversation_repository import IConversationRepository
from app.domain.entities.conversation import Conversation as DomainConversation
from app.infrastructure.database.models import Conversation as DBConversation
from app.infrastructure.database.models import ChatMessage as DBChatMessage
from app.domain.entities.chat_message import ChatMessage as DomainChatMessage
from app.domain.entities.chat_message import MessageRole 


class ConversationRepository(IConversationRepository):
    """
    SQLAlchemy implementation of conversation repositroy
    """
    def __init__(self , session:AsyncSession):
        self.session = session


    async def save(self , conversation : DomainConversation) -> DomainConversation:
        """
        Save or update conversation metadata [without messages]
        """
        db_conversation = DBConversation(
            id = int(conversation.id) if conversation.id else None ,
            user_id = int(conversation.user_id),
            title = conversation.title ,
        )
        self.session.add(db_conversation)
        await self.session.commit()
        await self.session.refresh(db_conversation)

        return self._to_domain(db_conversation)


    async def get_by_id(self, conversation_id: str, include_messages: bool = True) -> Optional[DomainConversation]:
        """Get conversation by ID, optionally including messages"""

        if include_messages:
            # Eager load messages from database
            result = await self.session.execute(
                select(DBConversation)
                .options(selectinload(DBConversation.messages))
                .where(DBConversation.id == int(conversation_id))
            )

        else:
            # Don't load messages
            result = await self.session.execute(
                select(DBConversation)
                .where(DBConversation.id == int(conversation_id))
            )

        db_conversation = result.scalar_one_or_none()
        if db_conversation is None :
            return None

        return self._to_domain(db_conversation=db_conversation , include_messages=include_messages)


    async def delete(self ,conversation_id:str) -> None:
        """Delete a conversation and all its messages"""
        result = await self.session.execute(
            select(DBConversation)
            .where(DBConversation.id == int(conversation_id))
        )

        db_conversation = result.scalar_one_or_none()

        if db_conversation is None:
            raise ConversationNotFoundError()

        await self.session.delete(db_conversation)
        await self.session.commit()

    async def exists(self , conversation_id:str) -> bool :
        """Check if conversation exists"""
        result = await self.session.execute(
            select(DBConversation)
            .where(DBConversation.id == int(conversation_id))
        )
        db_conversation  = result.scalar_one_or_none()

        if db_conversation is None:
            return False

        return True

    async def list_by_user(self, user_id: str, limit: int = 50, offset: int = 0) -> List[DomainConversation]:
        """List conversations for a user with pagination (without messages)"""
        result = await self.session.execute(
            select(DBConversation)
            .where(DBConversation.user_id == int(user_id))
            .offset(offset)
            .limit(limit)
        )

        db_conversations = result.scalars().all()
        if db_conversations is None:
            return []

        return [self._to_domain(con , include_messages=False) for con in db_conversations]
        
    async def count_by_user(self, user_id: str) -> int:
        """Count total conversations for a user"""
        result = await self.session.execute(
            select(func.count(DBConversation.id)).where(DBConversation.user_id == int(user_id))
        )
        count = result.scalar_one()
        
        return count

    async def add_message(self, conversation_id: str, message: DomainChatMessage) -> DomainChatMessage:
        """Add a single message to a conversation"""
        is_exist = await self.exists(conversation_id)
        if not is_exist:
            raise ConversationNotFoundError()
            
        db_message = DBChatMessage(
            conversation_id = int(conversation_id),
            role = MessageRole(message.role) ,
            content = message.content,
            created_at = message.created_at
        )
        self.session.add(db_message)
        await self.session.commit()
        await self.session.refresh(db_message)
        return self._message_to_domain(db_message)
        

    async def get_messages(self, conversation_id: str, limit: int = 100, offset: int = 0) -> List[DomainChatMessage]:
        """Get messages for a conversation with pagination"""
        is_exist = await self.exists(conversation_id)
        if not is_exist:
            raise ConversationNotFoundError()

        result = await self.session.execute(
            select(DBChatMessage)
            .where(DBChatMessage.conversation_id == int(conversation_id))
            .order_by(DBChatMessage.created_at.asc())
            .offset(offset)
            .limit(limit)
        )

        db_messages = result.scalars().all()
        return [self._message_to_domain(msg) for msg in db_messages]

    async def get_recent_messages(self, conversation_id: str, limit: int = 50) -> List[DomainChatMessage]:
        """Get the most recent N messages from a conversation"""
        is_exist = await self.exists(conversation_id)
        if not is_exist:
            raise ConversationNotFoundError()

        result = await self.session.execute(
            select(DBChatMessage)
            .where(DBChatMessage.conversation_id == int(conversation_id))
            .order_by(DBChatMessage.created_at.desc())
            .limit(limit)
        )

        db_messages = result.scalars().all()
        # Reverse to get chronological order (oldest to newest)
        return [self._message_to_domain(msg) for msg in reversed(db_messages)]











    def _message_to_domain(self , message :DBChatMessage ) -> DomainChatMessage:
        """
        Convert message database model to domain model
        """
        return DomainChatMessage(
            role = MessageRole(message.role),
            content=message.content,
            id =str(message.id),
            created_at=message.created_at
            

        )






    def _to_domain(self, db_conversation: DBConversation , include_messages:bool = True) -> DomainConversation:
        """Convert database model to domain entity"""

        # Conditionally load messages
        messages = []

        if include_messages and db_conversation.messages:
            messages = [self._message_to_domain(msg) for msg in db_conversation.messages]
        return DomainConversation(
            id=str(db_conversation.id),
            user_id=str(db_conversation.user_id),
            title=db_conversation.title,
            created_at=db_conversation.created_at,
            updated_at = db_conversation.updated_at,
            messages = messages
            

        )

