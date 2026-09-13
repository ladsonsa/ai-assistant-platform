from ai_assistant_platform.api.exceptions import (
    EmptyConversationError,
)
from ai_assistant_platform.api.mappers import (
    ChatResponseMapper,
)
from ai_assistant_platform.api.schemas import (
    ChatRequestSchema,
)
from ai_assistant_platform.api.schemas import (
    ChatResponseSchema,
)
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)


class ChatService:
    """Service layer handling business logic for interactive chat conversations.

    Attributes:
        _orchestrator (ChatbotOrchestrator): The orchestrator instance used to process
            and coordinate chat operations.
    """

    def __init__(
        self,
        orchestrator: ChatbotOrchestrator,
    ) -> None:
        """Initializes the ChatService with a chatbot orchestrator dependency.

        Args:
            orchestrator (ChatbotOrchestrator): The orchestrator instance responsible
                for coordinating chatbot execution.
        """
        self._orchestrator = orchestrator

    async def send(
        self,
        request: ChatRequestSchema,
    ) -> ChatResponseSchema:
        """Processes an incoming chat request, executing orchestrated message flow and mapping the response.

        Args:
            request (ChatRequest): Request object containing the conversation history and metadata.

        Returns:
            ChatResponse: Transformed chat response schema containing the orchestrator result.

        Raises:
            EmptyConversationError: If the provided conversation history in the request is empty.
        """
        if not request.history:
            raise EmptyConversationError()

        history = [
            {
                "role": message.role,
                "content": message.content,
                "metadata": message.metadata or {},
            }
            for message in request.history
        ]

        user_message = history[-1]["content"]
        conversation_history = history[:-1]

        response = self._orchestrator.process_message(
            user_message=user_message,
            conversation_history=conversation_history,
        )

        return ChatResponseMapper.to_schema(
            response=response,
        )
