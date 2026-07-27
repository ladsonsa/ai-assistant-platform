from dataclasses import dataclass


@dataclass(slots=True)
class MathContext:
    """
    Stores the structured mathematical information extracted from a user
    request.

    This object is produced by the ContextResolver and consumed by the
    ChatbotOrchestrator to execute mathematical operations.
    """

    expression: str

    use_previous_result: bool = False

    previous_result: float | None = None

    language: str = "en"
