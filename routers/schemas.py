from pydantic import BaseModel, Field

class UserMessageBodySchema(BaseModel):
    """
    Body schema for user's request to create new message
    """
    bot_id: int
    content: str = Field(max_length=2048)

class BotMessageBodySchema(BaseModel):
    """
    Body schema for bot's request to create new message
    """
    bot_token: str
    content: str = Field(max_length=2048)

class SeenByBotBodySchema(BaseModel):
    """
    Body schema for bot's request to mark message as seen (handled)
    """
    bot_token: str
    message_id: int

class CreateBotBodySchema(BaseModel):
    """
    Body schema for user's request to make a new bot
    """
    name: str = Field(max_length=64)
    description: str = Field(max_length=2048)