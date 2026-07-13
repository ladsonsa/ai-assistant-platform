import unittest
from ai_assistant_platform.llm.provider_factory import ProviderFactory
from ai_assistant_platform.llm.providers.providers.gemini_provider import GeminiProvider
from ai_assistant_platform.llm.llm_service import LLMService


class TestLLM(unittest.TestCase):
    # ... testes existentes ...

    def test_gemini_provider_factory(self):
        provider = ProviderFactory.get_provider("gemini")
        self.assertIsInstance(provider, GeminiProvider)

    def test_llm_service_gemini_initialization(self):
        service = LLMService(provider_name="gemini")
        self.assertEqual(service.provider_name, "gemini")
        self.assertIsInstance(service.provider, GeminiProvider)
