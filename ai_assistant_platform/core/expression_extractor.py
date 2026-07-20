import re


class ExpressionExtractor:
    """Extracts and sanitizes mathematical expressions from multilingual conversational text."""

    def __init__(self):
        # Captura operadores válidos, números, parênteses e a variável de contexto $result
        self._math_char_pattern = re.compile(r"[\d\.\+\-\*\/\(\)\s\$]+")
        self._has_alpha_pattern = re.compile(r"[a-zA-Z]")
        self._has_digit_pattern = re.compile(r"\d")

    def extract(self, text: str) -> str | None:
        """Extracts a clean mathematical expression from raw conversational text.

        Args:
            text: The raw input string from the user in any language.

        Returns:
            str | None: The sanitized expression string, or None if invalid.
        """
        if not text:
            return None

        # 1. Normalização do Histórico/Contexto (Independente do idioma original)
        # Substitui variações comuns de "resultado anterior" por $result
        cleaned = self._normalize_context_tokens(text)

        # 2. Extração baseada em Padrão Geométrico/Matemático
        # Em vez de limpar palavras, nós ativamente *buscamos* onde a matemática começa
        match = self._math_char_pattern.search(cleaned)
        if not match:
            return None

        # Isola o bloco que mais se parece com uma expressão matemática
        raw_expression = match.group()

        # 3. Limpeza de formatação e espaços
        expression = (
            raw_expression.strip().replace("\n", "").replace("\r", "").replace(" ", "")
        )

        # 4. Validação de Segurança e Conteúdo
        # Garante que não vazaram letras/palavras sem querer na expressão filtrada
        # (Exceto a palavra '$result' que é permitida)
        check_for_letters = expression.replace("$result", "")
        if self._has_alpha_pattern.search(check_for_letters):
            return None

        # Garante que há algo calculável (um dígito ou a referência de contexto)
        if (
            not self._has_digit_pattern.search(expression)
            and "$result" not in expression
        ):
            return None

        return expression

    def _normalize_context_tokens(self, text: str) -> str:
        """Normalizes multilingual context keywords into a unified $result token."""
        cleaned = text.lower()

        # Mapeamento multilíngue para o contexto do resultado anterior
        context_keywords = [
            "resultado anterior",
            "resultado",
            "ans",
            "answer",
            "previous result",
            "last result",
            "resultado anterior",
            "résultat",
            "resultado",
        ]

        for keyword in context_keywords:
            if keyword in cleaned:
                cleaned = cleaned.replace(keyword, "$result")

        return cleaned
