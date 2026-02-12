from pydantic import BaseModel, Field

class MessageBodySchema(BaseModel):
    bot_id: int
    content: str = Field(max_length=2048)

class SeenByBotBodySchema(BaseModel):
    bot_id: int
    message_id: int