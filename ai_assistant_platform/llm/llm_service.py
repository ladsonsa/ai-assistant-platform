from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.config.settings import (
    PROVIDER_NAME,
)
from ai_assistant_platform.llm.provider_factory import (
    ProviderFactory,
)

logger = get_logger(__name__)


class LLMService:
    """Facade responsible for communication with the configured LLM provider.

    Attributes:
        provider_name (str): The name of the LLM provider being used.
        provider: The underlying provider instance initialized via ProviderFactory.
    """

    def __init__(
        self,
        provider_name: str | None = None,
    ) -> None:
        """Initializes the LLMService with a specific or default LLM provider.

        Args:
            provider_name (str | None): The name of the LLM provider to use. Defaults to None.

        Returns:
            None

        Raises:
            RuntimeError: If the specified provider fails to initialize.
        """
        self.provider_name = provider_name or PROVIDER_NAME

        logger.info(
            "Initializing LLMService with provider=%s",
            self.provider_name,
        )

        try:
            self.provider = ProviderFactory.get_provider(
                self.provider_name,
            )
        except RuntimeError:
            logger.exception(
                "Failed to initialize provider=%s",
                self.provider_name,
            )
            raise

        logger.info(
            "LLMService initialized with provider=%s model=%s",
            self.provider_name,
            self.model_name,
        )

    @property
    def model_name(
        self,
    ) -> str:
        """Return the current model name.

        Args:
            None

        Returns:
            str: The model name of the underlying provider, or 'Unknown' if not found.

        Raises:
            None
        """

        model = getattr(
            self.provider,
            "model_name",
            "Unknown",
        )

        logger.debug(
            "Resolved model name for provider=%s model=%s",
            self.provider_name,
            model,
        )

        return model

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> dict:
        """Generate a response using the configured provider.

        Args:
            messages (list[dict[str, str]]): A list of message dictionaries representing the conversation history.

        Returns:
            dict: A dictionary containing the generated content and usage statistics.
                Format:
                {
                    "content": str,
                    "usage": dict
                }

        Raises:
            RuntimeError: If the provider fails while generating the response.
        """

        logger.info(
            "Generating response with provider=%s messages=%d",
            self.provider_name,
            len(messages),
        )

        try:
            response = self.provider.generate_response(
                messages=messages,
            )
        except RuntimeError:
            logger.exception(
                "Provider failed while generating response provider=%s",
                self.provider_name,
            )
            raise

        result = {
            "content": response.get(
                "content",
                "",
            ),
            "usage": response.get(
                "usage",
                {},
            ),
        }

        logger.info(
            "Response generated successfully provider=%s model=%s",
            self.provider_name,
            self.model_name,
        )

        return result

    def get_provider_info(
        self,
    ) -> dict:
        """Return provider metadata.

        Args:
            None

        Returns:
            dict: A dictionary containing provider metadata such as provider name and model name.

        Raises:
            None
        """

        info = {
            "provider": self.provider_name,
            "model": self.model_name,
        }

        logger.debug(
            "Provider info requested provider=%s model=%s",
            info["provider"],
            info["model"],
        )

        return info
