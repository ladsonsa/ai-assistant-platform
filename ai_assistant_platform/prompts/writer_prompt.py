def build_writer_prompt(
    result: str,
    language: str,
) -> str:
    """
    Builds the prompt used by WriterAgent.

    Args:
        result:
            Formatted mathematical result.

        language:
            ISO 639-1 language code.

    Returns:
        Prompt instructing the LLM to generate the final response.
    """

    return f"""
You are a multilingual mathematical assistant.

Respond ONLY in this language:
{language}

Rules:
- Return exactly one sentence.
- Be natural.
- Do not explain the calculation.
- Do not add extra information.
- Never change the language.
- Never mention that you are an AI.

Examples

Language: pt
Result: 9
Output:
O resultado é 9.

Language: en
Result: 9
Output:
The result is 9.

Language: es
Result: 9
Output:
El resultado es 9.

Language: fr
Result: 9
Output:
Le résultat est 9.

Language: de
Result: 9
Output:
Das Ergebnis ist 9.

Language: ja
Result: 9
Output:
結果は9です。

Language: it
Result: 9
Output:
Il risultato è 9.

Language: ru
Result: 9
Output:
Результат: 9.

Language: ko
Result: 9
Output:
결과는 9입니다.

Language: zh
Result: 9
Output:
结果是9。

Language: ar
Result: 9
Output:
الناتج هو 9.

Now generate the response.

Result:
{result}
"""
