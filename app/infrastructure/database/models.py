from sqlalchemy.sql.functions import func
from datetime import datetime
from sqlalchemy import ForeignKey , Text
from sqlalchemy.orm import DeclarativeBase , mapped_column , Mapped , relationship
from typing import List

class Base(DeclarativeBase):
    pass 

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str] = mapped_column(unique = True)
    created_at:Mapped[datetime] = mapped_column(server_default = func.now())

    # Relationship one - to - many
    documents:Mapped[List[Document]] = relationship(back_populates = "user")
    conversations:Mapped[List[Conversation]]= relationship(back_populates = "user")




class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key = True)
    filename: Mapped[str] = mapped_column(nullable=False)
    created_at:Mapped[datetime] = mapped_column(server_default = func.now())
    content:Mapped[str] = mapped_column(Text)

    # Relationship 
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user:Mapped[User] = relationship(back_populates= "documents")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id:Mapped[int] = mapped_column(primary_key = True)
    conversation_id :Mapped[int] = mapped_column(
        ForeignKey("conversations.id"),
        nullable = False
    )
    role: Mapped[str] = mapped_column(nullable=False)  # "user", "assistant", "system"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    # Relation
    conversation:Mapped[Conversation] = relationship(
        back_populates="messages"

    )


class Conversation(Base):
    __tablename__ = "conversations"
    id:Mapped[int] = mapped_column(primary_key = True)
    user_id :Mapped[int] = mapped_column(ForeignKey("user.id"))
    title : Mapped[str]= mapped_column(default="New conversation")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now() , onupdate= func.now())

    # Relation
    user:Mapped[User] = relationship(back_populates = "conversations")
    messages:Mapped[List[ChatMessage]] = relationship(
        back_populates = "conversation" ,
        cascade = "all, delete-orphan"
    )







