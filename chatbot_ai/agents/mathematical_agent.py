from pydantic import BaseModel

from chatbot_ai.tools.calculator import(
    add,
    subtract,
    multiply,
    divide
)

class mathematical_agent:

    def __init__(self):
        pass

    def solve(self, operation, number_1, number_2):
        pass

        if operation == "addition":
            return calculator.add(number_1, number_2)
    
        if operation == "subtraction":
            return calculator.subtract(number_1, number_2)
    
        if operation == "multiplication":
            return calculator.multiply(number_1, number_2)

        if operation == "division":
            return calculator.divide(number_1, number_2)

        raise ValueError("Unsupported operation.")
