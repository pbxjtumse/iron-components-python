from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol


class Clock(Protocol):
    def now(self) -> datetime:
        ...


class OrderNumberRepository(Protocol):
    def next_sequence(self, biz_date: str) -> int:
        ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class InMemoryOrderNumberRepository:
    def __init__(self) -> None:
        self._sequences: dict[str, int] = {}

    def next_sequence(self, biz_date: str) -> int:
        next_value = self._sequences.get(biz_date, 0) + 1
        self._sequences[biz_date] = next_value
        return next_value


@dataclass(frozen=True)
class OrderNumber:
    value: str
    biz_date: str
    sequence: int


class OrderNumberService:
    def __init__(self, clock: Clock, repository: OrderNumberRepository) -> None:
        self.clock = clock
        self.repository = repository

    def generate(self) -> OrderNumber:
        biz_date = self.clock.now().strftime("%Y%m%d")
        sequence = self.repository.next_sequence(biz_date)
        return OrderNumber(
            value=f"ORD{biz_date}{sequence:06d}",
            biz_date=biz_date,
            sequence=sequence,
        )


def demo() -> dict[str, object]:
    service = OrderNumberService(SystemClock(), InMemoryOrderNumberRepository())
    first = service.generate()
    second = service.generate()

    return {
        "topic": "mini component, Protocol ports, core service, in-memory provider",
        "first": first.value,
        "second": second.value,
        "same_biz_date": first.biz_date == second.biz_date,
    }
