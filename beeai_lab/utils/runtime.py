"""Runtime setup shared by every entry point."""

from __future__ import annotations

import logging
import os


def quiet_logging() -> None:
    """Silence noisy asyncio warnings (same as the lab's ``main()`` functions)."""
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)


def enable_debug_if_requested() -> None:
    """Turn on LiteLLM debug output when ``BEEAI_DEBUG=1``."""
    if os.getenv("BEEAI_DEBUG", "").lower() not in {"1", "true", "yes"}:
        return
    try:
        import litellm

        litellm._turn_on_debug()
    except Exception:  # debugging aid only; never fail because of it
        logging.basicConfig(level=logging.DEBUG)
