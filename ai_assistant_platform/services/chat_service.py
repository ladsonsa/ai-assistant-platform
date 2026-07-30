from ai_assistant_platform.api.schemas import ChatRequest
from ai_assistant_platform.api.schemas import ChatResponse
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)


class ChatService:
    """Provides business logic services for chat interactions.

    Attributes:
        _orchestrator (ChatbotOrchestrator): The orchestrator instance used to process
            and coordinate chat operations.
    """

    def __init__(
        self,
        orchestrator: ChatbotOrchestrator,
    ) -> None:
        """Initializes the ChatService with a chatbot orchestrator.

        Args:
            orchestrator (ChatbotOrchestrator): The orchestrator instance responsible
                for coordinating chatbot execution.
        """
        self._orchestrator = orchestrator

    async def send(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """Processes a chat request and returns a corresponding chat response.

        Args:
            request (ChatRequest): The incoming request payload containing conversation history.

        Returns:
            ChatResponse: The generated chat response model containing message content
                and optional metadata.
        """
        _ = request
        _ = self._orchestrator

        return ChatResponse(
            content="Service layer initialized.",
            metadata=None,
        )
