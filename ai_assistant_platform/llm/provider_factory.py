from importlib import import_module

from ai_assistant_platform.config.logging_config import (
    get_logger,
)

logger = get_logger(__name__)


class ProviderFactory:
    """
    Factory responsible for creating language model providers.
    """

    _PROVIDERS = {
        "openai": (
            "ai_assistant_platform.llm.providers.openai_provider",
            "OpenAIProvider",
        ),
        "gemini": (
            "ai_assistant_platform.llm.providers.gemini_provider",
            "GeminiProvider",
        ),
        "ollama": (
            "ai_assistant_platform.llm.providers.ollama_provider",
            "OllamaProvider",
        ),
    }

    @classmethod
    def get_provider(
        cls,
        provider_name: str,
    ):
        """
        Create and return a provider instance.
        """

        provider_name = provider_name.lower()

        logger.info(
            "Resolving provider=%s",
            provider_name,
        )

        provider_info = cls._PROVIDERS.get(
            provider_name,
        )

        if provider_info is None:
            logger.error(
                "Unsupported provider requested provider=%s",
                provider_name,
            )
            raise ValueError(f"Unsupported provider: {provider_name}")

        module_name, class_name = provider_info

        try:
            logger.debug(
                "Importing provider module=%s class=%s",
                module_name,
                class_name,
            )

            module = import_module(
                module_name,
            )

            provider_class = getattr(
                module,
                class_name,
            )

            provider = provider_class()

            logger.info(
                "Provider instantiated provider=%s class=%s",
                provider_name,
                class_name,
            )

            return provider

        except ModuleNotFoundError as exc:
            logger.exception(
                "Provider unavailable provider=%s missing_package=%s",
                provider_name,
                exc.name,
            )
            raise RuntimeError(
                f"The '{provider_name}' provider is unavailable because "
                f"the required package '{exc.name}' is not installed."
            ) from exc

        except AttributeError as exc:
            logger.exception(
                "Provider class not found provider=%s module=%s class=%s",
                provider_name,
                module_name,
                class_name,
            )
            raise RuntimeError(
                f"The provider class '{class_name}' was not found in "
                f"module '{module_name}'."
            ) from exc

        except Exception as exc:
            logger.exception(
                "Failed to initialize provider provider=%s",
                provider_name,
            )
            raise RuntimeError(
                f"Failed to initialize provider '{provider_name}': {exc}"
            ) from exc
