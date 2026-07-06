from ai_assistant_platform.llm.llm_service import LLMService

from ai_assistant_platform.prompts.writer_prompt import (
    build_writer_prompt,
)


class WriterAgent:
    """
    Agent responsible for generating natural language responses.

    This agent formats mathematical results into concise, human-readable
    sentences by delegating text generation to the configured language
    model service.
    """

    def __init__(
        self,
        llm_service: LLMService,
    ):
        self.llm_service = llm_service

    def generate_response(
        self,
        result: float,
        language: str,
    ) -> str:
        """
        Generate a natural language response for a mathematical result.

        The response is produced in the requested language using the
        configured language model.

        Args:
            result:
                Mathematical result to be presented.
            language:
                ISO 639-1 language code indicating the language of the
                response (for example: "pt", "en", "es").

        Returns:
            A concise natural language sentence containing the formatted
            mathematical result.
        """

        formatted_result = self._format(result)

        prompt = build_writer_prompt(
            result=formatted_result,
            language=language,
        )

        return self.llm_service.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate short mathematical answers "
                        "in the requested language."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        )

    def _format(
        self,
        value: float | int,
    ) -> str:
        """
        Format a numeric value for presentation.

        Integer-valued floats are converted to integers to avoid
        unnecessary decimal places (for example, ``5.0`` becomes ``5``).

        Args:
            value:
                Numeric value to format.

        Returns:
            String representation of the formatted value.
        """

        if isinstance(value, float) and value.is_integer():
            return str(int(value))

        return str(value)
