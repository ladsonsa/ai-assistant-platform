from ai_assistant_platform.config.settings import (
    PROVIDER_NAME,
)
from ai_assistant_platform.llm.provider_factory import (
    ProviderFactory,
)


class LLMService:
    """
    Facade responsible for communication with the configured LLM provider.
    """

    def __init__(
        self,
        provider_name: str | None = None,
    ) -> None:

        self.provider_name = provider_name or PROVIDER_NAME

        self.provider = ProviderFactory.get_provider(
            self.provider_name,
        )

    @property
    def model_name(
        self,
    ) -> str:
        """
        Return the current model name.
        """

        return getattr(
            self.provider,
            "model_name",
            "Unknown",
        )

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

        response = self.provider.generate_response(
            messages=messages,
        )

        return {
            "content": response.get(
                "content",
                "",
            ),
            "usage": response.get(
                "usage",
                {},
            ),
        }

    def get_provider_info(
        self,
    ) -> dict:
        """
        Return provider metadata.
        """

        return {
            "provider": self.provider_name,
            "model": self.model_name,
        }
