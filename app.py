import streamlit as st

from ai_assistant_platform.memory.chat_memory import (
    add_message,
    get_chat_history,
    initialize_chat_memory,
)
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)


def get_orchestrator() -> ChatbotOrchestrator:
    """
    Singleton simples via Streamlit session_state
    Evita recriação a cada input
    """

    if "orchestrator" not in st.session_state:

        st.session_state.orchestrator = ChatbotOrchestrator()

    return st.session_state.orchestrator


def main() -> None:

    initialize_chat_memory()

    st.title("AI Assistant Platform")

    # render chat history
    for message in get_chat_history():
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Type your message")

    if not user_input:
        return

    # 1. salva user message
    add_message(role="user", content=user_input)

    orchestrator = get_orchestrator()

    # 2. chama pipeline completo (orchestrator controla tudo)
    with st.spinner("Thinking..."):

        try:
            result = orchestrator.process_message(
                user_message=user_input,
                conversation_history=get_chat_history(),
            )

        except RuntimeError as exc:

            result = {
                "response": str(exc),
                "metadata": {},
            }

    # 3. salva resposta
    add_message(
        role="assistant",
        content=result["response"],
        metadata=result.get("metadata", {}),
    )

    st.rerun()


if __name__ == "__main__":
    main()
