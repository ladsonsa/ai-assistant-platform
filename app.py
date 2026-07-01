"""
Streamlit application entrypoint.

This module defines the main UI loop for the AI Assistant Platform.
It is responsible for rendering the chat interface, managing user
interaction, and coordinating communication between memory storage
and the chatbot orchestrator.

The application follows a modular architecture where:
- Chat memory is handled by a dedicated memory module.
- Message processing is delegated to the ChatbotOrchestrator.
- Specialized agents handle reasoning and response formatting.

Attributes / Components Used:
    ChatMemory:
        Provides functions to initialize, store, and retrieve chat history.

    ChatbotOrchestrator:
        Coordinates interaction between agents and manages message flow.

    MathematicalAgent:
        Handles mathematical reasoning and computation tasks.

    WriterAgent:
        Formats and transforms raw outputs into natural language responses.
"""

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
    Run the Streamlit chat application.

    This function initializes session state, renders the chat UI,
    processes user input through the orchestrator, and updates
    the conversation history.

    Returns:
        None
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

        add_messages(
            role="assistant",
            content=assistant_response,
        )

        st.rerun()


if __name__ == "__main__":
    main()
