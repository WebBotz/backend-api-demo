from fastapi import APIRouter, Depends

from database.tables import messages, bots
from utils.schemas import *
from utils import auth

router = APIRouter(
    prefix="/api/v0/user",
    dependencies=[Depends(auth.verify_token_depend)]
)

@router.get("/messages", tags=["Test API"])
async def get_all_messages():
    """
    TEST API: Get all messages list
    """
    msg_list = await messages.get_all()
    message_schemas = []
    for msg in msg_list:
        message_schemas.append(messages.MessageSchema.model_validate(msg))
    return message_schemas


@router.get("/messages/{bot_id}/{last_id}")
async def get_messages(bot_id: int, last_id: int):
    """
    Get messages for user client by specified bot and last message id
    """
    msg_list = await messages.get_by_bot_and_from_id(bot_id, last_id)
    message_schemas = []
    for msg in msg_list:
        message_schemas.append(messages.MessageSchema.model_validate(msg))
    return message_schemas


@router.post("/message", summary="Send user message")
async def send_user_message(body: UserMessageBodySchema):
    """
    Send message as user
    """
    # АВТОРИЗАЦИЯ ПО КУКИ ПОЛЬЗОВАТЕЛЯ
    message = messages.Message(
        by_bot=False,
        bot_id=body.bot_id,
        content=body.content,
        seen_by_bot=False
    )

    message = await messages.save_message(message)
    return message


@router.post("/bot", summary="Make a new bot")
async def create_bot(body: CreateBotBodySchema):
    """
    Create new bot and get it
    """
    bot = await bots.create_new(body.name, body.description)
    return bot


@router.get("/bot-list", summary="Get public bot list")
async def get_bot_list():
    """
    Get list of bots (without tokens)
    """
    bot_list = await bots.get_all()
    bot_schemas = []
    for bot in bot_list:
        bot_schemas.append(BotPublicSchema.model_validate(bot))
    return bot_schemas
