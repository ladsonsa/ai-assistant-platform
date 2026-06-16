from openai import OpenAI

from chatbot_ai.config.settings import OPENAI_API_KEY

client = OpenAI(
    api_key= OPENAI_API_KEY
)

def generate_response(message: list[dict]) -> str:

    try:
        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=message
        )
        return response.choices[0].message.content
    
    except Exceptionas as error:
        return f"An error ocorrend while generating the response: {error}"
