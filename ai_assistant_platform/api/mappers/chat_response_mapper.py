from ai_assistant_platform.api.schemas import (
    ChatResponseSchema,
)


class ChatResponseMapper:
    """Provides mapping utilities to transform internal orchestrator responses into API response schemas."""

    @staticmethod
    def to_schema(
        response: dict,
    ) -> ChatResponseSchema:
        """Converts an orchestrator response dictionary into a ChatResponseSchema schema object.

        Args:
            response (dict): A dictionary containing orchestrator outputs, expected to include
                'response' and 'metadata' keys.

        Returns:
            ChatResponseSchema: The constructed response schema containing message content and metadata.

        Raises:
            KeyError: If 'response' or 'metadata' keys are missing from the input dictionary.
        """
        return ChatResponseSchema(
            content=response["response"],
            metadata=response["metadata"],
        )
