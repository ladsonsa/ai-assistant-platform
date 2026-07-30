from ai_assistant_platform.api.schemas import ChatResponse


class ChatResponseMapper:
    """Provides mapping utilities to transform orchestrator responses into API response schemas."""

    @staticmethod
    def to_schema(
        response: dict,
    ) -> ChatResponse:
        """Converts an orchestrator response dictionary into a ChatResponse schema object.

        Args:
            response (dict): A dictionary containing the orchestrator output, expected to
                include 'response' and 'metadata' keys.

        Returns:
            ChatResponse: The constructed response schema containing message content and metadata.

        Raises:
            KeyError: If 'response' or 'metadata' keys are missing from the input dictionary.
        """
        return ChatResponse(
            content=response["response"],
            metadata=response["metadata"],
        )
