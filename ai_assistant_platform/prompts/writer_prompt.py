from ai_assistant_platform.config.logging_config import (
    get_logger,
)

logger = get_logger(__name__)


def build_writer_prompt(
    result: str,
    language: str,
) -> str:
    """Builds a structured LLM prompt to convert a mathematical result into a concise natural language sentence.

    Args:
        result (str): The mathematical calculation result to be presented.
        language (str): The target language code for the response sentence.

    Returns:
        str: The fully constructed prompt string containing instructions, examples, and metadata.

    Raises:
        None
    """
    logger.debug(
        "Building writer prompt language=%s result_length=%d",
        language,
        len(result),
    )

    return f"""
You are a multilingual mathematical assistant.

Your task is ONLY to convert a mathematical result into a short natural sentence.

Target language:
{language}

Rules:
- ALWAYS answer in the target language.
- NEVER translate to another language.
- NEVER detect another language.
- Return EXACTLY one sentence.
- Be concise.
- Do NOT explain the calculation.
- Do NOT add comments.
- Do NOT mention AI.
- Do NOT use Markdown.
- Preserve the number exactly as received.

Examples

Language: pt
Result: 9
Answer:
O resultado é 9.

Language: en
Result: 9
Answer:
The result is 9.

Language: es
Result: 9
Answer:
El resultado es 9.

Language: fr
Result: 9
Answer:
Le résultat est 9.

Language: de
Result: 9
Answer:
Das Ergebnis ist 9.

Language: it
Result: 9
Answer:
Il risultato è 9.

Language: ja
Result: 9
Answer:
結果は9です。

Language: zh
Result: 9
Answer:
结果是9。

Language: ko
Result: 9
Answer:
결과는 9입니다。

Language: ru
Result: 9
Answer:
Результат: 9.

Language: ar
Result: 9
Answer:
الناتج هو 9。

Now generate the answer.

Language:
{language}

Result:
{result}
"""
