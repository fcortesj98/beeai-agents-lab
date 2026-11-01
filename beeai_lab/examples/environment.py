"""Section 1 — environment check (replaces ``t1.py``)."""

from __future__ import annotations

import os

from beeai_lab.config import configure_environment, credential_report, get_settings
from beeai_lab.examples.base import ExampleOptions
from beeai_lab.utils import console


def print_environment_report() -> bool:
    """Print model choices and which credentials are set. Returns True if all are set."""
    configure_environment()
    settings = get_settings()

    console.section("Models")
    for role, model in (("chat", settings.chat), ("structured", settings.structured), ("agent", settings.agent)):
        temp = "provider default" if model.temperature is None else model.temperature
        print(f"  {role:<11} {model.name}  (temperature: {temp})")

    console.section("Credentials (values are never printed)")
    needed = {m.provider for m in (settings.chat, settings.structured, settings.agent)}
    all_ok = True
    for provider, checks in credential_report().items():
        flag = "" if provider in needed else "  (not used by current models)"
        print(f"  {provider}{flag}")
        for name, present in checks.items():
            print(f"    {'✅' if present else '❌'} {name}")
            if provider in needed and not present:
                all_ok = False

    if os.environ.get("WATSONX_PROJECT_ID") == "skills-network":
        print("\n  ℹ️  WATSONX_PROJECT_ID is the Skills Network lab default ('skills-network').")
    print("\nEnvironment configured successfully!" if all_ok else "\nSome credentials are missing; see README → Setup.")
    return all_ok


async def run(options: ExampleOptions) -> None:
    print_environment_report()
