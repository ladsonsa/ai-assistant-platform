from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)
from ai_assistant_platform.services import ChatService


def get_chatbot_orchestrator() -> ChatbotOrchestrator:
    """Instantiates and retrieves a ChatbotOrchestrator instance.

    Returns:
        ChatbotOrchestrator: A newly initialized chatbot orchestrator object.
    """
    return ChatbotOrchestrator()


def get_chat_service() -> ChatService:
    """Instantiates and retrieves a ChatService instance configured with its dependencies.

    Returns:
        ChatService: A newly initialized chat service injected with a
            ChatbotOrchestrator instance.
    """
    return ChatService(
        orchestrator=get_chatbot_orchestrator(),
    )
