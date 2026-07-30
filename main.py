from fastapi import FastAPI

from ai_assistant_platform.api.routers.chat import router as chat_router

app = FastAPI(
    title="AI Assistant Platform",
    version="2.0.0",
)
"""FastAPI: Primary application instance for the AI Assistant Platform API."""

app.include_router(chat_router)
