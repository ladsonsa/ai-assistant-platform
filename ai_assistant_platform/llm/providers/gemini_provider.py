import google.generativeai as genai
from chatbot.providers.base_provider import BaseProvider
from chatbot.settings import GEMINI_API_KEY, GEMINI_MODEL


class GeminiProvider(BaseProvider):
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.model.generate_content(prompt)
        return response.text
