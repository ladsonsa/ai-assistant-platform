from openai import OpenAI

from chatbot_ai.config.settings import OPENAI_API_KEY, MODEL_NAME

class LLMService:

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_response(self, messages: list[dict]) -> str:

        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME, 
                messages=messages)
            return response.choices[0].message.content

        except Exception as error:
            
            return f"An error occurred while generating the response: {error}"
