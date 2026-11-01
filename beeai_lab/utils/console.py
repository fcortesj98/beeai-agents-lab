"""Small console-output helpers so every example prints the same way."""

from __future__ import annotations

import shutil


def _width() -> int:
    return min(shutil.get_terminal_size((88, 20)).columns, 100)


def banner(title: str) -> None:
    line = "═" * _width()
    print(f"\n{line}\n {title}\n{line}")


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def labeled(label: str, text: str) -> None:
    """Print a labeled block, e.g. an agent's final answer."""
    print(f"\n{label}:\n{text}")


def exchange(user: str, assistant: str, *, user_label: str = "👤 Human", bot_label: str = "🤖 Agent") -> None:
    print(f"\n{user_label}: {user}")
    print(f"{bot_label}: {assistant}")
