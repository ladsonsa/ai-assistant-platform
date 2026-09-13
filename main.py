from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_assistant_platform.api.routers.chat import router as chat_router

"""FastAPI application module configuring CORS middleware and registering route handlers."""

app = FastAPI(
    title="AI Assistant Platform API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
