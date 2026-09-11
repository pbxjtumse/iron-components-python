# Stage 09 - Async and Concurrency

Stage 09 builds the mental model for `asyncio` before AI workflow frameworks are introduced.

| Python | Java |
| --- | --- |
| coroutine | async task body, close to a `CompletableFuture` supplier idea |
| `await` | wait for async result without blocking the event loop thread |
| `asyncio.TaskGroup` | structured concurrent task group |
| event loop | scheduler for async I/O work |

## Key Ideas

`asyncio` is mainly for I/O concurrency, not CPU-heavy parallel computation.

Calling an async function does not immediately execute all work like a normal blocking function. It returns a coroutine object that must be awaited or scheduled.

Structured concurrency with `TaskGroup` makes sibling task lifecycle easier to reason about.

## Code

See `src/iron_python_learning/stages/stage_09_concurrency_async.py`.
