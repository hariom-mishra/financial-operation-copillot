from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.settings import settings
from sqlalchemy.orm import DeclarativeBase
from core.exceptions import DatabaseConnectionException

db_engine = create_async_engine(settings.DB_URL)

session = async_sessionmaker(db_engine)

class Base(DeclarativeBase):
    pass

async def get_db():
    try:
        db = session()
    except Exception as e:
        raise DatabaseConnectionException(f"Failed to open DB session: {e}")
    try:
        async with db:
            yield db
    except DatabaseConnectionException:
        raise
    except Exception:
        # Re-raise exceptions from route handlers without wrapping them
        raise
    
    
