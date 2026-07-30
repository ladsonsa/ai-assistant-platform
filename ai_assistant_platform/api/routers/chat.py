from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from ai_assistant_platform.api.dependencies import (
    get_chat_service,
)
from ai_assistant_platform.api.schemas import ChatRequest
from ai_assistant_platform.api.schemas import ChatResponse
from ai_assistant_platform.services import ChatService

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
    service: Annotated[
        ChatService,
        Depends(get_chat_service),
    ],
) -> ChatResponse:
    """Handles incoming chat messages and delegates execution to the chat service.

    Args:
        request (ChatRequest): The payload containing conversation history and message context.
        service (ChatService): The injected service instance responsible for processing
            the chat logic and interacting with the orchestrator.

    Returns:
        ChatResponse: The generated chat response model containing response content and metadata.
    """
    return await service.send(
        request=request,
    )
