import streamlit as st


def initialize_chat_memory() -> None:
    """
    Initialize the chat memory in Streamlit session state.

    This function ensures that the conversation history is available
    in `st.session_state`. If it does not exist, it creates an empty list.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = []


def add_messages(
    role: str,
    content: str,
) -> None:
    """
    Add a message to the chat history.

    Args:
        role:
            The role of the message sender (e.g., "user", "assistant").

        content:
            The textual content of the message to store.

    Returns:
        None
    """

    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
        }
    )


def get_chat_history() -> list[dict]:
    """
    Retrieve the full chat history stored in the session state.

    Returns:
        A list of message dictionaries containing the conversation history.
        Each message has the format:
        {
            "role": str,
            "content": str
        }
    """

    return st.session_state.messages
