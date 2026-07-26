import streamlit as st

from ai_assistant_platform.config.logging_config import (
    get_logger,
)

logger = get_logger(__name__)


def initialize_chat_memory() -> None:
    """Initializes the chat memory in the Streamlit session state if it does not exist.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
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
    """Adds a new message with an optional metadata dictionary to the chat history.

    Args:
        role (str): The role of the message sender (e.g., 'user', 'assistant').
        content (str): The content of the message.
        metadata (dict | None): Optional metadata associated with the message. Defaults to None.

    Returns:
        None

    Raises:
        None
    """
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
    """Retrieves the complete chat history from the session state.

    Args:
        None

    Returns:
        list[dict]: A list of message dictionaries representing the chat history.

    Raises:
        None
    """
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
    """Finds and returns the most recent mathematical calculation result from the chat history metadata.

    Args:
        None

    Returns:
        float | None: The latest math result value as a float, or None if no result is found.

    Raises:
        None
    """
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
