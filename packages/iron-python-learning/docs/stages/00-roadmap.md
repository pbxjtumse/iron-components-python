# Python Learning 10 Stages Roadmap

This roadmap is the first stable learning skeleton. The order follows the path from language basics to a small technical component.

| Stage | Topic | Java Analogy | Output |
| --- | --- | --- | --- |
| 01 | Basic syntax, control flow, exceptions, modules | Java syntax, `if/for`, checked vs unchecked exception, utility classes | Understand Python's basic execution model |
| 02 | Object model, references, mutability, copy | Java reference variables, immutable `String`, shallow copy | Avoid mistakes around assignment and mutation |
| 03 | Type system, `Protocol`, `Annotated`, `TypeGuard` | Interface, generic type, annotation metadata, type narrowing | Write typed Python without pretending it is Java |
| 04 | Functions, modules, packages | Method overload habits, utility classes, Maven module boundary | Build Python modules with explicit dependencies |
| 05 | OOP, dataclass, ABC, composition | POJO, record, abstract class, interface | Model domain objects and service contracts |
| 06 | Collections, iterators, generators | Collections, Stream API, Iterator | Process data in Pythonic style |
| 07 | Errors, context managers, resource lifecycle | `try-with-resources`, exception wrapping | Handle failure and cleanup cleanly |
| 08 | I/O, path, JSON, serialization | Jackson, `Path`, DTO mapping | Read/write data safely with standard library tools |
| 09 | Async and concurrency | Thread pool, `CompletableFuture`, virtual-thread style thinking | Understand `asyncio` before touching AI workflows |
| 10 | Mini technical component | Java component API/SPI/Core/Provider | Build a small Python component using ports and adapters |

## Package Rule

Learning code stays in `iron-python-learning`. Real reusable capabilities should later move to packages such as `iron-foundation`, `iron-retry`, or AI packages only after the API shape is clear.
