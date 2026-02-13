from fastapi import FastAPI
from uvicorn import run
import asyncio

from routers import user_router, bots_router
from database import database

app = FastAPI()
    
app.include_router(
    user_router.router,
    tags=["User API"]
)
app.include_router(
    bots_router.router,
    tags=["Bot API"]
)

if __name__ == "__main__":
    asyncio.run(database.init())
    run(app)
