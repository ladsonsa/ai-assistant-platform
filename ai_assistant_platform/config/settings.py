from dotenv import load_dotenv

import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "openai",
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gpt-5.4-mini",
)
