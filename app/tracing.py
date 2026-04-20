from __future__ import annotations

import os
from typing import Any

from langfuse import observe
from langfuse import get_client

langfuse = get_client()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


def flush_traces() -> None:
    langfuse.flush()
