# Stage 06 - Collections, Iterators, Generators

Stage 06 is the bridge from Java Collections and Stream API to Python data processing.

| Python | Java |
| --- | --- |
| `list` | `ArrayList`-like ordered container |
| `dict` | `HashMap`, insertion ordered in modern Python |
| `set` | `HashSet` |
| comprehension | compact Stream/map/filter style expression |
| generator | lazy iterator, similar to lazy stream processing |

## Key Ideas

Python collections are direct and expressive. Start simple before introducing custom classes.

Comprehensions are good for small transformations. If the expression becomes hard to read, use a normal loop.

Generators are useful for lazy pipelines and large data. They are one-shot iterators, so do not expect to iterate the same generator repeatedly.

## Code

See `src/iron_python_learning/stages/stage_06_collections_iterators.py`.
