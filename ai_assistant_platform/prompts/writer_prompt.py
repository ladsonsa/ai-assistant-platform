"""
Prompt builders used by the WriterAgent.

This module centralizes prompt templates responsible for generating
natural language responses from mathematical results, keeping prompt
engineering separated from the application's business logic.
"""


def build_writer_prompt(
    result: str,
    language: str,
) -> str:
    """
    Build the prompt used to generate a natural language response.

    The generated prompt instructs the language model to transform a
    mathematical result into a short, natural, and user-friendly sentence
    using the requested language.

    Args:
        result:
            Formatted mathematical result to be included in the response.

        language:
            ISO 639-1 language code indicating the language in which the
            response should be generated.

    Returns:
        A formatted prompt ready to be sent to the configured language
        model.
    """

    return f"""
You are a concise response generator.

Rules:
- Respond in language: {language}
- Be natural and brief.
- Do NOT just return numbers.
- Always wrap the result in a short sentence.

Examples:

User: 2 + 2
Answer: The result is 4.

User: quanto é 2 + 2
Answer: O resultado é 4.

User: 2 + 2
Answer: 4 é o resultado.

Result:
{result}
"""
