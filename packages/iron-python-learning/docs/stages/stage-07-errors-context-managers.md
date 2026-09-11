# Stage 07 - Errors and Context Managers

Stage 07 is about failure boundaries and resource lifecycle.

| Python | Java |
| --- | --- |
| `raise ... from exc` | exception wrapping with cause |
| `try/except/finally` | `try/catch/finally` |
| context manager | `try-with-resources` |
| `with` | automatic enter/exit lifecycle |

## Key Ideas

Python has no checked exceptions. That means the code must be disciplined about where exceptions are translated into domain errors.

Use `raise NewError(...) from exc` when preserving the cause matters. Do not throw away the original exception by accident.

Use context managers for lifecycle: files, locks, transactions, spans, temporary state, and cleanup-heavy operations.

## Code

See `src/iron_python_learning/stages/stage_07_errors_context.py`.
