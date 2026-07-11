# app.py

import streamlit as st


from ai_assistant_platform.memory.chat_memory import (
    add_message,
    get_chat_history,
    initialize_chat_memory,
)
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)

from chatbot.llm_service import LLMService


def main() -> None:
    """
    Streamlit application entry point.
    """

    st.set_page_config(
        page_title="AI Math Assistant",
        page_icon="🧮",
    )

    st.title("🧮 AI Math Assistant")

    initialize_chat_memory()

    llm_service = LLMService()

    orchestrator = ChatbotOrchestrator()

    for message in get_chat_history():

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your mathematical question...")

    if not user_input:
        return

    add_message(
        role="user",
        content=user_input,
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:

        result = orchestrator.process_message(
            user_message=user_input,
            conversation_history=get_chat_history(),
        )

        response = result["response"]

        metadata = result.get(
            "metadata",
            {},
        )

    except RuntimeError as exc:

        response = str(exc)

        metadata = {}

    except Exception:

        response = "An unexpected error occurred while processing " "your request."

        metadata = {}

    add_message(
        role="assistant",
        content=response,
        metadata=metadata,
    )

    with st.chat_message("assistant"):
        st.markdown(response)


if __name__ == "__main__":
    main()
