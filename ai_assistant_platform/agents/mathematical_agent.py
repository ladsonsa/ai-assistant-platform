from ai_assistant_platform.tools.math_operations import add, subtract, multiply, divide


class MathematicalAgent:
    def __init__(self):
        pass

    def solve(self, operation: str, number_1: float, number_2: float) -> float:

        if operation == "addition":
            return add(number_1, number_2)

        elif operation == "subtraction":
            return subtract(number_1, number_2)

        elif operation == "multiplication":
            return multiply(number_1, number_2)

        elif operation == "division":
            return divide(number_1, number_2)

        raise ValueError("Unsupported operation.")
