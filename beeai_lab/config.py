"""Environment and model configuration.

Replaces the lab's ``t1.py``. In the original lab, ``t1.py`` set
``WATSONX_PROJECT_ID`` inside its own process, which does not carry over to the
other scripts. Here, :func:`configure_environment` runs at the start of every
example, so the settings are always applied to the process that needs them.

Every value can be overridden with an environment variable or a ``.env`` file
in the project root (see ``.env.example``).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Default used inside the IBM Skills Network lab environment.
SKILLS_NETWORK_PROJECT_ID = "skills-network"

# ---------------------------------------------------------------------------
# Default models (same ones the lab uses)
# ---------------------------------------------------------------------------
DEFAULT_CHAT_MODEL = "watsonx:ibm/granite-4-h-small"  # sections 2-3
DEFAULT_STRUCTURED_MODEL = "openai:gpt-5-nano"  # section 4
DEFAULT_AGENT_MODEL = "watsonx:meta-llama/llama-4-maverick-17b-128e-instruct-fp8"  # sections 5-12

# Credentials each provider needs. The URL/region pair is "one of".
PROVIDER_ENV_VARS: dict[str, list[str]] = {
    "watsonx": ["WATSONX_PROJECT_ID", "WATSONX_API_KEY", "WATSONX_URL | WATSONX_REGION"],
    "openai": ["OPENAI_API_KEY"],
}


@dataclass(frozen=True)
class ModelSettings:
    """Which model to call and with what sampling temperature.

    ``temperature=None`` means "use the provider default". GPT-5 models only
    accept the default temperature, so passing ``0`` to them fails.
    """

    name: str
    temperature: float | None = 0.0

    @property
    def provider(self) -> str:
        return self.name.split(":", 1)[0]


@dataclass(frozen=True)
class LabSettings:
    chat: ModelSettings
    structured: ModelSettings
    agent: ModelSettings


def _load_dotenv() -> None:
    """Load ``.env`` from the project root if python-dotenv is installed."""
    try:
        from dotenv import load_dotenv
    except ImportError:  # optional dependency
        return
    load_dotenv(PROJECT_ROOT / ".env", override=False)


def _temperature_for(model_name: str, default: float | None = 0.0) -> float | None:
    # GPT-5 family rejects temperature != 1, so leave it unset.
    return None if model_name.startswith("openai:gpt-5") else default


def configure_environment() -> None:
    """Apply lab defaults without overwriting anything already set."""
    _load_dotenv()
    os.environ.setdefault("WATSONX_PROJECT_ID", SKILLS_NETWORK_PROJECT_ID)


def get_settings() -> LabSettings:
    """Read model choices from the environment, falling back to lab defaults."""
    chat = os.getenv("BEEAI_CHAT_MODEL", DEFAULT_CHAT_MODEL)
    structured = os.getenv("BEEAI_STRUCTURED_MODEL", DEFAULT_STRUCTURED_MODEL)
    agent = os.getenv("BEEAI_AGENT_MODEL", DEFAULT_AGENT_MODEL)
    return LabSettings(
        chat=ModelSettings(chat, _temperature_for(chat)),
        structured=ModelSettings(structured, _temperature_for(structured)),
        agent=ModelSettings(agent, _temperature_for(agent)),
    )


def model_settings_for(model_name: str) -> ModelSettings:
    """Build settings for an ad-hoc model name (used by the ``--model`` flag)."""
    return ModelSettings(model_name, _temperature_for(model_name))


def credential_report() -> dict[str, dict[str, bool]]:
    """Return which credential variables are set, per provider (values never shown)."""
    report: dict[str, dict[str, bool]] = {}
    for provider, names in PROVIDER_ENV_VARS.items():
        report[provider] = {
            name: any(os.getenv(part.strip()) for part in name.split("|")) for name in names
        }
    return report
