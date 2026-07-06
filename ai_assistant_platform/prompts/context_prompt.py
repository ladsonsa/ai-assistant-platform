"""
Prompt builders used by the ContextResolver.

This module centralizes prompt templates responsible for extracting
structured mathematical intent from user messages, keeping prompt
engineering separated from application logic.
"""


def build_context_prompt(
    user_message: str,
    last_math_result: float | None,
) -> str:
    """
    Build the prompt used to extract mathematical intent from a user message.

    The generated prompt instructs the language model to determine whether
    the input represents a supported mathematical request and, when
    applicable, return a structured JSON object describing the operation,
    operands, conversation context usage, and detected language.

    Args:
        user_message:
            Raw message submitted by the user.

        last_math_result:
            Most recent mathematical result available in the conversation.
            Used when the user refers to a previous calculation.

    Returns:
        A formatted prompt ready to be sent to the configured language
        model.
    """

    return f"""
You are a mathematical intent parser.

Return ONLY valid JSON.

Rules:
- Detect if the message is mathematical.
- Detect the language of the CURRENT user message.
- Support any language.
- Use ISO 639-1 language codes.
- Ignore previous conversation language.
- If language detection fails use "en".

Allowed operations:
- addition
- subtraction
- multiplication
- division

User message:
{user_message}

Previous mathematical result:
{last_math_result}

If mathematical:

{{
    "is_math": true,
    "operation": "addition",
    "left_operand": 5,
    "right_operand": 4,
    "use_previous_result": false,
    "language": "pt"
}}

If not mathematical:

{{
    "is_math": false,
    "language": "pt"
}}
"""
