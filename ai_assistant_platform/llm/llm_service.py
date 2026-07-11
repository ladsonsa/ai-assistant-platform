import os
from chatbot.provider_factory import ProviderFactory


class LLMService:
    def __init__(self, provider_name: str = None):
        # Utiliza o Gemini como padrão se não for especificado ou configurado via .env
        self.provider_name = provider_name or os.getenv("LLM_PROVIDER", "gemini")
        self.provider = ProviderFactory.get_provider(self.provider_name)

    def generate_response(self, prompt: str, **kwargs) -> str:
        return self.provider.generate(prompt, **kwargs)
