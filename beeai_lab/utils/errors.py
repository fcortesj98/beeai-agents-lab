"""Turn opaque BeeAI/LiteLLM failures into actionable hints.

BeeAI wraps provider errors in generic ``FrameworkError`` / ``ChatModelError``
messages. These hints cover the failures that come up most often when running
this lab.
"""

from __future__ import annotations

import traceback

# (substrings to look for, case-insensitive; hint). First match wins.
_HINTS: list[tuple[tuple[str, ...], str]] = [
    (
        ("no module named 'mcp'",),
        "LiteLLM imports the 'mcp' package on every call. Install it with:\n"
        "    python3.11 -m pip install mcp\n"
        "or pin an older LiteLLM:  python3.11 -m pip install \"litellm<1.100\"",
    ),
    (
        ("'nonetype' object has no attribute 'choices'",),
        "The provider returned an empty response. Common causes: the model rejects a\n"
        "parameter (GPT-5 models only accept the default temperature), the model name\n"
        "is not available to your key, or LiteLLM is out of date. Re-run with\n"
        "BEEAI_DEBUG=1 to see the raw provider error.",
    ),
    (
        ("unsupported value: 'temperature'", "temperature' does not support"),
        "This model rejects the temperature setting. Use a different model with\n"
        "--model, or set the model through BEEAI_*_MODEL (GPT-5 models skip temperature).",
    ),
    (
        ("watsonx api key", "watsonx_apikey", "wx_api_key", "project_id and space_id", "api key is required"),
        "watsonx credentials look missing. Set WATSONX_API_KEY, WATSONX_PROJECT_ID and\n"
        "WATSONX_URL (or WATSONX_REGION). Run `python3.11 -m beeai_lab check-env`.",
    ),
    (
        ("openai_api_key", "incorrect api key"),
        "OpenAI credentials look missing. Set OPENAI_API_KEY, or run this example with a\n"
        "watsonx model via --model.",
    ),
]


def _full_text(exc: BaseException) -> str:
    """Concatenate the messages of the whole exception chain."""
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


def root_cause(exc: BaseException) -> BaseException:
    """Follow ``__cause__``/``__context__`` to the original exception.

    BeeAI reports most provider problems as a bare "Chat Model error"; the
    useful message (missing module, auth failure, bad parameter) is at the
    bottom of the chain.
    """
    seen: set[int] = set()
    while id(exc) not in seen:
        seen.add(id(exc))
        nxt = exc.__cause__ or exc.__context__
        if nxt is None:
            break
        exc = nxt
    return exc


def hint_for(exc: BaseException) -> str | None:
    text = _full_text(exc).lower()
    for needles, hint in _HINTS:
        if any(needle in text for needle in needles):
            return hint
    return None
