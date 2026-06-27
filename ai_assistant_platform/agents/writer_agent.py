from ai_assistant_platform.service.llm_services import LLMService


class WriterAgent:
    WRITER_PROMPT = """
    You are a Writer Agent.

    Responsibilities:
        - Transform raw information into user-friendly answers.
        - Answer in the same language used by the user.
        - Improve readability.
        - Be clear and concise.

    Restrictions:
        - Never perform calculations.
        - Never invent numbers.
        - Use only the information received.

    Return only the final answer.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def writer_response(
        self,
        user_message: str,
        result: float,
    ) -> str:

        prompt = f"""
            User message:
            {user_message}

            Result:
            {result}
            """

        return self.llm_service.generate_response(
            messages=[
                {"role": "system", "content": self.WRITER_PROMPT},
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        )
