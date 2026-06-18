from pydantic import BaseModel

from chatbot_ai.tools.math_operations import add, subtract, multiply, divide


class mathematical_agent:

    def __init__(self):
        pass

    def solve(self, operation, number_1, number_2):
        pass

        if operation == "addition":
            return math_operations.add(number_1, number_2)

        if operation == "subtraction":
            return math_operations.subtract(number_1, number_2)

        if operation == "multiplication":
            return math_operations.multiply(number_1, number_2)

        if operation == "division":
            return math_operations.divide(number_1, number_2)

        raise ValueError("Unsupported operation.")
