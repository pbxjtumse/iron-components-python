# Stage 10 - Mini Technical Component Project

Stage 10 connects language learning back to the technical component direction.

The first mini project uses a tiny order number component to show a Python version of the API/SPI/Core/Provider split.

| Layer | Java Component Habit | Python Shape |
| --- | --- | --- |
| API | public interface and DTO | Protocol, dataclass, public function/class |
| Core | default implementation | plain class with injected dependencies |
| Provider | Redis/JDBC/etc. adapter | object satisfying a Protocol |
| Starter | Spring Boot auto config | later: factory function or framework integration |

## Key Ideas

Python can still use clean architecture. The difference is that the boundaries are lighter.

Use `Protocol` to define what core needs from adapters. This avoids forcing every provider to inherit from a base class.

Keep the first project small. The goal is to make the component shape visible, not to build a production framework on day one.

## Code

See `src/iron_python_learning/stages/stage_10_component_project.py`.
