from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from ai_assistant_platform.api.dependencies import (
    get_chatbot_orchestrator,
)
from ai_assistant_platform.api.schemas import ChatRequest
from ai_assistant_platform.api.schemas import ChatResponse
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def send_message(
    request: ChatRequest,
    orchestrator: Annotated[
        ChatbotOrchestrator,
        Depends(get_chatbot_orchestrator),
    ],
) -> ChatResponse:
    """Handles incoming chat messages and generates assistant responses.

    Args:
        request (ChatRequest): The payload containing conversation history and message context.
        orchestrator (ChatbotOrchestrator): The injected orchestrator instance
            responsible for processing the chat conversation.

    Returns:
        ChatResponse: The generated chat response model containing response content and metadata.
    """
    _ = request
    _ = orchestrator

    return ChatResponse(
        content="FastAPI is running.",
        metadata=None,
    )
