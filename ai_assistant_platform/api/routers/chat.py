from fastapi import APIRouter, Depends, status

from ai_assistant_platform.api.dependencies import get_chat_service
from ai_assistant_platform.api.schemas.chat_request import ChatRequestSchema
from ai_assistant_platform.api.schemas.chat_response import ChatResponseSchema
from ai_assistant_platform.services import ChatService

router = APIRouter(tags=["Chat"])


@router.post(
    "/chat",
    response_model=ChatResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def chat_endpoint(
    request: ChatRequestSchema,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponseSchema:
    """Handles the HTTP POST endpoint for processing chat messages and interactions.

    Args:
        request (ChatRequestSchema): The request body containing conversation payload and history.
        chat_service (ChatService): The chat service injected via dependency injection.

    Returns:
        ChatResponseSchema: The processed response containing generated chat output.
    """
    return await chat_service.send(request)
