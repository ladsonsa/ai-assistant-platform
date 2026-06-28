import streamlit as st

from ai_assistant_platform.memory.chat_memory import (
    add_messages,
    get_chat_history,
    initialize_chat_memory,
)
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)
from ai_assistant_platform.agents.mathematical_agent import (
    MathematicalAgent,
)
from ai_assistant_platform.agents.writer_agent import (
    WriterAgent,
)


def main() -> None:
    """
    Streamlit application entrypoint.

    Responsibilities:
        - Render the chat interface.
        - Display conversation history.
        - Send user messages to the orchestrator.
        - Display assistant responses.

    Limitations:
        - Does not contain business logic.
        - Does not interact directly with LLM providers.
        - Does not perform calculations.
    """

    initialize_chat_memory()

    st.title("AI Assistant Platform")

    for message in get_chat_history():
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Type your message")

    if user_input:

        add_messages(
            role="user",
            content=user_input,
        )

        orchestrator = ChatbotOrchestrator(
            MathematicalAgent(),
            WriterAgent(),
        )

        with st.spinner("Thinking..."):
            assistant_response = orchestrator.process_message(
                user_message=user_input,
                conversation_history=get_chat_history(),
            )

        assistant_response = orchestrator.process_message(
            user_message=user_input,
            conversation_history=get_chat_history(),
        )

        add_messages(
            role="assistant",
            content=assistant_response,
        )

        st.rerun()


if __name__ == "__main__":
    main()
