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
    Coordinate the end-to-end processing of user messages.

    The orchestrator is responsible for managing the application workflow,
    delegating responsibilities to specialized components without
    implementing business logic itself.

    Processing pipeline:

    1. Retrieve the previous mathematical result from the conversation.
    2. Resolve the user's mathematical intent.
    3. Execute the requested mathematical operation.
    4. Generate a natural language response.
    5. Return the response together with metadata for future interactions.
    """

    def __init__(self):
        """
        Initialize the chatbot orchestrator.

        Creates and wires together all application components required to
        process mathematical conversations.
        """

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
        Process a user message through the complete chatbot pipeline.

        Args:
            user_message:
                Message submitted by the user.

            conversation_history:
                Complete conversation history stored by the application.

        Returns:
            A dictionary containing:

            - ``response``: Natural language response presented to the user.
            - ``metadata``: Internal metadata used to preserve conversation
              context across future requests.
        """

        last_math_result = self._extract_last_math_result(conversation_history)

        math_context = self.context_resolver.resolve(
            user_message=user_message,
            last_math_result=last_math_result,
        )

        if not math_context:
            return {
                "response": self._refusal_message(),
                "metadata": {},
            }

        try:
            result = self.mathematical_agent.execute(
                operation=math_context.operation,
                number_1=(
                    last_math_result
                    if math_context.use_previous_result
                    else math_context.left_operand
                ),
                number_2=math_context.right_operand,
            )
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
                "operation": math_context.operation,
            },
        }

    def _extract_last_math_result(
        self,
        conversation_history: list[dict],
    ) -> float | None:
        """
        Retrieve the most recent mathematical result from the conversation.

        Args:
            conversation_history:
                Conversation history including optional metadata.

        Returns:
            The last stored mathematical result if available; otherwise
            ``None``.
        """

        for message in reversed(conversation_history):

            metadata = message.get("metadata", {})

            if "math_result" in metadata:
                return metadata["math_result"]

        return None

    def _refusal_message(self) -> str:
        """
        Return the default response for unsupported requests.

        Returns:
            A message informing the user that only supported mathematical
            operations can be processed.
        """

        return (
            "Posso ajudar apenas com operações matemáticas "
            "básicas como soma, subtração, multiplicação e divisão."
        )
