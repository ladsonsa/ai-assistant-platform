from chatbot.providers.openai_provider import OpenAIProvider
from chatbot.providers.ollama_provider import OllamaProvider
from chatbot.providers.gemini_provider import GeminiProvider


class ProviderFactory:
    @staticmethod
    def get_provider(provider_name: str):
        provider_name = provider_name.lower()
        if provider_name == "openai":
            return OpenAIProvider()
        elif provider_name == "ollama":
            return OllamaProvider()
        elif provider_name == "gemini":
            return GeminiProvider()
        else:
            raise ValueError(f"Provider '{provider_name}' não suportado.")
