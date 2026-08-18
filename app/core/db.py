from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.settings import settings
from sqlalchemy.orm import DeclarativeBase

db_engine = create_async_engine(settings.DB_URL)

session = async_sessionmaker(db_engine)

class Base(DeclarativeBase):
    pass

async def get_db():
    try:
        async with session() as db:
            yield db
    except Exception as e:
        print(f"Database error: {e}")
        raise
    
    
