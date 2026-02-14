import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import INTEGER, VARCHAR, select
from pydantic import BaseModel, Field, ConfigDict

from database.database import Base, database

class BotSchema(BaseModel):
    id: int
    name: str = Field(max_length=32)
    description: str = Field(max_length=255)
    token: str = Field(max_length=64)
    model_config = ConfigDict(from_attributes=True)

class Bot(Base):
    __tablename__ = "bots"
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(32))
    description: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    token: Mapped[str] = mapped_column(VARCHAR(64))
    
    @staticmethod
    def from_schema(schema: BotSchema):
        bot = Bot(**schema.model_dump())
        bot.id = None
        return bot


async def get_all():
    """
    Get all bots
    :return: List of Bot objects
    """
    async with database.Session() as session:
        query = select(Bot)
        result = await session.execute(query)
        return result.scalars().all()

async def create_new(name: str, description: str) -> Bot:
    """
    Create new bot and generate token
    :param name: Name of bot (64 chars max)
    :param description: Description of bot (255 chars max)
    :return: Bot object
    """
    async with database.Session() as session:
        bot = Bot(
            name=name,
            description=description,
            token=uuid.uuid4().hex
        )
        session.add(bot)
        await session.commit()
        await session.refresh(bot)

        return bot
        
async def get_by_token(token: str) -> Bot | None:
    """
    Find bot by token
    :param token: Bot's token
    :return: Bot or None
    """
    async with database.Session() as session:
        query = select(Bot).where(Bot.token == token)
        result = await session.execute(query)
        bot = result.scalars().all()

        if len(bot) == 0:
            return None
        else:
            return bot[0]