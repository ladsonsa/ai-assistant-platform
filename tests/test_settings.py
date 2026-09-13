"""Tests for the application settings module."""

import importlib
from types import ModuleType

import _pytest.monkeypatch
import pytest

import ai_assistant_platform.config.settings as settings


def reload_settings(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    **values: str,
) -> ModuleType:
    """Helper function to update environment variables and reload the settings module.

    Args:
        monkeypatch: Pytest fixture for safely modifying environment variables.
        **values: Key-value pairs representing environment variable names and values.

    Returns:
        ModuleType: The reloaded settings module with updated configurations.
    """
    for name, value in values.items():
        monkeypatch.setenv(name, value)

    return importlib.reload(settings)


@pytest.mark.parametrize("provider", ["openai", "gemini", "ollama", "OPENAI"])
def test_valid_provider_names_are_accepted(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    provider: str,
) -> None:
    """Tests that valid LLM provider names (including case variations) are accepted."""
    module = reload_settings(monkeypatch, PROVIDER_NAME=provider)

    assert module.PROVIDER_NAME == provider


def test_provider_name_from_environment_is_preserved(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
) -> None:
    """Tests that the PROVIDER_NAME environment variable is accurately preserved upon module load."""
    module = reload_settings(monkeypatch, PROVIDER_NAME="gemini")

    assert module.PROVIDER_NAME == "gemini"


def test_empty_provider_name_is_rejected(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
) -> None:
    """Tests that an empty PROVIDER_NAME raises a ValueError during module load."""
    monkeypatch.setenv("PROVIDER_NAME", "")

    with pytest.raises(ValueError, match="PROVIDER_NAME must not be empty"):
        importlib.reload(settings)


def test_unsupported_provider_name_is_rejected(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
) -> None:
    """Tests that specifying an unknown provider name raises a ValueError."""
    monkeypatch.setenv("PROVIDER_NAME", "unknown")

    with pytest.raises(ValueError, match="Unsupported provider: unknown"):
        importlib.reload(settings)


@pytest.mark.parametrize("value", ["0", "2"])
def test_temperature_accepts_boundaries(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    value: str,
) -> None:
    """Tests that TEMPERATURE accepts valid boundary values [0, 2]."""
    module = reload_settings(monkeypatch, TEMPERATURE=value)

    assert module.TEMPERATURE == float(value)


@pytest.mark.parametrize("value", ["-0.1", "2.1"])
def test_temperature_rejects_values_outside_range(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    value: str,
) -> None:
    """Tests that TEMPERATURE values outside [0, 2] raise a ValueError."""
    monkeypatch.setenv("TEMPERATURE", value)

    with pytest.raises(ValueError, match="TEMPERATURE must be between 0 and 2"):
        importlib.reload(settings)


@pytest.mark.parametrize("value", ["1", "512"])
def test_max_tokens_accepts_positive_values(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    value: str,
) -> None:
    """Tests that MAX_TOKENS accepts valid positive integer values."""
    module = reload_settings(monkeypatch, MAX_TOKENS=value)

    assert module.MAX_TOKENS == int(value)


@pytest.mark.parametrize("value", ["0", "-1"])
def test_max_tokens_rejects_non_positive_values(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    value: str,
) -> None:
    """Tests that MAX_TOKENS values less than 1 raise a ValueError."""
    monkeypatch.setenv("MAX_TOKENS", value)

    with pytest.raises(
        ValueError,
        match="MAX_TOKENS must be greater than or equal to 1",
    ):
        importlib.reload(settings)


@pytest.mark.parametrize("value", ["0", "1"])
def test_top_p_accepts_boundaries(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    value: str,
) -> None:
    """Tests that TOP_P accepts valid boundary values [0, 1]."""
    module = reload_settings(monkeypatch, TOP_P=value)

    assert module.TOP_P == float(value)


@pytest.mark.parametrize("value", ["-0.1", "1.1"])
def test_top_p_rejects_values_outside_range(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    value: str,
) -> None:
    """Tests that TOP_P values outside [0, 1] raise a ValueError."""
    monkeypatch.setenv("TOP_P", value)

    with pytest.raises(ValueError, match="TOP_P must be between 0 and 1"):
        importlib.reload(settings)


@pytest.mark.parametrize("name", ["FREQUENCY_PENALTY", "PRESENCE_PENALTY"])
@pytest.mark.parametrize("value", ["-2", "0", "2"])
def test_penalties_accept_boundaries(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    name: str,
    value: str,
) -> None:
    """Tests that penalty settings accept valid boundary values [-2, 2]."""
    module = reload_settings(monkeypatch, **{name: value})

    assert getattr(module, name) == float(value)


@pytest.mark.parametrize("name", ["FREQUENCY_PENALTY", "PRESENCE_PENALTY"])
@pytest.mark.parametrize("value", ["-2.1", "2.1"])
def test_penalties_reject_values_outside_range(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    name: str,
    value: str,
) -> None:
    """Tests that penalty settings outside [-2, 2] raise a ValueError."""
    monkeypatch.setenv(name, value)

    with pytest.raises(
        ValueError,
        match=f"{name} must be between -2 and 2",
    ):
        importlib.reload(settings)


@pytest.mark.parametrize(
    "name",
    ["OPENAI_MODEL", "GEMINI_MODEL", "OLLAMA_MODEL"],
)
def test_empty_model_is_rejected(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
    name: str,
) -> None:
    """Tests that setting an empty model identifier raises a ValueError."""
    monkeypatch.setenv(name, "")

    with pytest.raises(ValueError, match=f"{name} must not be empty"):
        importlib.reload(settings)


def test_valid_custom_configuration_is_accepted(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
) -> None:
    """Tests that a fully custom set of valid environment variables loads correctly."""
    module = reload_settings(
        monkeypatch,
        PROVIDER_NAME="gemini",
        OPENAI_MODEL="custom-openai-model",
        GEMINI_MODEL="custom-gemini-model",
        OLLAMA_MODEL="custom-ollama-model",
        TEMPERATURE="2",
        MAX_TOKENS="1",
        TOP_P="0",
        FREQUENCY_PENALTY="-2",
        PRESENCE_PENALTY="2",
    )

    assert module.PROVIDER_NAME == "gemini"
    assert module.OPENAI_MODEL == "custom-openai-model"
    assert module.GEMINI_MODEL == "custom-gemini-model"
    assert module.OLLAMA_MODEL == "custom-ollama-model"
    assert module.TEMPERATURE == 2
    assert module.MAX_TOKENS == 1
    assert module.TOP_P == 0
    assert module.FREQUENCY_PENALTY == -2
    assert module.PRESENCE_PENALTY == 2
