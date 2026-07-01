"""
Unit tests for basic mathematical operations.

This module validates the correctness of core arithmetic tools,
ensuring that addition, subtraction, multiplication, and division
behave as expected.
"""

from ai_assistant_platform.tools import (
    add,
    divide,
    multiply,
    subtract,
)


def test_add():
    """Verify that addition returns the correct sum."""
    assert add(4, 6) == 10


def test_divide():
    """Verify that division returns the correct quotient."""
    assert divide(16, 2) == 8


def test_multiply():
    """Verify that multiplication returns the correct product."""
    assert multiply(2, 8) == 16


def test_subtract():
    """Verify that subtraction returns the correct difference."""
    assert subtract(15, 5) == 10
