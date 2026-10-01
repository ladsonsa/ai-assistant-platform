"""Deterministic mock LLM service module for testing pipelines."""

from typing import Any


class DeterministicLLMService:
    """Fake LLM service returning predictable outputs for testing purposes."""

    provider_name: str = "e2e"
    model_name: str = "deterministic"

    def generate_response(
        self,
        messages: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Generates a deterministic response dictionary based on input message content.

        Args:
            messages: List of message dictionaries containing chat context.

        Returns:
            dict[str, Any]: Dictionary with generated text content and token usage.
        """
        if (
            messages
            and messages[0].get("content") == "Return only valid JSON."
        ):
            return {
                "content": (
                    '{"is_math": true, "expression": "2 + 2", "language": "pt"}'
                ),
                "usage": {},
            }

        return {
            "content": "O resultado é 4.",
            "usage": {},
        }