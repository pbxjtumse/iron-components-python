from __future__ import annotations

from copy import copy
from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    tags: list[str]


def append_tag(order: Order, tag: str) -> None:
    order.tags.append(tag)


def rebind_tags(tags: list[str]) -> list[str]:
    tags = ["new-list"]
    return tags


def demo() -> dict[str, object]:
    original = Order(order_id="order-1001", tags=["created"])
    shallow = copy(original)

    append_tag(original, "paid")
    rebound = rebind_tags(original.tags)

    return {
        "topic": "names, references, mutability, shallow copy",
        "original_tags": original.tags,
        "shallow_copy_sees_same_tag_list": shallow.tags,
        "same_tag_list_object": original.tags is shallow.tags,
        "rebound_local_list": rebound,
        "original_after_rebind_function": original.tags,
    }
