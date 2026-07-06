import streamlit as st


def initialize_chat_memory() -> None:
    """
    Initialize the chat history stored in the Streamlit session state.

    This function creates the ``messages`` collection if it does not
    already exist, ensuring that the conversation history is available
    throughout the user's session.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = []


def add_message(
    role: str,
    content: str,
    metadata: dict | None = None,
) -> None:
    """
    Add a message to the conversation history.

    Args:
        role:
            Role of the message author (e.g. ``"user"`` or
            ``"assistant"``).

        content:
            Message content to store.

        metadata:
            Optional metadata associated with the message, such as
            mathematical results or operation details. Defaults to an
            empty dictionary.
    """

    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
            "metadata": metadata or {},
        }
    )


def get_chat_history() -> list[dict]:
    """
    Retrieve the current conversation history.

    Returns:
        A list of message dictionaries stored in the Streamlit session
        state. Each message contains the following fields:

        - ``role``: Message author.
        - ``content``: Message text.
        - ``metadata``: Optional contextual information associated with
          the message.
    """

    return st.session_state.messages
