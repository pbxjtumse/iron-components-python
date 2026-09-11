# Stage 08 - I/O, JSON, Serialization

Stage 08 introduces common standard-library tools for reading, writing, and serializing data.

| Python | Java |
| --- | --- |
| `pathlib.Path` | `java.nio.file.Path` |
| `json` module | Jackson basic usage |
| `dataclasses.asdict` | DTO to map conversion |
| file context manager | `try-with-resources` file handling |

## Key Ideas

Use `pathlib.Path` instead of string path manipulation.

Use the standard `json` module for basic JSON. Reach for Pydantic or other libraries when validation and schema behavior become important.

Serialization should be explicit. A Python object is not automatically a stable API payload.

## Code

See `src/iron_python_learning/stages/stage_08_io_serialization.py`.
