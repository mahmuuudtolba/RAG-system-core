from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker



engine = create_async_engine(settings.DATABASE_URL ,
                        echo= settings.DB_ECHO  ,
                        pool_size=settings.POOL_SIZE  ,
                        pool_timeout=settings.POOL_TIMEOUT ,
                        pool_recycle=settings.POOL_RECYCLE ,
                        pool_pre_ping=settings.POOL_PRE_PING ,
                        max_overflow =settings.MAX_OVERFLOW)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()