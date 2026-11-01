"""Mustache-style prompt templates (lab section 3).

The lab's version converted ``{{name}}`` to ``{name}`` and called
``str.format``, which breaks on any other brace in the template (a JSON
example, say). This version substitutes placeholders directly and reports
missing variables clearly. The public API (``SimplePromptTemplate(...).render``)
is unchanged.
"""

from __future__ import annotations

import re
import textwrap
from collections.abc import Mapping
from typing import Any

_PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")


class MissingTemplateVariableError(KeyError):
    """Raised when a template placeholder has no matching variable."""


class SimplePromptTemplate:
    """Simple prompt template using ``{{variable}}`` placeholders."""

    def __init__(self, template: str) -> None:
        self.template = textwrap.dedent(template).strip()

    @property
    def variables(self) -> set[str]:
        """Names of all placeholders in the template."""
        return set(_PLACEHOLDER.findall(self.template))

    def render(self, variables: Mapping[str, Any]) -> str:
        """Render the template with the provided variables."""
        missing = self.variables - set(variables)
        if missing:
            raise MissingTemplateVariableError(f"Missing template variables: {sorted(missing)}")
        return _PLACEHOLDER.sub(lambda m: str(variables[m.group(1)]), self.template)
