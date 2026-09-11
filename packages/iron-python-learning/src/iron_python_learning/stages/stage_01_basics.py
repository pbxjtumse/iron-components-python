from __future__ import annotations


def normalize_status(raw_status: str) -> str:
    status = raw_status.strip().lower()
    if status in {"ok", "success"}:
        return "SUCCESS"
    if status in {"fail", "failed", "error"}:
        return "FAILED"
    return "UNKNOWN"


def divide(left: int, right: int) -> float:
    try:
        return left / right
    except ZeroDivisionError as exc:
        raise ValueError("right must not be zero") from exc


def demo() -> dict[str, object]:
    left = ["order-1"]
    right = ["order-1"]
    same_value = left == right
    same_object = left is right

    statuses = [normalize_status(item) for item in [" ok ", "FAILED", "missing"]]

    try:
        divide(10, 0)
    except ValueError as exc:
        error_message = str(exc)

    return {
        "topic": "basic syntax, equality, exceptions, module functions",
        "same_value_with_equals": same_value,
        "same_object_with_is": same_object,
        "normalized_statuses": statuses,
        "wrapped_error": error_message,
    }
