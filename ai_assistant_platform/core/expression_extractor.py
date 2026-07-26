import re


class ExpressionExtractor:
    """Extracts and sanitizes mathematical expressions from natural language text.

    Attributes:
        None
    """

    def extract(
        self,
        text: str,
    ) -> str | None:
        """Extracts a valid mathematical expression from the given text string.

        Args:
            text (str): The input text containing a potential mathematical expression.

        Returns:
            str | None: The sanitized mathematical expression as a string if valid,
                or None if no valid expression can be extracted.

        Raises:
            None
        """

        cleaned = text.lower()

        for prefix in (
            "quanto é",
            "calcule",
            "calcule:",
            "resolve",
            "resolva",
        ):
            cleaned = cleaned.replace(
                prefix,
                "",
            )

        if "$result" in cleaned:
            cleaned = cleaned.replace(
                "resultado anterior",
                "$result",
            ).replace(
                "resultado",
                "$result",
            )

        text_without_result = cleaned.replace(
            "$result",
            "",
        )

        if re.search(
            r"[a-z]",
            text_without_result,
        ):
            return None

        match = re.search(
            r"[\d\.\+\-\*\/\(\)\s\$]+",
            cleaned,
        )

        if not match:
            return None

        expression = (
            match.group().strip().replace("\n", "").replace("\r", "").replace(" ", "")
        )

        if (
            not re.search(
                r"\d",
                expression,
            )
            and "$result" not in expression
        ):
            return None

        return expression
