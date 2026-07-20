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

from ai_assistant_platform.core.expression_extractor import (
    ExpressionExtractor,
)


class ContextResolver:
    """
    Resolves user messages into structured mathematical context.
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
    ) -> None:
        self.llm_service = llm_service
        self._expression_extractor = ExpressionExtractor()

    def resolve(
        self,
        user_message: str,
        last_math_result: float | None,
    ) -> MathContext | None:

        expression = self._expression_extractor.extract(
            user_message,
        )

        if expression is not None:
            return MathContext(
                expression=expression,
                use_previous_result="$result" in expression,
                previous_result=last_math_result,
                language=self._detect_language(
                    user_message,
                ),
            )

        if not self._is_math_candidate(
            user_message,
        ):
            return None

        data = self._call_llm(
            user_message=user_message,
            last_math_result=last_math_result,
        )

        if not data:
            return None

        if not data.get(
            "is_math",
            False,
        ):
            return None

        expression = data.get(
            "expression",
        )

        if not expression:
            return None

        expression = expression.strip()

        if not expression:
            return None

        return MathContext(
            expression=expression,
            use_previous_result=bool(
                data.get(
                    "use_previous_result",
                    False,
                )
            ),
            previous_result=last_math_result,
            language=self._normalize_language(
                data.get(
                    "language",
                )
            ),
        )

    def _extract_expression(
        self,
        text: str,
    ) -> str | None:
        """
        Extract mathematical expressions directly from the message.
        """
        cleaned = text.lower()

        for prefix in (
            "quanto é",
            "calcule",
            "calcule:",
            "resolve",
            "resolva",
        ):
            cleaned = cleaned.replace(prefix, "")

        if "$result" in cleaned:
            cleaned = cleaned.replace("resultado anterior", "$result").replace(
                "resultado", "$result"
            )

        text_without_result = cleaned.replace("$result", "")
        if re.search(r"[a-z]", text_without_result):
            return None

        match = re.search(
            r"[\d\.\+\-\*\/\(\)\s\$]+",
            cleaned,
        )

        if not match:
            return None

        expression = match.group().strip()
        expression = expression.replace("\n", "").replace("\r", "").replace(" ", "")

        if not re.search(r"\d", expression) and "$result" not in expression:
            return None

        return expression

    def _call_llm(
        self,
        user_message: str,
        last_math_result: float | None,
    ) -> dict | None:

        response = self.llm_service.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": "Return only valid JSON.",
                },
                {
                    "role": "user",
                    "content": build_context_prompt(
                        user_message=user_message,
                        last_math_result=last_math_result,
                    ),
                },
            ]
        )

        try:
            return json.loads(
                response["content"],
            )

        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
        ):
            return None

    def _is_math_candidate(
        self,
        text: str,
    ) -> bool:

        lowered = text.lower()

        if re.search(
            r"[\+\-\*/()]",
            lowered,
        ):
            return True

        math_words = (
            "quanto",
            "calcule",
            "calcular",
            "soma",
            "somar",
            "subtraia",
            "subitrair",
            "mais",
            "menos",
            "vezes",
            "multiplicar",
            "multiplique",
            "dividir",
            "divida",
            "divide",
            "plus",
            "minus",
            "times",
            "multiply",
            "divide",
            "resultado",
            "anterior",
            "caixas",
            "itens",
            "perdi",
        )

        return any(word in lowered for word in math_words)

    def _detect_language(
        self,
        text: str,
    ) -> str:

        lowered = text.lower()

        if any(
            word in lowered
            for word in (
                "quanto",
                "calcule",
                "resultado",
                "mais",
                "menos",
                "vezes",
            )
        ):
            return "pt"

        if any(
            word in lowered
            for word in (
                "what",
                "calculate",
                "plus",
                "minus",
                "times",
            )
        ):
            return "en"

        if any(
            word in lowered
            for word in (
                "cuanto",
                "ahora",
                "resultado",
                "más",
                "menos",
            )
        ):
            return "es"

        return "en"

    def _normalize_language(
        self,
        language: str | None,
    ) -> str:

        if not language:
            return "en"

        language = language.lower()

        if language in self.SUPPORTED_LANGUAGES:
            return language

        return language[:2]
