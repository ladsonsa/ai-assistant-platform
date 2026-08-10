import logging
from fastapi import APIRouter, HTTPException, status
from ai_assistant_platform.api.schemas.chat_request import ChatRequestSchema
from ai_assistant_platform.api.schemas.chat_response import ChatResponseSchema
from ai_assistant_platform.orchestrators.chatbot_orchestrator import ChatbotOrchestrator

router = APIRouter(tags=["Chat"])
logger = logging.getLogger(__name__)

orchestrator = ChatbotOrchestrator()


@router.post(
    "/chat",
    response_model=ChatResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def chat_endpoint(request: ChatRequestSchema) -> ChatResponseSchema:
    """Handles incoming chat HTTP requests and processes conversation history.

    Args:
        request (ChatRequestSchema): The incoming request payload containing the
            conversation history.

    Returns:
        ChatResponseSchema: The generated response containing content and metadata.

    Raises:
        HTTPException:
            - 400 Bad Request if the conversation history is empty.
            - 500 Internal Server Error if an unexpected error occurs during processing.
    """
    try:
        if not request.history:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="History cannot be empty",
            )

        formatted_history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.history
        ]

        last_message = formatted_history[-1]["content"]
        previous_history = formatted_history[:-1]

        result = orchestrator.process_message(
            user_message=last_message,
            conversation_history=previous_history,
        )

        content = result.get("content") or result.get("response") or str(result)

        return ChatResponseSchema(
            content=content,
            metadata={},
        )
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Error while processing message in chatbot orchestrator")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )
