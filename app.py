import streamlit as st

from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.config.settings import (
    FREQUENCY_PENALTY,
    GEMINI_MODEL,
    MAX_TOKENS,
    OLLAMA_MODEL,
    OPENAI_MODEL,
    PRESENCE_PENALTY,
    PROVIDER_NAME,
    TEMPERATURE,
    TOP_P,
)
from ai_assistant_platform.llm.llm_service import (
    LLMService,
)
from ai_assistant_platform.memory.chat_memory import (
    add_message,
    get_chat_history,
    initialize_chat_memory,
)
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)

logger = get_logger("ai_assistant_platform.app")

PROVIDERS = {
    "openai": OPENAI_MODEL,
    "gemini": GEMINI_MODEL,
    "ollama": OLLAMA_MODEL,
}


def main() -> None:
    st.set_page_config(
        page_title="AI Math Assistant",
        page_icon="🧮",
    )

    logger.info("Streamlit application started")

    st.title("🧮 AI Math Assistant")

    initialize_chat_memory()

    with st.sidebar:
        st.header("LLM Provider")

        provider_options = list(PROVIDERS.keys())
        default_provider = (
            PROVIDER_NAME if PROVIDER_NAME in PROVIDERS else provider_options[0]
        )

        if default_provider != PROVIDER_NAME:
            logger.warning(
                "Unsupported PROVIDER_NAME=%s. Falling back to %s.",
                PROVIDER_NAME,
                default_provider,
            )

        provider = st.selectbox(
            "Select provider",
            options=provider_options,
            index=provider_options.index(default_provider),
        )

        provider_info = st.empty()

    try:
        llm_service = LLMService(
            provider_name=provider,
        )

        orchestrator = ChatbotOrchestrator(
            llm_service=llm_service,
        )

        logger.info("Orchestrator initialized with provider=%s", provider)

    except RuntimeError:
        logger.exception("Failed to initialize the selected provider.")
        st.error("Não foi possível inicializar o provedor LLM selecionado.")
        st.stop()

    model = PROVIDERS[provider]
    chat_history = get_chat_history()

    if chat_history:
        render_provider_info(
            placeholder=provider_info,
            provider=provider,
            model=model,
            usage=None,
        )
    else:
        provider_info.empty()

    render_history()

    user_input = st.chat_input("Type your mathematical question...")

    if not user_input:
        return

    logger.info("Received user message")

    add_message(
        role="user",
        content=user_input,
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    response = ""
    metadata = {}
    usage = {}

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                result = orchestrator.process_message(
                    user_message=user_input,
                    conversation_history=get_chat_history(),
                )

                response = result.get(
                    "response",
                    "",
                )

                metadata = result.get(
                    "metadata",
                    {},
                )

                usage = result.get(
                    "usage",
                    {},
                )

                logger.info("Message processed successfully.")

            except RuntimeError as exc:
                logger.exception("Runtime error while processing user message.")
                response = str(exc)

            except Exception:
                logger.exception("Unexpected error while processing user message.")
                response = "Ocorreu um erro inesperado ao processar sua solicitação."

        st.markdown(response)

    add_message(
        role="assistant",
        content=response,
        metadata=metadata,
    )

    render_provider_info(
        placeholder=provider_info,
        provider=provider,
        model=model,
        usage=usage,
    )


def render_history() -> None:
    for message in get_chat_history():
        with st.chat_message(
            message["role"],
        ):
            st.markdown(
                message["content"],
            )


def render_provider_info(
    placeholder,
    provider: str,
    model: str,
    usage: dict | None,
) -> None:
    with placeholder.container():
        st.subheader(
            "Current Provider",
        )

        st.write(f"**Provider:** {provider}")
        st.write(f"**Model:** {model}")

        st.divider()

        st.subheader(
            "Generation Parameters",
        )

        st.write(f"**Temperature:** {TEMPERATURE}")
        st.write(f"**Max Tokens:** {MAX_TOKENS}")
        st.write(f"**Top P:** {TOP_P}")

        if provider == "openai":
            st.write(f"**Frequency Penalty:** {FREQUENCY_PENALTY}")
            st.write(f"**Presence Penalty:** {PRESENCE_PENALTY}")

        if not usage:
            return

        st.divider()

        st.subheader(
            "Last Request",
        )

        fields = {
            "Input Tokens": "input_tokens",
            "Output Tokens": "output_tokens",
            "Total Tokens": "total_tokens",
            "Finish Reason": "finish_reason",
            "Eval Duration": "eval_duration",
        }

        for label, key in fields.items():
            value = usage.get(
                key,
            )

            if value is not None:
                st.write(f"**{label}:** {value}")


if __name__ == "__main__":
    main()
