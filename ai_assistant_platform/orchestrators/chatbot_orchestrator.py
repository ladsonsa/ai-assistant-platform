from ai_assistant_platform.agents.mathematical_agent import (
    MathematicalAgent,
)
from ai_assistant_platform.agents.writer_agent import (
    WriterAgent,
)
from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.core.context_resolver import (
    ContextResolver,
)
from ai_assistant_platform.llm.llm_service import (
    LLMService,
)
from ai_assistant_platform.tools.expression_evaluator import (
    ExpressionEvaluator,
)

logger = get_logger(__name__)


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
        self._llm_service = llm_service if llm_service is not None else LLMService()

        logger.info(
            "Initializing ChatbotOrchestrator with provider=%s",
            self._llm_service.provider_name,
        )

        self._context_resolver = ContextResolver(
            llm_service=self._llm_service,
        )

        evaluator = ExpressionEvaluator()

        self._mathematical_agent = MathematicalAgent(
            evaluator=evaluator,
        )

        self._writer_agent = WriterAgent(
            llm_service=self._llm_service,
        )

        logger.info("ChatbotOrchestrator initialized successfully")

    def process_message(
        self,
        user_message: str,
        conversation_history: list[dict],
    ) -> dict:
        logger.info(
            "Processing message length=%d history_size=%d",
            len(user_message),
            len(conversation_history),
        )

        last_math_result = self._extract_last_math_result(
            conversation_history,
        )

        math_context = self._context_resolver.resolve(
            user_message=user_message,
            last_math_result=last_math_result,
        )

        if math_context is None:
            logger.info("Non-math message detected. Returning refusal.")
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

        logger.debug(
            "Resolved math expression=%s language=%s use_previous_result=%s",
            expression,
            math_context.language,
            math_context.use_previous_result,
        )

        try:
            result = self._mathematical_agent.execute(
                expression=expression,
            )

        except ZeroDivisionError:
            logger.warning(
                "Division by zero detected expression=%s",
                expression,
            )

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
            logger.warning(
                "Mathematical evaluation failed expression=%s error=%s",
                expression,
                exc,
            )

            error_response = self._writer_agent.generate_error_response(
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

        except RuntimeError as exc:
            logger.exception(
                "Infrastructure failure while processing message",
            )
            return {
                "response": str(exc),
                "metadata": {},
                "usage": {},
            }

        response = self._writer_agent.generate_response(
            result=result,
            language=math_context.language,
        )

        logger.info(
            "Message processed successfully result=%s language=%s",
            result,
            math_context.language,
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
