# ai_assistant_platform/core/context_resolver.py

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
    Resolves the user's message into a MathContext.
    """

    def __init__(
        self,
        llm_service: LLMService,
    ):
        self.llm_service = llm_service

    def resolve(
        self,
        user_message: str,
        last_math_result: float | None,
    ) -> MathContext | None:

        if not self._is_valid_candidate(user_message):
            return None

        data = self._call_llm(
            user_message=user_message,
            last_math_result=last_math_result,
        )

        if not data:
            return None

        if not data.get("is_math"):
            return None

        expression = data.get("expression")

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
                    "en",
                )
            ),
        )

    def _call_llm(
        self,
        user_message: str,
        last_math_result: float | None,
    ) -> dict | None:

        prompt = build_context_prompt(
            user_message=user_message,
            last_math_result=last_math_result,
        )

        response = self.llm_service.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": "Return only valid JSON.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return None

    def _normalize_language(
        self,
        language: str,
    ) -> str:

        if not language:
            return "en"

        return language.lower()[:2]

    def _is_valid_candidate(
        self,
        text: str,
    ) -> bool:

        return bool(
            re.search(
                r"\d|[\+\-\*/()]|mais|menos|vezes|divid|som|sub|mult|calc|equa|express|plus|minus|times|divide",
                text.lower(),
            )
        )
