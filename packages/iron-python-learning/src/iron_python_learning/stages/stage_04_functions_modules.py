from __future__ import annotations


def build_headers(trace_id: str, **extra: str) -> dict[str, str]:
    headers = {"trace_id": trace_id}
    headers.update(extra)
    return headers


def collect_items(*items: str, prefix: str = "item") -> list[str]:
    return [f"{prefix}:{item}" for item in items]


def append_safely(item: str, values: list[str] | None = None) -> list[str]:
    result = [] if values is None else values
    result.append(item)
    return result


def demo() -> dict[str, object]:
    return {
        "topic": "functions, keyword args, varargs, safe defaults",
        "headers": build_headers("trace-001", tenant="bank", scene="learning"),
        "items": collect_items("a", "b", prefix="stage04"),
        "first_call": append_safely("one"),
        "second_call": append_safely("two"),
    }
