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
            trace_kwargs = {}
            for key in ("user_id", "session_id", "tags", "metadata"):
                if key in kwargs:
                    trace_kwargs[key] = kwargs[key]
            if not trace_kwargs:
                return

            # Langfuse SDK <=3 exposes update_current_trace; SDK 4 removed it.
            if hasattr(lf, "update_current_trace"):
                try:
                    lf.update_current_trace(**trace_kwargs)
                    return
                except Exception:
                    pass

            # Fallback for SDK 4+: persist trace-like fields on current span metadata.
            metadata: dict[str, Any] = {}
            existing_metadata = trace_kwargs.get("metadata")
            if isinstance(existing_metadata, dict):
                metadata.update(existing_metadata)
            elif existing_metadata is not None:
                metadata["trace_metadata"] = existing_metadata

            if "user_id" in trace_kwargs:
                metadata["trace_user_id"] = trace_kwargs["user_id"]
            if "session_id" in trace_kwargs:
                metadata["trace_session_id"] = trace_kwargs["session_id"]
            if "tags" in trace_kwargs:
                metadata["trace_tags"] = trace_kwargs["tags"]

            if metadata:
                try:
                    lf.update_current_span(metadata=metadata)
                except Exception:
                    pass

        def update_current_span(self, **kwargs: Any) -> None:
            lf = _get_client()
            span_kwargs = {}
            if "metadata" in kwargs:
                span_kwargs["metadata"] = kwargs["metadata"]
            usage = kwargs.get("usage") or kwargs.get("usage_details")
            if usage:
                span_kwargs["usage_details"] = usage
            if span_kwargs:
                try:
                    lf.update_current_span(**span_kwargs)
                except TypeError:
                    # Older/newer SDK variants may not accept usage details on spans.
                    if "usage_details" in span_kwargs:
                        del span_kwargs["usage_details"]
                        if span_kwargs:
                            lf.update_current_span(**span_kwargs)
                except Exception:
                    pass

        def update_current_generation(self, **kwargs: Any) -> None:
            lf = _get_client()
            gen_kwargs = {}
            for key in ("model", "input", "output", "metadata"):
                if key in kwargs:
                    gen_kwargs[key] = kwargs[key]
            usage = kwargs.get("usage") or kwargs.get("usage_details")
            if usage:
                gen_kwargs["usage_details"] = usage
            if gen_kwargs:
                try:
                    lf.update_current_generation(**gen_kwargs)
                except TypeError:
                    if "usage_details" in gen_kwargs:
                        del gen_kwargs["usage_details"]
                        if gen_kwargs:
                            lf.update_current_generation(**gen_kwargs)
                except Exception:
                    pass

        def update_current_observation(self, **kwargs: Any) -> None:
            if kwargs.get("model") or kwargs.get("usage") or kwargs.get("usage_details"):
                self.update_current_generation(**kwargs)
            else:
                self.update_current_span(**kwargs)

        def flush(self) -> None:
            try:
                _get_client().flush()
            except Exception:
                pass

    langfuse_context = _LangfuseContext()
    langfuse = langfuse_context

except Exception:
    from typing import Callable

    def observe(*args: Any, **kwargs: Any) -> Callable:  # type: ignore[misc]
        def decorator(func: Callable) -> Callable:
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kw: Any) -> None: ...
        def update_current_span(self, **kw: Any) -> None: ...
        def update_current_generation(self, **kw: Any) -> None: ...
        def update_current_observation(self, **kw: Any) -> None: ...
        def flush(self) -> None: ...

    langfuse_context = _DummyContext()  # type: ignore[assignment]
    langfuse = langfuse_context


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
