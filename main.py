from fastapi import FastAPI

from ai_assistant_platform.api.routers.chat import (
    router as chat_router,
)

"""FastAPI application initialization and router registration module."""

app = FastAPI(
    title="AI Assistant Platform",
    version="2.0.0",
)

app.include_router(chat_router)
