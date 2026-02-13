from fastapi import APIRouter

from database.tables import messages, bots
from routers.schemas import *

router = APIRouter(
    prefix="/api/v0/user"
)

@router.get("/messages", tags=["Test API"])
async def get_all_messages():
    # TODO: ПРОВЕРКА АВТОРИЗАЦИИ
    msg_list = await messages.get_all()
    message_schemas = []
    for msg in msg_list:
         message_schemas.append(messages.MessageSchema.model_validate(msg))
    return message_schemas
    
@router.post("/message", summary="Send user message")
async def send_user_message(body: UserMessageBodySchema):
    # АВТОРИЗАЦИЯ ПО КУКИ ПОЛЬЗОВАТЕЛЯ
    message = messages.Message(
        by_bot = False,
        bot_id = body.bot_id,
        content = body.content,
        seen_by_bot = False
    )

    message = await messages.save_message(message)
    return message

@router.post("/bot", summary="Make a new bot")
async def create_bot(body: CreateBotBodySchema):
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