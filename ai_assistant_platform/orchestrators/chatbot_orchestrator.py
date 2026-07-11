# ai_assistant_platform/orchestrators/chatbot_orchestrator.py

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
    Coordinates the complete chatbot execution flow.

    Pipeline:
        User Message
            ↓
        ContextResolver
            ↓
        MathematicalAgent
            ↓
        WriterAgent
            ↓
        Response
    """

    def __init__(self) -> None:

        self.llm_service = LLMService()

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
        """
        Executes the chatbot pipeline.
        """

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

            return {
                "response": self.writer_agent.generate_error_response(
                    user_message=user_message,
                    error="Division by zero.",
                ),
                "metadata": {},
            }

        except ValueError as exc:

            return {
                "response": self.writer_agent.generate_error_response(
                    user_message=user_message,
                    error=str(exc),
                ),
                "metadata": {},
            }

        response = self.writer_agent.generate_response(
            result=result,
            language=math_context.language,
        )

        return {
            "response": response,
            "metadata": {
                "math_result": result,
                "expression": expression,
            },
        }

    def _extract_last_math_result(
        self,
        conversation_history: list[dict],
    ) -> float | None:
        """
        Retrieves the last mathematical result stored in the conversation.
        """

        for message in reversed(conversation_history):

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
        """
        Default message for requests outside the chatbot scope.
        """

        return (
            "Posso ajudar apenas com matemática básica, incluindo "
            "operações, expressões com parênteses e problemas simples."
        )
