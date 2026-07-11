import unittest
from chatbot.provider_factory import ProviderFactory
from chatbot.providers.gemini_provider import GeminiProvider
from chatbot.llm_service import LLMService


class TestLLM(unittest.TestCase):
    # ... testes existentes ...

    def test_gemini_provider_factory(self):
        provider = ProviderFactory.get_provider("gemini")
        self.assertIsInstance(provider, GeminiProvider)

    def test_llm_service_gemini_initialization(self):
        service = LLMService(provider_name="gemini")
        self.assertEqual(service.provider_name, "gemini")
        self.assertIsInstance(service.provider, GeminiProvider)
