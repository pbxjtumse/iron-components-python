# Stage 04 - Functions, Modules, Packages

Stage 04 focuses on how Python organizes executable behavior.

For a Java engineer, the closest comparison is:

| Python | Java |
| --- | --- |
| function | static method or instance method, depending on where it lives |
| module file | one `.java` file plus utility-class style namespace |
| package directory | Java package or Maven module namespace |
| keyword argument | named parameter style call, but checked at runtime |
| `*args` / `**kwargs` | varargs plus a map of named arguments |

## Key Ideas

Python does not require every function to live inside a class. A plain module function is normal and often preferred for stateless behavior.

Default arguments are evaluated once when the function is defined. For mutable defaults, use `None` and create the object inside the function.

Python has no Java-style method overloading. Use clear function names, default parameters, `singledispatch`, or explicit branching.

## Code

See `src/iron_python_learning/stages/stage_04_functions_modules.py`.
