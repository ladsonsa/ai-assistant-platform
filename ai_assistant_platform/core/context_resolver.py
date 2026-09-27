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
    """Resolves mathematical intent and context from natural language input messages.

    Attributes:
        SUPPORTED_LANGUAGES (frozenset[str]): Set of supported ISO 639-1 two-letter
            language codes.
        _llm_service (LLMService): Service instance used for natural language processing
            via an LLM.
    """

    SUPPORTED_LANGUAGES = frozenset(
        {
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
    )

    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:
        """Initializes the ContextResolver with the required LLM service.

        Args:
            llm_service (LLMService): Service handling interaction with language models.
        """
        self._llm_service = llm_service
        logger.info("ContextResolver initialized")

    def resolve(
        self,
        user_message: str,
        last_math_result: float | None,
        last_language: str | None = None,
    ) -> MathContext | None:
        """Resolves user input into a MathContext object using deterministic extraction or LLM analysis.

        Args:
            user_message (str): The raw text message provided by the user.
            last_math_result (float | None): The numerical result of the previous mathematical
                operation, if available.

        Returns:
            MathContext | None: Resolved mathematical context details, or None if the input
                does not contain mathematical intent.
        """
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
                fallback_language=last_language,
            )
            resolved_expression = self._resolve_previous_result(
                expression=expression,
                last_math_result=last_math_result,
            )

            logger.info(
                "Direct mathematical expression detected language=%s expression=%s",
                language,
                resolved_expression,
            )

            return MathContext(
                expression=resolved_expression,
                use_previous_result=False,
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

        resolved_expression = self._resolve_previous_result(
            expression=expression,
            last_math_result=last_math_result,
        )

        language = self._normalize_language(
            data.get("language"),
            fallback_language=last_language,
        )

        logger.info(
            "LLM resolved mathematical context language=%s expression=%s",
            language,
            resolved_expression,
        )

        return MathContext(
            expression=resolved_expression,
            use_previous_result=False,
            previous_result=last_math_result,
            language=language,
        )

    def _resolve_previous_result(
        self,
        expression: str,
        last_math_result: float | None,
    ) -> str:
        """Replaces the '$result' placeholder in an expression with the actual previous result value.

        Args:
            expression (str): The mathematical expression string containing potential placeholders.
            last_math_result (float | None): The previous evaluation result value to inject.

        Returns:
            str: Expression string with '$result' replaced by the numerical value if available.
        """
        if "$result" not in expression:
            return expression

        if last_math_result is None:
            logger.warning(
                "Expression references previous result but no previous result exists",
            )
            return expression

        return expression.replace(
            "$result",
            str(last_math_result),
        )

    def _extract_expression(
        self,
        text: str,
    ) -> str | None:
        """Attempts direct extraction of a mathematical expression from plain text.

        Args:
            text (str): The input text to analyze.

        Returns:
            str | None: The extracted math expression string, or None if extraction failed.
        """
        cleaned = text.lower()

        for prefix in (
            "quanto é",
            "calcule",
            "calcule:",
            "resolve",
            "resolva",
            "now",
            "agora",
        ):
            cleaned = cleaned.replace(prefix, "")

        if "$result" in cleaned:
            cleaned = cleaned.replace(
                "resultado anterior",
                "$result",
            ).replace(
                "resultado",
                "$result",
            )

        if cleaned.startswith(
            (
                "subtract",
                "subtraia",
                "menos",
                "-",
            )
        ):
            match = re.search(
                r"\d+(?:\.\d+)?",
                cleaned,
            )
            if match:
                return f"$result - {match.group()}"

        if cleaned.startswith(
            (
                "add",
                "plus",
                "somar",
                "adicionar",
                "mais",
                "+",
            )
        ):
            match = re.search(
                r"\d+(?:\.\d+)?",
                cleaned,
            )
            if match:
                return f"$result + {match.group()}"

        text_without_result = cleaned.replace(
            "$result",
            "",
        )

        if re.search(
            r"[a-z]",
            text_without_result,
        ):
            logger.debug(
                "Direct extraction rejected because of alphabetic text",
            )
            return None

        match = re.search(
            r"(?:\$result|[\d\.\+\-\*\/\(\)\s])+",
            cleaned,
        )

        if not match:
            logger.debug(
                "Direct extraction found no mathematical pattern",
            )
            return None

        expression = match.group().strip()
        expression = expression.replace("\n", "").replace("\r", "").replace(" ", "")

        if (
            not re.search(
                r"\d",
                expression,
            )
            and "$result" not in expression
        ):
            logger.debug(
                "Direct extraction rejected because no numeric content was found",
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
        """Involves the LLM service to analyze ambiguous mathematical input and retrieve JSON results.

        Args:
            user_message (str): The raw text message provided by the user.
            last_math_result (float | None): Previous calculation result context.

        Returns:
            dict | None: Parsed JSON response dictionary from the LLM, or None if parsing failed.
        """
        logger.debug(
            "Calling LLM for math interpretation has_previous_result=%s",
            last_math_result is not None,
        )

        response = self._llm_service.generate_response(
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
        """Determines if a text string is a potential candidate for mathematical processing.

        Args:
            text (str): The raw text string to evaluate.

        Returns:
            bool: True if mathematical operators or keywords are detected, False otherwise.
        """
        lowered = text.lower()

        if re.search(
            r"\d",
            lowered,
        ):
            logger.debug("Math candidate detected by numeric content")
            return True

        math_words = (
            "quanto",
            "calcule",
            "calcular",
            "soma",
            "calculate",
            "sum",
            "add",
            "subtract",
            "multiply",
            "divide",
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
            "plus",
            "minus",
            "times",
            "multiply",
            "resultado",
            "anterior",
            "caixas",
            "itens",
            "perdi",
            "double",
            "twice",
            "half",
            "dobrar",
            "dobre",
            "metade",
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
        fallback_language: str | None = None,
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

        normalized_fallback = self._normalize_language(
            fallback_language,
        )

        return normalized_fallback

    def _normalize_language(
        self,
        language: str | None,
        fallback_language: str | None = None,
    ) -> str:
        if language:
            normalized = language.lower().split("-")[0]

            if normalized in self.SUPPORTED_LANGUAGES:
                return normalized

            logger.warning(
                "Unsupported language received language=%s",
                language,
            )

        if fallback_language:
            fallback = fallback_language.lower().split("-")[0]

            if fallback in self.SUPPORTED_LANGUAGES:
                return fallback

        return "en"
