from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class Base(DeclarativeBase):
    pass

class Database:
    def __init__(self):
        self.engine = create_async_engine("sqlite+aiosqlite:///./database.db")
        self.Session = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            class_=AsyncSession
        )
        
database: Database

async def init():
    global database
    database = Database()
    
    async with database.engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)
