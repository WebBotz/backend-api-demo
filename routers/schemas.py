from pydantic import BaseModel, Field, ConfigDict


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
    name: str = Field(max_length=32)
    description: str = Field(max_length=2048)

class BotPublicSchema(BaseModel):
    """
    Schema contains bot object without secret token
    """
    id: int
    name: str = Field(max_length=32)
    description: str = Field(max_length=255)

    model_config = ConfigDict(extra="ignore", from_attributes=True) # Removes token from schema
