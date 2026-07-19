from ai_assistant_platform.agents.mathematical_agent import (
    MathematicalAgent,
)

from ai_assistant_platform.agents.writer_agent import (
    WriterAgent,
)

from ai_assistant_platform.core.context_resolver import (
    ContextResolver,
)

from ai_assistant_platform.llm.llm_service import (
    LLMService,
)


class ChatbotOrchestrator:
    """
    Coordinates the complete chatbot execution pipeline.

    Flow:

        User Input
            ↓
        Context Resolver
            ↓
        Mathematical Agent
            ↓
        Writer Agent
            ↓
        Response
    """

    def __init__(
        self,
        llm_service: LLMService | None = None,
    ) -> None:

        self.llm_service = llm_service if llm_service is not None else LLMService()

        self.context_resolver = ContextResolver(
            llm_service=self.llm_service,
        )

        self.mathematical_agent = MathematicalAgent()

        self.writer_agent = WriterAgent(
            llm_service=self.llm_service,
        )

    def process_message(
        self,
        user_message: str,
        conversation_history: list[dict],
    ) -> dict:

        last_math_result = self._extract_last_math_result(
            conversation_history,
        )

        math_context = self.context_resolver.resolve(
            user_message=user_message,
            last_math_result=last_math_result,
        )

        if math_context is None:
            return {
                "response": self._refusal_message(),
                "metadata": {},
                "usage": {},
            }

        expression = math_context.expression

        if math_context.use_previous_result and last_math_result is not None:
            expression = expression.replace(
                "$result",
                str(last_math_result),
            )

        try:
            result = self.mathematical_agent.execute(
                expression=expression,
            )

        except ZeroDivisionError:
            error_messages = {
                "pt": "Erro: Divisão por zero não é permitida na matemática.",
                "en": "Error: Division by zero is not allowed.",
                "es": "Error: La división por cero no está permitida.",
            }

            lang = getattr(math_context, "language", "pt")
            response_text = error_messages.get(lang, error_messages["pt"])

            return {
                "response": response_text,
                "metadata": {"error": "ZeroDivisionError", "expression": expression},
                "usage": {},
            }

        except ValueError as exc:
            error_response = self.writer_agent.generate_error_response(
                user_message=user_message,
                error=str(exc),
            )

            return {
                "response": error_response["content"],
                "metadata": {},
                "usage": error_response.get(
                    "usage",
                    {},
                ),
            }

        response = self.writer_agent.generate_response(
            result=result,
            language=math_context.language,
        )

        return {
            "response": response["content"],
            "metadata": {
                "math_result": result,
                "expression": expression,
                "language": math_context.language,
            },
            "usage": response.get(
                "usage",
                {},
            ),
        }

    def _extract_last_math_result(
        self,
        conversation_history: list[dict],
    ) -> float | None:

        for message in reversed(
            conversation_history,
        ):
            metadata = message.get(
                "metadata",
                {},
            )

            if "math_result" in metadata:
                return metadata["math_result"]

        return None

    def _refusal_message(
        self,
    ) -> str:

        return (
            "Posso ajudar apenas com matemática básica, "
            "incluindo operações, expressões com parênteses "
            "e problemas matemáticos simples."
        )
