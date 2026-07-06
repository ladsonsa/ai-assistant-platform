from dataclasses import dataclass


@dataclass
class MathContext:
    """
    Represents a parsed mathematical request extracted from a user message.

    This data structure encapsulates all information required by the
    orchestrator and mathematical agent to execute a supported operation.

    Attributes:
        operation:
            Canonical mathematical operation to execute
            (e.g. ``addition``, ``subtraction``, ``multiplication``,
            ``division``).

        left_operand:
            Left operand of the mathematical operation.

        right_operand:
            Right operand of the mathematical operation.

        use_previous_result:
            Indicates whether the previous mathematical result should be
            used as the left operand instead of ``left_operand``.

        previous_result:
            Last mathematical result available in the conversation.
            ``None`` when no previous result exists.

        language:
            ISO 639-1 language code detected from the current user
            message (e.g. ``pt``, ``en``, ``es``).
    """

    operation: str
    left_operand: float
    right_operand: float
    use_previous_result: bool
    previous_result: float | None
    language: str
