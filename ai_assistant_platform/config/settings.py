from os import getenv

from dotenv import load_dotenv

load_dotenv()

PROVIDER_NAME = getenv("PROVIDER_NAME", "openai")

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
GEMINI_API_KEY = getenv("GEMINI_API_KEY")

OPENAI_MODEL = getenv("OPENAI_MODEL", "gpt-5.4-mini")
GEMINI_MODEL = getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
OLLAMA_MODEL = getenv("OLLAMA_MODEL", "llama3.2")

TEMPERATURE = float(getenv("TEMPERATURE", "0"))
MAX_TOKENS = int(getenv("MAX_TOKENS", "512"))
TOP_P = float(getenv("TOP_P", "1"))
FREQUENCY_PENALTY = float(getenv("FREQUENCY_PENALTY", "0"))
PRESENCE_PENALTY = float(getenv("PRESENCE_PENALTY", "0"))

LOG_LEVEL = getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = getenv("LOG_DIR", "logs")
LOG_FILE_NAME = getenv("LOG_FILE_NAME", "app.log")
LOG_MAX_BYTES = int(getenv("LOG_MAX_BYTES", "5242880"))
LOG_BACKUP_COUNT = int(getenv("LOG_BACKUP_COUNT", "5"))
LOG_TO_CONSOLE = getenv("LOG_TO_CONSOLE", "true").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
LOG_FORMAT = getenv(
    "LOG_FORMAT",
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
