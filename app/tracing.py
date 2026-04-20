from __future__ import annotations

import os
from typing import Any

try:
    from langfuse import observe, Langfuse

    _langfuse_client = None

    def _get_client() -> Langfuse:
        global _langfuse_client
        if _langfuse_client is None:
            _langfuse_client = Langfuse()
        return _langfuse_client

    class _LangfuseContext:
        """Adapter mapping old langfuse_context calls to Langfuse v3+ API."""

        def update_current_trace(self, **kwargs: Any) -> None:
            lf = _get_client()
            span_kwargs = {}
            if "metadata" in kwargs:
                span_kwargs["metadata"] = kwargs["metadata"]
            if span_kwargs:
                lf.update_current_span(**span_kwargs)

        def update_current_observation(self, **kwargs: Any) -> None:
            lf = _get_client()
            if kwargs.get("model") or kwargs.get("usage") or kwargs.get("usage_details"):
                gen_kwargs = {}
                if "model" in kwargs:
                    gen_kwargs["model"] = kwargs["model"]
                if "input" in kwargs:
                    gen_kwargs["input"] = kwargs["input"]
                if "output" in kwargs:
                    gen_kwargs["output"] = kwargs["output"]
                usage = kwargs.get("usage") or kwargs.get("usage_details")
                if usage:
                    gen_kwargs["usage_details"] = usage
                if "metadata" in kwargs:
                    gen_kwargs["metadata"] = kwargs["metadata"]
                try:
                    lf.update_current_generation(**gen_kwargs)
                except Exception:
                    pass
            else:
                span_kwargs = {}
                if "metadata" in kwargs:
                    span_kwargs["metadata"] = kwargs["metadata"]
                if span_kwargs:
                    lf.update_current_span(**span_kwargs)

        def flush(self) -> None:
            _get_client().flush()

    langfuse_context = _LangfuseContext()

except Exception:
    from typing import Callable

    def observe(*args: Any, **kwargs: Any) -> Callable:  # type: ignore[misc]
        def decorator(func: Callable) -> Callable:
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kw: Any) -> None: ...
        def update_current_observation(self, **kw: Any) -> None: ...
        def flush(self) -> None: ...

    langfuse_context = _DummyContext()  # type: ignore[assignment]


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
