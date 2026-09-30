"""Async unit tests for ChatService concurrent request processing."""

import asyncio
from typing import Any
import threading
from unittest.mock import MagicMock

from ai_assistant_platform.api.mappers import ChatResponseMapper
from ai_assistant_platform.api.schemas import (
    ChatMessageSchema,
    ChatRequestSchema,
)
from ai_assistant_platform.services.chat_service import ChatService


def test_send_allows_independent_requests_to_progress_concurrently() -> None:
    """Tests that send enables concurrent execution for independent requests."""

    async def run_test() -> None:
        first_started = threading.Event()
        second_started = threading.Event()
        release_first = threading.Event()

        orchestrator = MagicMock()

        def process_message(
            user_message: str,
            conversation_history: list[dict[str, Any]],
        ) -> dict[str, Any]:
            if user_message == "first":
                first_started.set()
                release_first.wait(timeout=1)
            else:
                second_started.set()

            return {
                "response": user_message,
                "metadata": {},
                "usage": {},
            }

        orchestrator.process_message.side_effect = process_message

        original_to_schema = ChatResponseMapper.to_schema
        ChatResponseMapper.to_schema = staticmethod(
            lambda response: response
        )

        try:
            service = ChatService(orchestrator=orchestrator)

            first_request = ChatRequestSchema(
                history=[
                    ChatMessageSchema(
                        role="user",
                        content="first",
                    )
                ]
            )
            second_request = ChatRequestSchema(
                history=[
                    ChatMessageSchema(
                        role="user",
                        content="second",
                    )
                ]
            )

            first_task = asyncio.create_task(service.send(first_request))

            assert await asyncio.to_thread(first_started.wait, 1)

            second_task = asyncio.create_task(service.send(second_request))

            assert await asyncio.to_thread(second_started.wait, 1)

            release_first.set()

            first_response, second_response = await asyncio.gather(
                first_task,
                second_task,
            )

            assert first_response["response"] == "first"
            assert second_response["response"] == "second"
            assert orchestrator.process_message.call_count == 2
        finally:
            ChatResponseMapper.to_schema = original_to_schema

    asyncio.run(run_test())