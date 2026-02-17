from fastapi import APIRouter, HTTPException

from database.tables import messages, bots
from utils.schemas import *

router = APIRouter(
    prefix="/api/v0/bot",
)


@router.get("/bots-full", summary="Get all bot list", tags=["Test API"], deprecated=True)
async def get_all_bots():
    """
    Get full list of bots (WITH TOKENS). SHOULD NOT BE ABLE FOR USERS
    """
    # ЗАПРЕТИТЬ ДОСТУП К ЭТОМУ ЭНДПОИНТУ, ТК ОН ПОКАЗЫВАЕТ ТОКЕНЫ
    bot_list = await bots.get_all()
    bot_schemas = []
    for bot in bot_list:
        bot_schemas.append(bots.BotSchema.model_validate(bot))
    return bot_schemas


@router.post("/message", summary="Send bot message")
async def send_bot_message(body: BotMessageBodySchema):
    """
    Send message as bot
    """
    bot = await bots.get_by_token(body.bot_token)
    if bot is None:
        raise HTTPException(status_code=403, detail="Incorrect bot token")

    message = messages.Message(
        by_bot=True,
        bot_id=bot.id,
        content=body.content,
        seen_by_bot=True
    )

    message = await messages.save_message(message)
    return message


@router.get("/update/{token}", summary="Bot update")
async def bot_update(token: str):
    """
    Get user messages, sent to specified bot, but not seen (handled) yet
    """
    bot = await bots.get_by_token(token)
    if bot is None:
        raise HTTPException(status_code=403, detail="Incorrect bot token")

    msg_list = await messages.get_for_bot_update(bot.id)

    message_schemas = []
    for msg in msg_list:
        message_schemas.append(messages.MessageSchema.model_validate(msg))
    return message_schemas


@router.put("/seen", summary="Mark user message as seen by bot")
async def seen_by_bot(body: SeenByBotBodySchema):
    """
    Mark message as seen (handled)
    """
    bot = await bots.get_by_token(body.bot_token)
    if bot is None:
        raise HTTPException(status_code=403, detail="Incorrect bot token")

    status = await messages.mark_as_seen(body.message_id)
    return {"success": status}
