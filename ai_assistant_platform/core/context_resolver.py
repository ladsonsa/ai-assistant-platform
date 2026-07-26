import json
import re

from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.core.math_context import (
    MathContext,
)
from ai_assistant_platform.llm.llm_service import (
    LLMService,
)
from ai_assistant_platform.prompts.context_prompt import (
    build_context_prompt,
)

logger = get_logger(__name__)


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
        logger.info("ContextResolver initialized")

    def resolve(
        self,
        user_message: str,
        last_math_result: float | None,
    ) -> MathContext | None:
        logger.debug(
            "Resolving math context message_length=%d has_previous_result=%s",
            len(user_message),
            last_math_result is not None,
        )

        expression = self._extract_expression(
            user_message,
        )

        if expression is not None:
            language = self._detect_language(
                user_message,
            )
            logger.info(
                "Direct mathematical expression detected language=%s expression=%s",
                language,
                expression,
            )
            return MathContext(
                expression=expression,
                use_previous_result="$result" in expression,
                previous_result=last_math_result,
                language=language,
            )

        if not self._is_math_candidate(
            user_message,
        ):
            logger.debug("Message rejected as non-math candidate")
            return None

        data = self._call_llm(
            user_message=user_message,
            last_math_result=last_math_result,
        )

        if not data:
            logger.warning("LLM returned empty or invalid payload")
            return None

        if not data.get(
            "is_math",
            False,
        ):
            logger.info("LLM classified message as non-math")
            return None

        expression = data.get(
            "expression",
        )

        if not expression:
            logger.warning("LLM response missing expression")
            return None

        expression = expression.strip()

        if not expression:
            logger.warning("LLM response returned blank expression")
            return None

        language = self._normalize_language(
            data.get(
                "language",
            )
        )

        use_previous_result = bool(
            data.get(
                "use_previous_result",
                False,
            )
        )

        logger.info(
            "LLM resolved mathematical context language=%s use_previous_result=%s",
            language,
            use_previous_result,
        )

        return MathContext(
            expression=expression,
            use_previous_result=use_previous_result,
            previous_result=last_math_result,
            language=language,
        )

    def _extract_expression(
        self,
        text: str,
    ) -> str | None:
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
                "resultado",
                "$result",
            )

        text_without_result = cleaned.replace("$result", "")
        if re.search(r"[a-z]", text_without_result):
            logger.debug("Direct extraction rejected because of alphabetic text")
            return None

        match = re.search(
            r"[\d\.\+\-\*\/\(\)\s\$]+",
            cleaned,
        )

        if not match:
            logger.debug("Direct extraction found no mathematical pattern")
            return None

        expression = match.group().strip()
        expression = expression.replace("\n", "").replace("\r", "").replace(" ", "")

        if not re.search(r"\d", expression) and "$result" not in expression:
            logger.debug(
                "Direct extraction rejected because no numeric content was found"
            )
            return None

        logger.debug(
            "Direct expression extracted expression=%s",
            expression,
        )

        return expression

    def _call_llm(
        self,
        user_message: str,
        last_math_result: float | None,
    ) -> dict | None:
        logger.debug(
            "Calling LLM for math interpretation has_previous_result=%s",
            last_math_result is not None,
        )

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
            parsed = json.loads(
                response["content"],
            )
            logger.debug("LLM payload parsed successfully")
            return parsed
        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
        ):
            logger.warning("LLM payload could not be parsed as JSON")
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
            logger.debug("Math candidate detected by operator presence")
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

        is_candidate = any(word in lowered for word in math_words)

        logger.debug(
            "Math candidate evaluated result=%s",
            is_candidate,
        )

        return is_candidate

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
            logger.debug("Language not provided. Falling back to en")
            return "en"

        language = language.lower()

        if language in self.SUPPORTED_LANGUAGES:
            return language

        normalized = language[:2]
        logger.debug(
            "Language normalized language=%s normalized=%s",
            language,
            normalized,
        )
        return normalized
