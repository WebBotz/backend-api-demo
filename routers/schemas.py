from pydantic import BaseModel, Field

class UserMessageBodySchema(BaseModel):
    bot_id: int
    content: str = Field(max_length=2048)

class BotMessageBodySchema(BaseModel):
    bot_token: str
    content: str = Field(max_length=2048)

class SeenByBotBodySchema(BaseModel):
    bot_token: str
    message_id: int

class CreateBotBodySchema(BaseModel):
    name: str = Field(max_length=64)
    description: str = Field(max_length=2048)