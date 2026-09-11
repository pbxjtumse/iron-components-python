from __future__ import annotations

import asyncio


async def fetch_metric(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name}:ok"


async def collect_metrics() -> list[str]:
    async with asyncio.TaskGroup() as group:
        cpu = group.create_task(fetch_metric("cpu", 0.01))
        memory = group.create_task(fetch_metric("memory", 0.01))
    return [cpu.result(), memory.result()]


def demo() -> dict[str, object]:
    return {
        "topic": "asyncio, await, TaskGroup, structured concurrency",
        "metrics": asyncio.run(collect_metrics()),
    }
