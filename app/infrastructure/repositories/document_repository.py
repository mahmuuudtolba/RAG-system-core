from typing import List , Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , delete  as sql_delete , func
from datetime import datetime


from app.domain.exceptions import DocumentNotFoundError

from app.application.interfaces.document_repository import IDocumentRepositroy
from app.domain.entities.document import Document as DomainDocument
from app.infrastructure.database.models import Document as DBDocument 


class DocumentRepository(IDocumentRepositroy):
    """
    SQLAlchemy implementation of document repositroy
    """
    def __init__(self , session:AsyncSession):
        self.session = session

    async def save(self , document :DomainDocument) -> DomainDocument:
        """Save or update a document"""
        # Convert domain entity to database model
        db_document = DBDocument(
            id = int(document.id) if document.id else None,
            filename = document.filename ,
            content = document.content , 
            user_id = int(document.user_id),
            created_at = document.created_at
        )

        self.session.add(db_document)
        await self.session.commit()
        await self.session.refresh(db_document)

        return self._to_domain(db_document)


    async def get_by_id(self , document_id :str) -> Optional[DomainDocument]:
        """Get document by ID"""
        result = await self.session.execute(
            select(DBDocument).where(DBDocument.id == int(document_id))
        )

        db_document = result.scalar_one_or_none()
        if db_document is None:
            return None

        return self._to_domain(db_document)

    async def get_by_filename(self, filename: str, user_id: str) -> Optional[DomainDocument]:
        """Get document by filename for a specific user"""
        result = await self.session.execute(
            select(DBDocument).where(
                DBDocument.user_id == int(user_id),
                DBDocument.filename == filename)
        )
        db_document = result.scalar_one_or_none()
        if db_document is None:
            return None
        return self._to_domain(db_document)
        

    async def list_by_user(self, user_id: str, limit: int = 50, offset: int = 0) -> List[DomainDocument]:
        """List documents for a user with pagination"""
        result = await self.session.execute(
            select(DBDocument).where(
                DBDocument.user_id == int(user_id)
            ).offset(offset).limit(limit)
        )
        db_documents = result.scalars().all()
        if db_documents is None:
            return []

        return [self._to_domain(doc) for doc in db_documents]


        

    async def delete(self, document_id: str) -> None:
        """Delete a document"""
        result = await self.session.execute(
            select(DBDocument).where(DBDocument.id == int(document_id))
        )

        db_document = result.scalar_one_or_none()

        if db_document is None:
            raise DocumentNotFoundError()

        await self.session.delete(db_document)
        await self.session.commit()
   
        

    async def exists(self, document_id: str) -> bool:
        """Check if document exists"""
        result = await self.session.execute(
            select(DBDocument).where(DBDocument.id == int(document_id))
        )

        db_document = result.scalar_one_or_none()

        if db_document is None:
            return False

        return True


    async def count_by_user(self , user_id:str) ->int:
        """Count total documents for a user"""
        result = await self.session.execute(
            select(func.count(DBDocument.id)).where(DBDocument.user_id == int(user_id))
         )
        count = result.scalar_one()

        return count




    async def search_by_user(self,
                             user_id:str,
                             query:str,
                             limit:int =10) -> List[DomainDocument]:
        """Search documents by content for a user"""
        pattern = f"%{query}%"
        result = await self.session.execute(
            select(DBDocument)
            .where(DBDocument.user_id == int(user_id))
            .where(DBDocument.content.ilike(pattern))
            .limit(limit)
         )
        documents = result.scalars().all()

        return [self._to_domain(doc) for doc in documents]

    

    def _to_domain(self, db_document: DBDocument) -> DomainDocument:
        """Convert database model to domain entity"""
        return DomainDocument(
            id=str(db_document.id),
            filename=db_document.filename,
            content=db_document.content,
            created_at=db_document.created_at,
            user_id=str(db_document.user_id),
            chunks=[]  # Chunks are computed on demand, not stored
        )