"""Application settings and environment configuration module.

Loads environment variables, defines runtime default parameters for LLM providers
and logging systems, and enforces validation rules during initialization.
"""

from os import getenv

from dotenv import load_dotenv

load_dotenv()

PROVIDER_NAME: str = getenv("PROVIDER_NAME", "openai")

OPENAI_API_KEY: str | None = getenv("OPENAI_API_KEY")
GEMINI_API_KEY: str | None = getenv("GEMINI_API_KEY")

OPENAI_MODEL: str = getenv("OPENAI_MODEL", "gpt-5.4-mini")
GEMINI_MODEL: str = getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
OLLAMA_MODEL: str = getenv("OLLAMA_MODEL", "llama3.2")

TEMPERATURE: float = float(getenv("TEMPERATURE", "0"))
MAX_TOKENS: int = int(getenv("MAX_TOKENS", "512"))
TOP_P: float = float(getenv("TOP_P", "1"))
FREQUENCY_PENALTY: float = float(getenv("FREQUENCY_PENALTY", "0"))
PRESENCE_PENALTY: float = float(getenv("PRESENCE_PENALTY", "0"))

LOG_LEVEL: str = getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR: str = getenv("LOG_DIR", "logs")
LOG_FILE_NAME: str = getenv("LOG_FILE_NAME", "app.log")
LOG_MAX_BYTES: int = int(getenv("LOG_MAX_BYTES", "5242880"))
LOG_BACKUP_COUNT: int = int(getenv("LOG_BACKUP_COUNT", "5"))
LOG_TO_CONSOLE: bool = getenv("LOG_TO_CONSOLE", "true").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
LOG_FORMAT: str = getenv(
    "LOG_FORMAT",
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def _validate_settings() -> None:
    """Validates runtime settings against operational boundaries and constraints.

    Raises:
        ValueError: If provider names, models, or numerical parameters fall outside
            their acceptable domains.
    """
    if not PROVIDER_NAME.strip():
        raise ValueError("PROVIDER_NAME must not be empty.")

    if PROVIDER_NAME.lower() not in {"openai", "gemini", "ollama"}:
        raise ValueError(f"Unsupported provider: {PROVIDER_NAME}")

    for name, model in {
        "OPENAI_MODEL": OPENAI_MODEL,
        "GEMINI_MODEL": GEMINI_MODEL,
        "OLLAMA_MODEL": OLLAMA_MODEL,
    }.items():
        if not model or not model.strip():
            raise ValueError(f"{name} must not be empty.")

    if not 0 <= TEMPERATURE <= 2:
        raise ValueError("TEMPERATURE must be between 0 and 2.")

    if MAX_TOKENS < 1:
        raise ValueError("MAX_TOKENS must be greater than or equal to 1.")

    if not 0 <= TOP_P <= 1:
        raise ValueError("TOP_P must be between 0 and 1.")

    if not -2 <= FREQUENCY_PENALTY <= 2:
        raise ValueError("FREQUENCY_PENALTY must be between -2 and 2.")

    if not -2 <= PRESENCE_PENALTY <= 2:
        raise ValueError("PRESENCE_PENALTY must be between -2 and 2.")


_validate_settings()
