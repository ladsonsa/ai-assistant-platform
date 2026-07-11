# ai_assistant_platform/core/math_context.py

from dataclasses import dataclass


@dataclass(slots=True)
class MathContext:
    """
    Represents a validated mathematical request extracted from the user's
    message.

    Attributes:
        expression:
            Canonical mathematical expression to be evaluated.

        use_previous_result:
            Indicates whether the previous conversation result should be used
            when evaluating the expression.

        previous_result:
            Previous mathematical result stored in the conversation.

        language:
            ISO 639-1 language code detected from the current user message.
    """

    expression: str
    use_previous_result: bool
    previous_result: float | None
    language: str
