from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager


class LearningError(RuntimeError):
    pass


@contextmanager
def operation(name: str) -> Iterator[list[str]]:
    events: list[str] = [f"enter:{name}"]
    try:
        yield events
    except Exception as exc:
        events.append(f"error:{type(exc).__name__}")
        raise LearningError(f"operation failed: {name}") from exc
    finally:
        events.append(f"exit:{name}")


def parse_positive(raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise ValueError("value must be positive")
    return value


def demo() -> dict[str, object]:
    try:
        with operation("parse") as events:
            parse_positive("0")
    except LearningError as exc:
        error = str(exc)
        cause = type(exc.__cause__).__name__ if exc.__cause__ else None

    return {
        "topic": "exception wrapping, context manager, cleanup",
        "events": events,
        "error": error,
        "cause": cause,
    }
