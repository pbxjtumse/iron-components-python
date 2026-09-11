from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str


@dataclass
class PaymentCommand:
    order_id: str
    amount: Money


class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, command: PaymentCommand) -> str:
        raise NotImplementedError


class AuditSink(Protocol):
    def record(self, event: str) -> None:
        ...


class MemoryAuditSink:
    def __init__(self) -> None:
        self.events: list[str] = []

    def record(self, event: str) -> None:
        self.events.append(event)


class FakePaymentGateway(PaymentGateway):
    def pay(self, command: PaymentCommand) -> str:
        return f"paid:{command.order_id}:{command.amount.amount}{command.amount.currency}"


class PaymentService:
    def __init__(self, gateway: PaymentGateway, audit_sink: AuditSink) -> None:
        self.gateway = gateway
        self.audit_sink = audit_sink

    def pay(self, command: PaymentCommand) -> str:
        result = self.gateway.pay(command)
        self.audit_sink.record(result)
        return result


def demo() -> dict[str, object]:
    audit = MemoryAuditSink()
    service = PaymentService(FakePaymentGateway(), audit)
    result = service.pay(PaymentCommand("order-1001", Money(99, "CNY")))

    return {
        "topic": "dataclass, frozen value object, ABC, Protocol, composition",
        "result": result,
        "audit_events": audit.events,
    }
