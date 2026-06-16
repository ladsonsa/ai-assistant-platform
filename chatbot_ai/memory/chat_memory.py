import streamlit as st


def initialize_chat_memory() -> None:
    """
    Initialize conversation history.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []

def add_messages(
    role: str,
    content: str,
) -> None:
    """
    Add a messages to history.
    """
    st.session_state.messages.append(
        {
        "role": role,
        "content": content, 
        }
    )
    
def get_chat_history() -> list[dict]:

    """
    Return all conversation to history.
    """
    return st.session_state.messages

