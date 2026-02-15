from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
import asyncio

from routers import user_router, bots_router
from database import database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://127.0.0.1", "https://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
    
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
