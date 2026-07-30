from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)


def get_chatbot_orchestrator() -> ChatbotOrchestrator:
    """Instantiates and retrieves a ChatbotOrchestrator instance.

    Returns:
        ChatbotOrchestrator: A newly initialized chatbot orchestrator object.
    """
    return ChatbotOrchestrator()