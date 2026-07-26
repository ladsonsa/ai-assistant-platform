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
    """
    Facade responsible for communication with the configured LLM provider.
    """

    def __init__(
        self,
        provider_name: str | None = None,
    ) -> None:
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
        """
        Return the current model name.
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
        """
        Generate a response using the configured provider.

        Returns:
            {
                "content": str,
                "usage": dict
            }
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
        """
        Return provider metadata.
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
