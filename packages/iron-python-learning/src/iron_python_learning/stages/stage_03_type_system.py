from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Protocol, TypeGuard, get_type_hints

OrderId = Annotated[str, "non-empty order id"]


@dataclass(frozen=True)
class Envelope:
    order_id: OrderId
    payload: dict[str, object]


class Runnable(Protocol):
    def run(self) -> str:
        ...


class EmailJob:
    def __init__(self, address: str) -> None:
        self.address = address

    def run(self) -> str:
        return f"send email to {self.address}"


def is_str_list(value: object) -> TypeGuard[list[str]]:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def execute(job: Runnable) -> str:
    return job.run()


def demo() -> dict[str, object]:
    unknown: object = ["python", "typing"]
    narrowed = unknown if is_str_list(unknown) else []

    hints = get_type_hints(Envelope, include_extras=True)

    return {
        "topic": "Protocol, Annotated, TypeGuard, type hints",
        "protocol_result": execute(EmailJob("dev@example.com")),
        "narrowed_upper": [item.upper() for item in narrowed],
        "order_id_hint": repr(hints["order_id"]),
    }
