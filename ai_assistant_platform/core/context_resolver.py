import json
import re

from ai_assistant_platform.core.math_context import (
    MathContext,
)
from ai_assistant_platform.llm.llm_service import (
    LLMService,
)

from ai_assistant_platform.prompts.context_prompt import (
    build_context_prompt,
)


class ContextResolver:
    """
    Resolve mathematical intent from user messages.

    This class is responsible for determining whether a user message
    represents a supported mathematical request and converting it into
    a structured ``MathContext``.

    Resolution follows a three-step strategy:

    1. Parse simple mathematical expressions using regular expressions.
    2. Reject obviously invalid inputs before invoking an LLM.
    3. Delegate complex intent parsing to the configured language model.

    The returned ``MathContext`` is consumed by the orchestrator to
    execute the requested mathematical operation.
    """

    SUPPORTED_LANGUAGES = {
        "pt",
        "en",
        "es",
        "fr",
        "de",
        "ja",
        "it",
        "ru",
        "zh",
        "ko",
        "ar",
    }

    def __init__(
        self,
        llm_service: LLMService,
    ):
        """
        Initialize the context resolver.

        Args:
            llm_service:
                Service responsible for communicating with the configured
                language model provider.
        """
        self.llm_service = llm_service

    def resolve(
        self,
        user_message: str,
        last_math_result: float | None,
    ) -> MathContext | None:
        """
        Resolve a user message into a mathematical context.

        The resolver first attempts to parse simple expressions locally
        using regular expressions. If this fails, it validates whether
        the message is a reasonable candidate for mathematical processing
        before delegating intent extraction to the LLM.

        Args:
            user_message:
                Raw message provided by the user.

            last_math_result:
                Previous mathematical result available in the conversation,
                if any.

        Returns:
            A populated ``MathContext`` when the message represents a valid
            mathematical request, otherwise ``None``.
        """

        regex_result = self._try_regex(
            user_message=user_message,
        )

        if regex_result:
            return regex_result

        if not self._is_valid_candidate(
            user_message,
        ):
            return None

        data = self._call_llm(
            user_message=user_message,
            last_math_result=last_math_result,
        )

        if not data:
            return None

        if not data.get("is_math"):
            return None

        operation = self._normalize_operation(data.get("operation"))

        if operation is None:
            return None

        try:
            return MathContext(
                operation=operation,
                left_operand=float(data["left_operand"]),
                right_operand=float(data["right_operand"]),
                use_previous_result=bool(
                    data.get(
                        "use_previous_result",
                        False,
                    )
                ),
                previous_result=last_math_result,
                language=self._normalize_language(data.get("language")),
            )

        except (
            KeyError,
            ValueError,
            TypeError,
        ):
            return None

    def _try_regex(
        self,
        user_message: str,
    ) -> MathContext | None:
        """
        Parse simple mathematical expressions using regular expressions.

        Supported expressions include direct operations such as:

        - 2 + 2
        - 10 / 5
        - 8 * 7

        Args:
            user_message:
                User input to analyze.

        Returns:
            A ``MathContext`` if a supported expression is found.
            Otherwise, returns ``None``.
        """

        pattern = r"(-?\d+(?:\.\d+)?)" r"\s*([\+\-\*/])\s*" r"(-?\d+(?:\.\d+)?)"

        match = re.search(
            pattern,
            user_message,
        )

        if not match:
            return None

        left, operator, right = match.groups()

        operation_map = {
            "+": "addition",
            "-": "subtraction",
            "*": "multiplication",
            "/": "division",
        }

        return MathContext(
            operation=operation_map[operator],
            left_operand=float(left),
            right_operand=float(right),
            use_previous_result=False,
            previous_result=None,
            language="auto",
        )

    def _call_llm(
        self,
        user_message: str,
        last_math_result: float | None,
    ) -> dict | None:
        """
        Request mathematical intent parsing from the language model.

        Args:
            user_message:
                Raw user message.

            last_math_result:
                Previous mathematical result available in the conversation.

        Returns:
            Parsed JSON response as a dictionary when successful.
            Returns ``None`` if the response cannot be parsed.
        """

        prompt = prompt = build_context_prompt(
            user_message=user_message,
            last_math_result=last_math_result,
        )

        response = self.llm_service.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": ("Return only valid JSON."),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        )

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return None

    def _normalize_operation(
        self,
        operation: str | None,
    ) -> str | None:
        """
        Normalize operation aliases into canonical operation names.

        Examples:
            add -> addition
            plus -> addition
            multiply -> multiplication

        Args:
            operation:
                Operation returned by the parser.

        Returns:
            Canonical operation name or ``None`` if unsupported.
        """

        if not operation:
            return None

        mapping = {
            "addition": "addition",
            "add": "addition",
            "sum": "addition",
            "subtraction": "subtraction",
            "subtract": "subtraction",
            "minus": "subtraction",
            "multiplication": "multiplication",
            "multiply": "multiplication",
            "times": "multiplication",
            "division": "division",
            "divide": "division",
        }

        return mapping.get(
            operation.lower(),
        )

    def _normalize_language(
        self,
        language: str | None,
    ) -> str:
        """
        Normalize language codes returned by the language model.

        Supported ISO 639-1 language codes are preserved. Unknown codes
        are truncated to their first two characters when possible.

        Args:
            language:
                Language code returned by the parser.

        Returns:
            A normalized ISO 639-1 language code.
        """

        if not language:
            return "en"

        language = language.lower()

        if language in self.SUPPORTED_LANGUAGES:
            return language

        if len(language) >= 2:
            return language[:2]

        return "en"

    def _is_valid_candidate(
        self,
        text: str,
    ) -> bool:
        """
        Determine whether a message is a reasonable mathematical candidate.

        This lightweight validation prevents obviously invalid inputs
        (random symbols, noise, etc.) from reaching the language model,
        reducing latency and API costs.

        Args:
            text:
                User input.

        Returns:
            ``True`` if the message is likely to represent a mathematical
            request, otherwise ``False``.
        """

        text = text.strip().lower()

        has_number = bool(re.search(r"\d", text))

        math_words = [
            "mais",
            "menos",
            "vezes",
            "dividido",
            "somar",
            "subtrair",
            "multiplicar",
            "plus",
            "minus",
            "times",
            "divide",
            "add",
            "multiply",
            "+",
            "-",
            "*",
            "/",
        ]

        has_math_word = any(word in text for word in math_words)

        is_noise = bool(
            re.fullmatch(
                r"[^a-zA-Z0-9\s\+\-\*/.,]+",
                text,
            )
        )

        return (has_number or has_math_word) and not is_noise
