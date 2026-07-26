import streamlit as st

from ai_assistant_platform.config.logging_config import (
    get_logger,
)

logger = get_logger(__name__)


def initialize_chat_memory() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
        logger.info("Chat memory initialized")
        return

    logger.debug(
        "Chat memory already initialized size=%d",
        len(st.session_state.messages),
    )


def add_message(
    role: str,
    content: str,
    metadata: dict | None = None,
) -> None:
    message = {
        "role": role,
        "content": content,
        "metadata": metadata or {},
    }

    st.session_state.messages.append(
        message,
    )

    logger.debug(
        "Message added role=%s has_metadata=%s history_size=%d",
        role,
        bool(metadata),
        len(st.session_state.messages),
    )


def get_chat_history() -> list[dict]:
    history = st.session_state.get(
        "messages",
        [],
    )

    logger.debug(
        "Chat history requested size=%d",
        len(history),
    )

    return history


def get_last_math_result() -> float | None:
    for message in reversed(
        st.session_state.get(
            "messages",
            [],
        )
    ):
        metadata = message.get(
            "metadata",
            {},
        )

        if "math_result" in metadata:
            logger.debug(
                "Last math result found value=%s",
                metadata["math_result"],
            )
            return metadata["math_result"]

    logger.debug("No math result found in chat history")
    return None
