from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import INTEGER, VARCHAR, select

from pydantic import BaseModel, Field

from database.database import Base, Database

class BotSchema(BaseModel):
    id: int
    name: str = Field(maxlength=64)
    description: str = Field(maxlength=255)
    token: str = Field(maxlength=64)

class Bot(Base):
    __tablename__ = "bots"
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(64))
    description: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    token: Mapped[str] = mapped_column(VARCHAR(64))
    
    @staticmethod
    def from_schema(schema: BotSchema):
        bot = Bot(**schema.model_dump())
        bot.id = None
        return bot
        
async def get_by_token(database: Database, token: str) -> Bot | None:
    async with database.Session() as session:
        query = select(Bot).where(Bot.token == token)
        result = await session.execute()
        bot = result.scalar()