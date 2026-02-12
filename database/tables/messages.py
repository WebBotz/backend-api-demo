from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import INTEGER, Boolean, VARCHAR, select, update
from pydantic import BaseModel, Field, ConfigDict

from database.database import Base, database

class MessageSchema(BaseModel):
    id: int
    bot_id: int
    by_bot: bool
    content: str = Field(max_length=2048)
    seen_by_bot: bool
    model_config = ConfigDict(from_attributes=True)

class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    bot_id: Mapped[int] = mapped_column(INTEGER) # Bot id
    by_bot: Mapped[bool] = mapped_column(Boolean)
    content: Mapped[str] = mapped_column(VARCHAR(2048))
    seen_by_bot: Mapped[bool] = mapped_column(Boolean)
    
    @staticmethod
    def from_schema(schema: MessageSchema):
        message = Message(**schema.model_dump())
        message.id = None
        return message
    

async def get_all():
    """
    Get all messages
    :return: Message list
    """
    async with database.Session() as session:
        query = select(Message)
        result = await session.execute(query)
        return result.scalars().all()
        
async def get_by_bot_id(bot_id: int):
    """
    Get all messages sent to bot
    :param bot_id: Bot id
    :return: Message list
    """
    async with database.Session() as session:
        query = select(Message).where(Message.bot_id == bot_id)
        
        result = await session.execute(query)
        return result.scalars().all()
        
async def get_for_bot_update(bot_id: int):
    """
    Get new messages sent to bot by users, but not seen yet
    """
    async with database.Session() as session:
        query = select(Message).where(Message.bot_id == bot_id, Message.by_bot == False, Message.seen_by_bot == False)
        
        result = await session.execute(query)
        return result.scalars().all()
        
async def save_message(message: Message):
    """
    Save new message
    :param message: Message object
    :return: Created message
    """
    async with database.Session() as session:
        session.merge(message)
        await session.commit()
        await session.refresh(message)

        return message
        
async def mark_as_seen(message_id: int):
    """
    Mark message as seen (handled) by bot
    :param message_id: Message id
    :return: Status
    """
    async with database.Session() as session:
        query = update(Message).where(Message.id==message_id).values(seen_by_bot=True)
        result = await session.execute(query)
        await session.commit()
        return result != 0