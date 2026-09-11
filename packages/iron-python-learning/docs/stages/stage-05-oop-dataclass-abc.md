# Stage 05 - OOP, Dataclass, ABC

Stage 05 maps Python object-oriented tools to Java habits.

| Python | Java |
| --- | --- |
| `@dataclass` | Lombok `@Data`, Java record, simple DTO |
| `@dataclass(frozen=True)` | immutable value object |
| `ABC` | abstract class with abstract methods |
| `Protocol` | interface by structure, not declaration |
| composition | the same design preference as Java service composition |

## Key Ideas

Use `dataclass` for data carriers and value objects. Do not write manual constructor code until there is a real reason.

Use `ABC` when inheritance and explicit subclassing are part of the design. Use `Protocol` when you only care that an object has the right methods.

Python supports inheritance, but the default engineering style should still prefer composition for service wiring.

## Code

See `src/iron_python_learning/stages/stage_05_oop_dataclass.py`.
