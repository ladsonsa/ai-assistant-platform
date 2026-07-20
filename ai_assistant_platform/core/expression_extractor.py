import re


class ExpressionExtractor:

    def extract(
        self,
        text: str,
    ) -> str | None:

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
            match.group()
            .strip()
            .replace("\n", "")
            .replace("\r", "")
            .replace(" ", "")
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