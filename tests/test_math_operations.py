from chatbot_ai.math_tools import (
    add,
    divide,
    multiply,
    subtract,
)


def test_add():
    assert add(4, 6) == 10


def test_divide():
    assert divide(16, 2) == 8


def test_multiply():
    assert multiply(2, 8) == 16


def test_subtract():
    assert subtract(15, 5) == 10
