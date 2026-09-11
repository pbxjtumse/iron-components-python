from __future__ import annotations

from collections.abc import Iterable, Iterator


def paid_order_ids(events: Iterable[dict[str, object]]) -> Iterator[str]:
    for event in events:
        if event.get("status") == "PAID":
            yield str(event["order_id"])


def demo() -> dict[str, object]:
    events = [
        {"order_id": "1001", "status": "CREATED", "amount": 12},
        {"order_id": "1002", "status": "PAID", "amount": 30},
        {"order_id": "1003", "status": "PAID", "amount": 18},
    ]

    amount_by_order = {str(event["order_id"]): int(event["amount"]) for event in events}
    high_value_orders = [order_id for order_id, amount in amount_by_order.items() if amount >= 20]

    return {
        "topic": "list, dict, set, comprehension, generator",
        "amount_by_order": amount_by_order,
        "paid_order_ids": list(paid_order_ids(events)),
        "high_value_orders": high_value_orders,
        "unique_statuses": {str(event["status"]) for event in events},
    }
