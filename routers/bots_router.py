from fastapi import APIRouter
from pydantic import BaseModel, Field

from database import database
from database.tables import messages
from routers.schemas import *

router = APIRouter(
    prefix="/api/v0/bot",
)

@router.post("/message", summary="Send bot message")
async def send_bot_message(body: MessageBodySchema):
    # АВТОРИЗАЦИЯ ПО ТОКЕНУ БОТА
    message = messages.Message(
        by_bot = True,
        bot_id = body.bot_id,
        content = body.content,
        seen_by_bot = True
    )
    
    await messages.save_message(message)
    
@router.get("/update/{bot_id}", summary="Bot update")
async def bot_update(bot_id: int):
    # АВТОРЗАЦИЯ ПО ТОКЕНУ БОТА
    msg_list = await messages.get_for_bot_update(bot_id)
    
    message_schemas = []
    for msg in msg_list:
        message_schemas.append(messages.MessageSchema.model_validate(msg))
    return message_schemas
    
@router.put("/seen", summary="Mark user message as seen by bot")
async def seen_by_bot(body: SeenByBotBodySchema):
    # ПРОВЕРИТЬ АВТОРИЗАЦИЮ ПО ТОКЕНУ ОТ БОТА С bot_id
    status = await messages.mark_as_seen(body.message_id, body.bot_id)
    return { "status" : status }