from importlib import import_module


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

        provider_info = cls._PROVIDERS.get(
            provider_name,
        )

        if provider_info is None:
            raise ValueError(
                f"Unsupported provider: {provider_name}"
            )

        module_name, class_name = provider_info

        try:

            module = import_module(
                module_name,
            )

            provider_class = getattr(
                module,
                class_name,
            )

            return provider_class()

        except ModuleNotFoundError as exc:

            raise RuntimeError(
                f"The '{provider_name}' provider is unavailable because "
                f"the required package '{exc.name}' is not installed."
            ) from exc

        except AttributeError as exc:

            raise RuntimeError(
                f"The provider class '{class_name}' was not found in "
                f"module '{module_name}'."
            ) from exc

        except Exception as exc:

            raise RuntimeError(
                f"Failed to initialize provider "
                f"'{provider_name}': {exc}"
            ) from exc