import streamlit as st
from ai_assistant_platform.memory.chat_memory import (
    initialize_chat_memory,
    add_messages,
    get_chat_history,
)
from ai_assistant_platform.llm.llm_services import LLMService

initialize_chat_memory()

st.title("AI Chatbot Agent.")

for message in get_chat_history():
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message")

if user_input:
    add_messages(role="user", content=user_input)

    assistant_response = generate_response(get_chat_history())

    add_messages(role="assistant", content=assistant_response)

    st.rerun()
