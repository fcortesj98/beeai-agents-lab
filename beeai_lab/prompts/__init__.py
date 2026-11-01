"""Prompt templates, system instructions and sample queries."""

from beeai_lab.prompts import queries, system_prompts
from beeai_lab.prompts.templates import MissingTemplateVariableError, SimplePromptTemplate

__all__ = ["SimplePromptTemplate", "MissingTemplateVariableError", "queries", "system_prompts"]
