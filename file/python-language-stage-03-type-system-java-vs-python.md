# Python 语言基础学习笔记：阶段 3 —— 类型系统（Java → Python 对照版）

> 学习目标：基于 Java 静态类型系统，系统理解 Python 的 Type Hint、Union、Optional、Generic、Callable、Protocol、ABC、TypedDict、NewType、Literal、Annotated、ParamSpec 等核心类型能力。  
> 适用对象：熟悉 Java，希望将 Python 用于生产级工程、技术组件、FastAPI 与 AI 应用开发。  
> Python 基线：Python 3.12  
> 核心原则：**Python 是动态语言，但生产级 Python 仍然需要用 Type Hint、静态检查和 Runtime Validation 建立清晰工程边界。**

---

# 1. 阶段 3 学习目标

阶段 1 解决：

> Python 代码怎么写。

阶段 2 解决：

> Python 对象为什么这样运行。

阶段 3 解决：

> Python 明明是动态语言，生产工程如何把 API、SPI、参数、返回值、泛型、回调、配置与边界约束清楚？

本阶段重点：

- Type Hint
- `T | None`
- Union
- `object`
- `Any`
- Generic
- TypeVar
- Python 3.12 泛型语法
- Callable
- Awaitable
- Protocol
- ABC
- Structural Typing
- Nominal Typing
- NewType
- Type Alias
- Literal
- TypedDict
- Final
- ClassVar
- Self
- overload
- cast
- isinstance / Narrowing
- TypeGuard
- Annotated
- ParamSpec
- Never
- `assert_never`
- Type Hint 与 Runtime Validation 的边界

---

# 2. Java → Python 类型系统总对照

| Java | Python | 作用 |
|---|---|---|
| `String` | `str` | 字符串 |
| `Integer` / `Long` | `int` | 整数 |
| `List<String>` | `list[str]` | 泛型 List |
| `Map<String,Object>` | `dict[str, object]` | Map |
| `Set<T>` | `set[T]` | Set |
| nullable `T` | `T | None` | 可空 |
| `Optional<T>` | `T | None` / `Optional[T]` | Python Optional 不是容器 |
| `Object` | `object` | 所有对象公共基类 |
| 无完全对应 | `Any` | 暂时退出静态类型检查 |
| `<T>` | `[T]` | Python 3.12 泛型参数 |
| `<T extends Base>` | `[T: Base]` | 泛型上界 |
| `Supplier<T>` | `Callable[[], T]` | 无参返回 T |
| `Consumer<T>` | `Callable[[T], None]` | 消费 T |
| `Function<A,B>` | `Callable[[A], B]` | 函数类型 |
| `Predicate<T>` | `Callable[[T], bool]` | 条件函数 |
| `interface` | `Protocol` / `ABC` | 接口 |
| `abstract class` | `ABC` | 抽象基类 |
| `record` / DTO | `dataclass` | 数据对象 |
| enum | `Enum / StrEnum` | 枚举 |
| `final` | `Final` | 静态不可重新绑定意图 |
| static field | `ClassVar` | 类属性 |
| overloaded method | `@overload` | 静态签名 |
| 强类型 ID wrapper | `NewType` | 领域类型 |
| DTO-shaped Map | `TypedDict` | 强类型 dict |
| Annotation Metadata | `Annotated` | 类型 + 元信息 |

---

# 3. Type Hint 不等于 Java Compile Type

Java：

```java
public String findName(long userId) {
    return "...";
}
```

调用：

```java
findName("1001");
```

编译直接失败。

Python：

```python
def find_name(user_id: int) -> str:
    return "..."
```

即使写：

```python
find_name("1001")
```

Python Runtime 默认也不会因为这个 Type Hint 自动拒绝执行。

所以 Type Hint 更准确地理解为：

```text
Static Type Contract
+
IDE
+
Pyright / mypy
+
Code Review
+
CI
```

而不是 Java 编译器那种强制 Runtime 类型边界。

---

# 4. Python 工程里的两套类型世界

Python 运行时：

```text
Python Runtime
    ↓
Runtime Object
```

静态分析：

```text
Source Code
    ↓
Type Hint
    ↓
Pyright / mypy / IDE / CI
```

因此要区分：

```text
Runtime Type
```

和：

```text
Static Type Analysis
```

这两个不是一回事。

---

# 5. 基础 Type Hint

Java：

```java
String name = "iron";
int count = 10;
boolean enabled = true;
```

Python：

```python
name: str = "iron"
count: int = 10
enabled: bool = True
```

但局部变量通常可以直接依赖类型推断：

```python
name = "iron"
count = 10
enabled = True
```

真正值得认真写 Type Hint 的地方是：

```text
Public API
Function Parameter
Function Return
SPI
Callback
Configuration
Public Attribute
```

---

# 6. 函数类型声明

Java：

```java
public String generate(String prefix) {
    return "...";
}
```

Python：

```python
def generate(prefix: str) -> str:
    return "..."
```

无返回值：

```python
def execute() -> None:
    ...
```

建议生产代码明确写：

```python
-> None
```

---

# 7. None 也是类型语义

Python：

```python
None
```

本身也是一个对象。

例如：

```python
type(None)
```

函数：

```python
def close() -> None:
    ...
```

表示：

> 正常返回值就是 None。

---

# 8. `T | None`

这是 Python 生产代码最常见的写法之一：

```python
def find_user(
    user_id: str,
) -> User | None:
    ...
```

表示：

```text
User
OR
None
```

---

# 9. Python Optional 与 Java Optional 不一样

Java：

```java
Optional<User>
```

是一个真实容器对象：

```text
Optional
   │
   └── User
```

Python：

```python
Optional[User]
```

实际等价：

```python
User | None
```

所以 Python `Optional[T]` 不是 Java 那种 Optional 容器。

---

# 10. Python 3.12 推荐的 Optional 写法

旧写法：

```python
from typing import Optional


def find_user() -> Optional[User]:
    ...
```

现代写法：

```python
def find_user() -> User | None:
    ...
```

对我们 Python 3.12 项目，优先使用后一种。

---

# 11. Union

传统：

```python
Union[str, int]
```

现代：

```python
str | int
```

例如：

```python
def normalize_id(value: str | int) -> str:
    return str(value)
```

Java 没有完全对应的 Union Type。

---

# 12. Union 不要滥用

例如：

```python
def execute(
    value: str | int | float | dict | list | None,
):
    ...
```

这种接口通常已经开始失去语义边界。

很像 Java：

```java
Object execute(Object value)
```

虽然灵活，但工程可维护性很差。

---

# 13. `object`

Python：

```python
object
```

粗略对应 Java：

```java
Object
```

例如：

```python
def print_value(value: object) -> None:
    print(value)
```

所有普通对象都能传。

但：

```python
value.foo()
```

类型检查器会阻止，因为 `object` 并没有承诺 `foo()`。

---

# 14. `Any`

Python：

```python
from typing import Any


def execute(value: Any) -> Any:
    ...
```

很多 Java 开发者会误认为：

```text
Any ≈ Object
```

这是错误的。

---

# 15. `object` vs `Any`

```python
value: object
value.foo()
```

静态检查器通常会报错。

但是：

```python
value: Any
value.foo().bar().xxx()
```

类型检查器通常会直接放行。

因此：

```text
object
=
不知道具体类型，但仍然接受类型系统约束。

Any
=
暂时退出静态类型系统。
```

---

# 16. Java 如何类比 Any

Java 没有完全等价物。

可以粗略理解为：

```text
Raw Type
+
Reflection
+
SuppressWarnings
```

混合起来的效果。

---

# 17. 技术组件不要泛滥 Any

不推荐：

```python
def execute(
    provider: Any,
    options: Any,
    callback: Any,
) -> Any:
    ...
```

这种代码看似“写了类型”，实际上几乎关闭了静态类型价值。

---

# 18. `dict[str, object]` vs `dict[str, Any]`

```python
data: dict[str, object]
```

表示 value 可以是任何对象，但取出来后需要重新判断类型。

而：

```python
data: dict[str, Any]
```

则会把 value 直接传播成 Any。

所以前者通常更安全。

---

# 19. Message Payload 应该怎么设计

如果 payload 真正是动态业务结构：

```python
payload: dict[str, object]
```

可以接受。

但明确领域结构：

```text
OrderCreatedPayload
UserCreatedPayload
PaymentResult
```

应优先建明确类型，而不是长期使用：

```python
dict[str, Any]
```

这和 Java 不推荐到处使用 `Map<String, Object>` 是一样的。

---

# 20. 容器类型

Java：

```java
List<String>
Set<Long>
Map<String, User>
```

Python：

```python
list[str]
set[int]
dict[str, User]
```

Tuple：

```python
tuple[str, int]
tuple[str, ...]
```

---

# 21. `tuple[str, int]` 与 `tuple[str, ...]`

```python
tuple[str, int]
```

表示：

```text
位置 0：str
位置 1：int
```

而：

```python
tuple[str, ...]
```

表示：

> 任意数量的 str。

---

# 22. API 参数不要默认都用 list

Java 有：

```java
List<User>
Collection<User>
Iterable<User>
```

Python 也有：

```python
list[User]
Collection[User]
Iterable[User]
Sequence[User]
```

应该根据 API 真正需要的能力来选。

---

# 23. Sequence

```python
from collections.abc import Sequence


def execute_all(
    tasks: Sequence[Task],
) -> None:
    ...
```

表示：

> 我需要一个有顺序、可读取的序列。

调用方可以传 `list`、`tuple` 等。

---

# 24. API 声明“最小所需能力”

如果函数只是遍历：

```python
for item in items:
    ...
```

那么：

```python
Iterable[Item]
```

可能已经足够。

没必要要求：

```python
list[Item]
```

因为 list 还额外承诺了 mutation、index 等能力。

---

# 25. Java 也有同样原则

不推荐：

```java
void execute(ArrayList<Task> tasks)
```

推荐：

```java
void execute(List<Task> tasks)
```

甚至：

```java
void execute(Collection<Task> tasks)
```

Python 也一样。

---

# 26. Mapping vs dict

如果 API 只读取：

```python
from collections.abc import Mapping


def execute(
    headers: Mapping[str, str],
) -> None:
    ...
```

通常比：

```python
dict[str, str]
```

更加抽象。

粗略可以理解：

```text
Mapping
≈
Java Map interface
```

而 `dict` 更接近一个具体实现。

---

# 27. Generic 泛型

Java：

```java
public class Box<T> {

    private final T value;

    public Box(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}
```

Python 3.12：

```python
class Box[T]:

    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value
```

---

# 28. 泛型对象

```python
string_box = Box("iron")
number_box = Box(100)
```

类型检查器可以推断：

```text
Box[str]
Box[int]
```

---

# 29. 泛型函数

Java：

```java
public static <T> T first(List<T> items) {
    return items.get(0);
}
```

Python 3.12：

```python
def first[T](items: list[T]) -> T:
    return items[0]
```

几乎一一对应。

---

# 30. 传统 TypeVar 写法

第三方代码仍会大量看到：

```python
from typing import TypeVar

T = TypeVar("T")


def first(items: list[T]) -> T:
    return items[0]
```

所以 Python 3.12 新旧泛型语法都要认识。

---

# 31. Generic 真正解决什么

Generic 不是：

> 什么类型都可以随便传。

真正解决：

> 输入类型和输出类型之间存在稳定关系。

```python
def first[T](items: list[T]) -> T:
    ...
```

传 `list[str]`，返回 `str`。

传 `list[User]`，返回 `User`。

---

# 32. object 会丢失类型关系

如果写：

```python
def first(items: list[object]) -> object:
    return items[0]
```

即使传 `list[str]`，静态返回类型仍然只是 `object`。

Generic 能保留输入与输出之间的关联。

---

# 33. Generic 对 Template 很重要

RetryTemplate：

```python
from collections.abc import Callable


class RetryTemplate:

    def execute[T](
        self,
        action: Callable[[], T],
    ) -> T:
        ...
```

调用：

```python
def load_order() -> Order:
    ...


order = retry_template.execute(load_order)
```

IDE 可以知道：

```text
order: Order
```

---

# 34. Java Template 对照

Java：

```java
public <T> T execute(Supplier<T> action) {
    ...
}
```

Python：

```python
def execute[T](
    action: Callable[[], T],
) -> T:
    ...
```

这个模式以后会大量出现在：

```text
RetryTemplate
TransactionTemplate
LockExecutionTemplate
CacheTemplate
```

---

# 35. Callable

Java：

```java
Function<String, Integer>
```

Python：

```python
from collections.abc import Callable

handler: Callable[[str], int]
```

表示：

```text
接收 str
返回 int
```

---

# 36. Java Functional Interface → Python Callable

| Java | Python |
|---|---|
| `Runnable` | `Callable[[], None]` |
| `Supplier<T>` | `Callable[[], T]` |
| `Consumer<T>` | `Callable[[T], None]` |
| `Function<A,B>` | `Callable[[A], B]` |
| `BiFunction<A,B,R>` | `Callable[[A,B], R]` |
| `Predicate<T>` | `Callable[[T], bool]` |

---

# 37. Callable 与技术模板

Java：

```java
transactionTemplate.execute(() -> {
    ...
});
```

Python：

```python
def create_order() -> Order:
    ...


order = transaction_template.execute(create_order)
```

Python 函数是一等对象，所以这种设计非常自然。

---

# 38. Async Callable

```python
async def load_user() -> User:
    ...
```

类型可以写：

```python
from collections.abc import Awaitable, Callable

action: Callable[[], Awaitable[User]]
```

链路：

```text
action()
↓
Awaitable[User]
↓
await
↓
User
```

---

# 39. Generic Bound

Java：

```java
<T extends BaseEvent>
```

Python 3.12：

```python
def publish[T: BaseEvent](event: T) -> T:
    ...
```

传统写法：

```python
TEvent = TypeVar(
    "TEvent",
    bound=BaseEvent,
)
```

---

# 40. Generic Constraint

```python
T = TypeVar(
    "T",
    str,
    bytes,
)
```

表示：

```text
T 只能是 str 或 bytes
```

区别：

```text
Bound
=
某个父类型及其子类型

Constraint
=
限定几个候选类型
```

---

# 41. Generic 不要泛滥

看到：

```python
class Executor[
    TRequest,
    TResponse,
    TContext,
    TOptions,
    TException,
]:
    ...
```

必须先问：

> 这些泛型真的建立了调用者关心的类型关系吗？

如果没有，就属于过度抽象。

---

# 42. 泛型不变性 Invariance

假设：

```python
class Animal:
    pass


class Dog(Animal):
    pass
```

虽然：

```text
Dog is Animal
```

但是：

```text
list[Dog]
```

并不是：

```text
list[Animal]
```

的子类型。

---

# 43. 为什么 list 是 invariant

假设允许：

```python
dogs: list[Dog]
animals: list[Animal] = dogs
```

那么：

```python
animals.append(Cat())
```

就会让 `dogs` 中出现 Cat。

因此 mutable generic 通常必须保持不变性。

---

# 44. Java 也是一样

Java：

```java
List<Dog>
```

不能直接赋值给：

```java
List<Animal>
```

原因完全相同。

---

# 45. Sequence 的协变价值

如果只是读取：

```python
def feed_all(
    animals: Sequence[Animal],
) -> None:
    ...
```

就比 `list[Animal]` 更灵活。

所以使用抽象 collection 不只是架构问题，也影响类型兼容性。

---

# 46. Protocol

这是 Python 技术组件中非常关键的能力。

Java：

```java
public interface IdGenerator {

    String generate();
}
```

Python：

```python
from typing import Protocol


class IdGenerator(Protocol):

    def generate(self) -> str:
        ...
```

---

# 47. Structural Typing

实现：

```python
class UuidGenerator:

    def generate(self) -> str:
        return "..."
```

`UuidGenerator` 不需要显式继承 `IdGenerator`。

只要方法结构满足，就满足 Protocol。

这就是：

> Structural Typing。

---

# 48. Java Nominal Typing

Java interface：

```java
interface IdGenerator {
}
```

实现必须：

```java
class UuidGenerator implements IdGenerator {
}
```

即使某个类方法结构完全一样，如果没 `implements`，Java 也不认为它属于这个接口类型。

---

# 49. Protocol 更像 Go interface

Protocol 关心：

```text
你有没有我要求的能力？
```

而不是：

```text
你有没有显式声明 implements？
```

---

# 50. Protocol 的工程价值

例如：

```python
class Clock(Protocol):

    def now_millis(self) -> int:
        ...
```

生产：

```python
class SystemClock:

    def now_millis(self) -> int:
        ...
```

测试：

```python
class FixedClock:

    def now_millis(self) -> int:
        return 123456789
```

两者都自然符合 Clock。

---

# 51. Protocol 特别适合 SPI / Port

例如：

```text
MessageProvider
LockProvider
IdGenerator
Clock
Serializer
RetryClassifier
MetricsRecorder
Repository Port
```

这些本质都在描述：

```text
Capability
Contract
SPI
Port
```

---

# 52. Protocol 与 Ports & Adapters

```python
class LockProvider(Protocol):

    def acquire(
        self,
        key: str,
    ) -> LockResult:
        ...
```

Core：

```python
class LockService:

    def __init__(
        self,
        provider: LockProvider,
    ) -> None:
        self._provider = provider
```

Redis：

```python
class RedisLockProvider:

    def acquire(
        self,
        key: str,
    ) -> LockResult:
        ...
```

不要求：

```python
RedisLockProvider(LockProvider)
```

结构：

```text
Core
 ↓
Protocol Port
 ↓
Provider / Adapter
```

非常符合 Hexagonal Architecture。

---

# 53. ABC

Python：

```python
from abc import ABC, abstractmethod


class IdGenerator(ABC):

    @abstractmethod
    def generate(self) -> str:
        ...
```

实现：

```python
class UuidGenerator(IdGenerator):

    def generate(self) -> str:
        ...
```

ABC 强调显式继承。

---

# 54. ABC 更接近 Java abstract class

ABC 可以承载：

```text
abstract method
concrete method
shared state
template method
shared implementation
```

例如：

```python
class BaseProvider(ABC):

    def validate(self) -> None:
        ...

    @abstractmethod
    def send(self) -> None:
        ...
```

---

# 55. Protocol vs ABC

| 场景 | Protocol | ABC |
|---|---:|---:|
| 只描述能力 | ★★★★★ | ★★★ |
| SPI / Port | ★★★★★ | ★★★ |
| 第三方实现兼容 | ★★★★★ | ★ |
| 不想强制继承 | ★★★★★ | ★ |
| Structural Typing | ✅ | ❌ |
| 共享实现 | ★★ | ★★★★★ |
| 共享状态 | ★ | ★★★★★ |
| Template Method | ★ | ★★★★★ |
| 强继承体系 | ★ | ★★★★★ |

推荐：

```text
Port / SPI → Protocol
Shared Implementation → ABC
```

---

# 56. ABC 有 Runtime 效果

如果 abstract method 没实现：

```python
class BadProvider(Provider):
    pass
```

直接实例化：

```python
BadProvider()
```

会失败。

所以 ABC 不只是静态检查。

---

# 57. Protocol 主要用于静态类型

```python
class Provider(Protocol):

    def send(self) -> None:
        ...
```

核心用途是：

```text
Static Type Checking
```

而不是 Runtime interface enforcement。

---

# 58. `@runtime_checkable`

如果真的需要：

```python
isinstance(obj, Provider)
```

可以：

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Provider(Protocol):

    def send(self) -> None:
        ...
```

但运行时 Protocol 检查比较粗，不应理解成 Java Compiler。

---

# 59. Duck Typing + Protocol

传统 Python：

```python
def execute(provider):
    provider.send()
```

这是 Duck Typing。

现代生产 Python：

```python
def execute(
    provider: Provider,
) -> None:
    provider.send()
```

得到：

```text
Duck Typing 灵活性
+
Static Type Safety
```

---

# 60. NewType

如果：

```python
user_id: str
order_id: str
message_id: str
```

底层都是 `str`，静态类型无法区分领域语义。

可以：

```python
from typing import NewType

UserId = NewType("UserId", str)
OrderId = NewType("OrderId", str)
```

---

# 61. NewType 示例

```python
def load_user(
    user_id: UserId,
) -> User:
    ...
```

```python
def load_order(
    order_id: OrderId,
) -> Order:
    ...
```

类型检查器就可以减少语义 ID 传错的问题。

---

# 62. Java 对照 NewType

Java 可能写：

```java
record UserId(String value) {}
record OrderId(String value) {}
```

Python `NewType` 更轻量，但主要作用于静态类型系统。

---

# 63. NewType 在技术组件中的用途

例如：

```text
OwnerToken
FencingToken
MessageId
BusinessKey
TraceId
```

底层可能全部是 `str`，但领域含义不同。

此时 NewType 很有价值。

---

# 64. Type Alias

Python 3.12：

```python
type Headers = Mapping[str, str]
```

这只是：

> 给复杂类型取一个别名。

---

# 65. Type Alias vs NewType

```python
type UserId = str
```

只是别名。

而：

```python
UserId = NewType("UserId", str)
```

表示新的静态领域类型。

---

# 66. Literal

```python
from typing import Literal

LogLevel = Literal[
    "debug",
    "info",
    "warning",
    "error",
]
```

函数：

```python
def configure_log(
    level: LogLevel,
) -> None:
    ...
```

静态检查器可以拒绝：

```python
configure_log("hello")
```

---

# 67. Literal vs Java Enum

Java：

```java
enum LogLevel {
    DEBUG,
    INFO,
    WARNING,
    ERROR
}
```

Python `Literal` 可以理解成：

> 轻量的固定值约束。

---

# 68. Literal vs Enum

Literal 更适合：

```text
简单固定参数
轻量字符串模式
内部小 API
```

Enum / StrEnum 更适合：

```text
稳定领域概念
状态
大量分支
需要方法
复用
序列化
```

---

# 69. TypedDict

JSON-like 数据：

```python
{
    "id": "1001",
    "name": "iron",
    "enabled": True,
}
```

可以写：

```python
from typing import TypedDict


class UserData(TypedDict):
    id: str
    name: str
    enabled: bool
```

---

# 70. TypedDict Runtime 仍是 dict

TypedDict 不是新的 Runtime Object。

运行时仍然是：

```python
dict
```

它只是提供：

```text
Static Schema
```

---

# 71. Java 对照 TypedDict

可以粗略理解成：

```text
Map<String,Object>
+
Static Schema
```

但稳定领域对象仍建议 dataclass / Pydantic / domain class。

---

# 72. TypedDict vs dataclass

| | TypedDict | dataclass |
|---|---|---|
| Runtime | dict | 真正对象 |
| 访问 | `data["id"]` | `data.id` |
| JSON-like | ★★★★★ | ★★★ |
| Domain Object | ★★ | ★★★★★ |
| 行为方法 | 不适合 | 适合 |
| 静态字段 | ✅ | ✅ |

---

# 73. Optional Key

```python
from typing import NotRequired, TypedDict


class MessageHeaders(TypedDict):
    trace_id: str
    tenant_id: NotRequired[str]
```

表示：

```text
trace_id 必须存在

tenant_id 可以不存在
```

---

# 74. `NotRequired[str]` 与 `str | None`

```python
tenant_id: str | None
```

表示：

> key 存在，但 value 可以是 None。

而：

```python
tenant_id: NotRequired[str]
```

表示：

> key 本身可以不存在。

这在 JSON、HTTP、Message Header 中很重要。

---

# 75. Final

```python
from typing import Final

MAX_RETRY: Final = 3
```

表示：

> 静态层面不应该再次赋值。

但 Runtime 默认仍能执行重新赋值。

所以它不是 Java `final` 的完全 Runtime 等价物。

---

# 76. ClassVar

```python
from typing import ClassVar


class RetryPolicy:
    DEFAULT_ATTEMPTS: ClassVar[int] = 3
```

粗略对应：

```java
static int DEFAULT_ATTEMPTS = 3;
```

---

# 77. Self

```python
from typing import Self


class Builder:

    def enable(self) -> Self:
        return self
```

用于：

> 返回当前具体类型。

对子类 fluent API 很有帮助。

---

# 78. Python 不支持 Java 那种 Runtime overload

Java：

```java
send(String text)
send(byte[] data)
```

Python 如果写：

```python
def send(value: str):
    ...


def send(value: bytes):
    ...
```

第二个定义会覆盖第一个。

---

# 79. `@overload`

Python：

```python
from typing import overload


@overload
def parse(value: str) -> TextResult:
    ...


@overload
def parse(value: bytes) -> BinaryResult:
    ...


def parse(
    value: str | bytes,
) -> TextResult | BinaryResult:
    ...
```

前两个只服务静态类型检查器。

最后一个才是真正 Runtime 实现。

---

# 80. Java overload vs Python overload

Java：

```text
多个 Runtime Method
```

Python：

```text
多个 Static Signature
+
一个 Runtime Implementation
```

---

# 81. cast

```python
from typing import cast

value: object = load()
user = cast(User, value)
```

注意：

> cast 不会真的把 value 转成 User。

---

# 82. Python cast 与 Java cast 的区别

Java：

```java
(User) value
```

Runtime 可能抛：

```text
ClassCastException
```

Python：

```python
cast(User, value)
```

Runtime 基本只是返回原对象，只影响静态检查器。

---

# 83. cast 不是类型转换

```python
cast(int, value)
```

不等于：

```python
int(value)
```

前者：

```text
Static Hint
```

后者：

```text
Runtime Conversion
```

---

# 84. isinstance 与 Type Narrowing

```python
value: object

if isinstance(value, str):
    print(value.upper())
```

进入 if 后，静态检查器知道：

```text
value: str
```

这叫 Type Narrowing。

---

# 85. None Narrowing

```python
user: User | None

if user is None:
    return

user.name
```

if 之后：

```text
user: User
```

---

# 86. TypeGuard

```python
from typing import TypeGuard


def is_string_list(
    values: list[object],
) -> TypeGuard[list[str]]:
    return all(
        isinstance(value, str)
        for value in values
    )
```

之后：

```python
if is_string_list(values):
    ...
```

检查器可以把 `values` 缩窄为 `list[str]`。

---

# 87. Annotated

```python
from typing import Annotated

UserId = Annotated[
    str,
    "user identifier",
]
```

静态类型仍然是 `str`，但可以附带 Metadata。

---

# 88. FastAPI 为什么大量使用 Annotated

例如：

```python
user_id: Annotated[
    str,
    Path(min_length=1),
]
```

其中：

```text
str
=
类型

Path(...)
=
框架元数据
```

---

# 89. Java Annotation 对照

Java：

```java
@NotNull
@Size(min = 1)
String name
```

Python `Annotated` 可以理解成：

```text
Type + Metadata
```

以后 FastAPI / Pydantic 会大量遇到。

---

# 90. Protocol 也能定义属性

```python
class Message(Protocol):
    message_id: str
    payload: bytes
```

任何对象只要拥有这些属性，就可以静态满足这个 Protocol。

---

# 91. Property Protocol

```python
class LockHandle(Protocol):

    @property
    def acquired(self) -> bool:
        ...

    def release(self) -> None:
        ...
```

这很适合组件 API。

---

# 92. Callable Protocol

简单 callable：

```python
Callable[[Message], Result]
```

如果 callable 还需要属性：

```python
class Handler(Protocol):

    name: str

    def __call__(
        self,
        message: Message,
    ) -> Result:
        ...
```

表达力更强。

---

# 93. `__call__`

```python
class Handler:

    def __call__(
        self,
        message: Message,
    ) -> Result:
        ...
```

于是对象可以：

```python
handler(message)
```

像函数一样调用。

适合：

```text
Strategy
Pipeline Step
Middleware
Callback
Handler
```

---

# 94. ParamSpec

Decorator typing 的核心能力之一。

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def traced(
    func: Callable[P, R],
) -> Callable[P, R]:
    ...
```

P 表示：

> 原函数完整参数列表。

R 表示：

> 返回类型。

---

# 95. ParamSpec 与 Retry Decorator

```python
@retry
def load_order(
    order_id: str,
    timeout: float,
) -> Order:
    ...
```

理想情况下，decorator 之后仍保持：

```text
(str, float) -> Order
```

而不是退化为：

```text
(*args, **kwargs) -> Any
```

这就是 ParamSpec 的价值。

---

# 96. Java 为什么不太需要 ParamSpec 这种东西

Java Annotation：

```java
@Retry
```

通常不会改变 Java 编译时方法签名。

Python decorator 会真正替换函数，因此 decorator typing 是很重要的工程问题。

---

# 97. Never

```python
from typing import Never


def fail(message: str) -> Never:
    raise RuntimeError(message)
```

表示：

> 这个函数不会正常返回。

---

# 98. assert_never

```python
from typing import assert_never


def handle(status: Status) -> str:
    match status:
        case Status.SUCCESS:
            return "success"
        case Status.FAILED:
            return "failed"
        case _:
            assert_never(status)
```

可以帮助发现状态分支没有穷尽。

---

# 99. 状态机中的价值

对于：

```text
LockStatus
MessageStatus
ConsumeStatus
TransactionStatus
```

可以配合：

```text
Enum
+
match
+
assert_never
```

增强穷尽检查。

---

# 100. Python 类型系统不只描述 class

它还能直接描述：

```text
值
Literal

联合类型
Union

函数
Callable

结构接口
Protocol

dict schema
TypedDict

类型关系
Generic

函数参数列表
ParamSpec

领域语义
NewType
```

这也是 Python typing 表达力很强的原因。

---

# 101. Type Hint 与 Runtime Validation 必须分开

```python
def execute(
    timeout: int,
) -> None:
    ...
```

不会自动阻止：

```python
execute("abc")
```

如果数据来自：

```text
HTTP
Config
MQ
Environment
JSON
LLM
```

必须额外做 Runtime Validation。

---

# 102. Java 对照 Runtime Validation

Java：

```text
Static Type
+
Bean Validation
```

例如：

```java
@NotNull
@Min(1)
Integer timeout;
```

Python：

```text
Type Hint
+
Pydantic / Explicit Validation
```

两者是两层职责。

---

# 103. 外部边界不要只相信 Type Hint

HTTP JSON：

```json
{
  "amount": "abc"
}
```

即使代码写：

```python
amount: int
```

也不能认为输入自动安全。

还需要：

```text
Parsing
Validation
Conversion
```

---

# 104. Python 三层类型模型

```text
第一层
Runtime Object Model
↓
对象如何存在和运行

第二层
Static Type System
↓
代码边界如何约束

第三层
Runtime Validation
↓
外部数据是否可信
```

---

# 105. Public API 应完整 typing

例如：

```python
def try_lock(
    key: str,
    options: LockOptions,
) -> LockResult:
    ...
```

类型签名本身就是 API 文档。

---

# 106. SPI / Port 优先 Protocol

例如：

```python
class LockProvider(Protocol):
    ...
```

这种能力契约非常适合 Protocol。

---

# 107. Value Object

推荐：

```text
dataclass
+
明确字段类型
+
必要时 frozen=True
```

例如 `RetryOptions`、`LockOptions`。

---

# 108. Runtime State

可以 mutable：

```python
@dataclass
class LockRuntimeState:
    lost: bool = False
    released: bool = False
```

但字段类型依然应该明确。

---

# 109. Callback

不推荐：

```python
callback: Any
```

推荐：

```python
callback: Callable[[], T]
```

这样 Template 才能保留业务返回类型。

---

# 110. Collection API

优先考虑：

```text
Iterable
Sequence
Mapping
```

而不是默认全部：

```text
list
dict
```

---

# 111. Optional 是 API 语义

```python
def find_user(
    user_id: UserId,
) -> User | None:
    ...
```

表示：

> 找不到是正常结果。

而：

```python
def get_required_user(
    user_id: UserId,
) -> User:
    ...
```

表示：

> 找不到应该抛异常。

---

# 112. 不要 Optional 泛滥

如果：

```python
def generate_id() -> str | None:
```

但业务定义是：

> 正常调用必须产生 ID，否则就是错误。

那就应该：

```python
def generate_id() -> str:
    ...
```

失败时抛异常。

---

# 113. Protocol 应该尽量小

不要一个巨大接口：

```text
MessageProvider
  send
  subscribe
  close
  metrics
  health
  admin
  ...
```

可以拆：

```python
class MessageSender(Protocol):
    ...


class MessageSubscriber(Protocol):
    ...
```

这与 Interface Segregation 很契合。

---

# 114. Structural Typing 天然支持接口拆分

同一个：

```python
class KafkaProvider:
    ...
```

只要同时具有 `send()` 和 `subscribe()`，就可以自然满足多个 Protocol。

不需要显式：

```text
implements A, B
```

---

# 115. Type Alias 简化复杂 Callable

例如：

```python
type MessageHandler = Callable[
    [MessageEnvelope, ConsumeContext],
    Awaitable[ConsumeResult],
]
```

然后：

```python
def subscribe(
    handler: MessageHandler,
) -> None:
    ...
```

签名可读性明显更好。

---

# 116. Java FunctionalInterface 对照

Java：

```java
@FunctionalInterface
interface MessageHandler {

    ConsumeResult handle(
        MessageEnvelope message,
        ConsumeContext context
    );
}
```

Python：

```python
type MessageHandler = Callable[
    [MessageEnvelope, ConsumeContext],
    ConsumeResult,
]
```

如果只是纯 callable，通常就够了。

---

# 117. Callable 不够时使用 Protocol

如果 Handler 还需要：

```text
name
priority
supports()
close()
```

则可以：

```python
class MessageHandler(Protocol):

    @property
    def name(self) -> str:
        ...

    def __call__(
        self,
        message: MessageEnvelope,
    ) -> ConsumeResult:
        ...
```

---

# 118. RetryTemplate 完整例子

Java：

```java
public class RetryTemplate {

    public <T> T execute(Supplier<T> action) {
        ...
    }
}
```

Python：

```python
from collections.abc import Callable


class RetryTemplate:

    def execute[T](
        self,
        action: Callable[[], T],
    ) -> T:
        ...
```

这类 Generic + Callable 是非常核心的生产模式。

---

# 119. TransactionTemplate

Java：

```java
public <T> T execute(
    TransactionCallback<T> callback
) {
}
```

Python：

```python
def execute[T](
    self,
    callback: Callable[[], T],
) -> T:
    ...
```

---

# 120. DistributedLockClient

```python
class DistributedLockClient:

    def execute[T](
        self,
        key: str,
        action: Callable[[], T],
        options: LockOptions | None = None,
    ) -> T:
        ...
```

这个签名与 Java `<T> + Supplier<T>` 的技术模板思想几乎完全对应。

---

# 121. LockProvider Protocol

```python
from typing import Protocol


class LockProvider(Protocol):

    def acquire(
        self,
        key: str,
        owner_token: str,
        lease_seconds: float,
    ) -> LockAcquireResult:
        ...

    def release(
        self,
        key: str,
        owner_token: str,
    ) -> LockReleaseResult:
        ...
```

Redis 实现不需要显式继承这个 Protocol。

---

# 122. Ports & Adapters 的 Python 风格

```text
core
 │
 ▼
Protocol Port
 │
 ├── Redis Adapter
 ├── Memory Adapter
 └── Fake Adapter
```

Core 只依赖 Contract。

这是 Python Hexagonal Architecture 很自然的实现方式。

---

# 123. Fake / Stub 很容易

```python
class FakeLockProvider:

    def acquire(...) -> LockAcquireResult:
        return LockAcquireResult.acquired()

    def release(...) -> LockReleaseResult:
        return LockReleaseResult.success()
```

它只要结构满足，就自然符合 `LockProvider`。

---

# 124. Python 测试替身为什么容易

因为：

```text
Structural Typing
+
Duck Typing
+
First-class Function
```

Fake、Stub、Callback 都非常轻。

---

# 125. Strict Typing 不是越多越好

看到：

```python
class AbstractProvider[
    TRequest,
    TResponse,
    TContext,
    TOptions,
    TException,
]:
    ...
```

要警惕过度抽象。

Type System 的目标是降低理解成本，而不是增加抽象层数。

---

# 126. 什么时候值得 Generic

典型适合：

```text
Container[T]
Result[T]
Page[T]
Repository[T]
Cache[K,V]
Serializer[T]
Template.execute[T]()
```

不适合：

> 没有真实类型关系，只为了让代码看起来高级。

---

# 127. Python Typing 原则一

> 能用具体类型，就不要 Any。

例如：

```python
options: RetryOptions
```

优于：

```python
options: dict[str, Any]
```

---

# 128. 原则二

> 只读 Collection 优先抽象接口。

例如：

```python
Sequence[Task]
Mapping[str, str]
Iterable[Event]
```

---

# 129. 原则三

> SPI / Capability 优先 Protocol。

---

# 130. 原则四

> 共享实现才考虑 ABC。

---

# 131. 原则五

> Generic 用于保持类型关系，不用于炫技。

---

# 132. 原则六

> Optional 表示正常缺失，不表示错误兜底。

---

# 133. 原则七

> Type Hint 不是 Runtime Validation。

---

# 134. 原则八

> 外部输入必须 Runtime Validation。

包括：

```text
HTTP
MQ
Config
Environment
LLM Output
Database Raw Data
```

---

# 135. 原则九

> Any 应该停留在边界，并尽快转成明确类型。

例如：

```python
raw: Any = sdk.call()
```

进入系统后尽快：

```text
parse
validate
convert
```

变成明确领域对象。

---

# 136. 原则十

> 类型签名本身就是 API 文档。

例如：

```python
def try_lock(
    key: str,
    options: LockOptions,
) -> LockResult:
    ...
```

调用者不看实现就知道输入和输出边界。

---

# 137. Python 与 Java 类型哲学差异

Java：

```text
Nominal Typing

你是谁？
你显式 implements 了谁？
```

Python Protocol：

```text
Structural Typing

你能做什么？
你的结构是否符合？
```

---

# 138. Programming to Interface vs Capability

Java 常说：

```text
Programming to Interface
```

Python 可以进一步理解为：

```text
Programming to Capability
```

只要对象具有需要的能力，就可以被使用。

---

# 139. 阶段 3 类型体系图

```text
                    Python Type System
                           │
            ┌──────────────┼───────────────┐
            │              │               │
          Value         Structure       Relationship
            │              │               │
         Literal        Protocol         Generic
         Union          TypedDict        TypeVar
         None           Callable         ParamSpec
         NewType        ABC
                           │
                           ▼
                    Component Contract
                           │
             ┌─────────────┼─────────────┐
             │             │             │
            API           SPI          Callback
```

---

# 140. Java → Python 类型系统速查表

| Java | Python |
|---|---|
| `String` | `str` |
| `Integer / Long` | `int` |
| `List<T>` | `list[T]` |
| `Set<T>` | `set[T]` |
| `Map<K,V>` | `dict[K,V]` |
| `Collection<T>` | `Collection[T]` |
| `Iterable<T>` | `Iterable[T]` |
| Read-only List 思路 | `Sequence[T]` |
| Read-only Map 思路 | `Mapping[K,V]` |
| nullable `T` | `T | None` |
| Java Optional | `T | None` |
| `Object` | `object` |
| 无安全对应 | `Any` |
| `<T>` | `[T]` |
| `<T extends Base>` | `[T: Base]` |
| `Supplier<T>` | `Callable[[], T]` |
| `Consumer<T>` | `Callable[[T], None]` |
| `Function<A,B>` | `Callable[[A], B]` |
| `Predicate<T>` | `Callable[[T], bool]` |
| `interface` | `Protocol / ABC` |
| `abstract class` | `ABC` |
| enum | `Enum / StrEnum` |
| static field | `ClassVar` |
| final | `Final` |
| overload | `@overload` |
| Strong ID Wrapper | `NewType` |
| Map DTO | `TypedDict` |
| Annotation Metadata | `Annotated` |
| Decorator parameter typing | `ParamSpec` |

---

# 141. `iron-foundation/id` 示例

```python
from typing import Protocol


class IdGenerator(Protocol):

    def generate(self) -> str:
        ...
```

UUID：

```python
class UuidGenerator:

    def generate(self) -> str:
        ...
```

Snowflake：

```python
class SnowflakeGenerator:

    def generate(self) -> str:
        ...
```

业务：

```python
class OrderService:

    def __init__(
        self,
        id_generator: IdGenerator,
    ) -> None:
        self._id_generator = id_generator
```

这就是：

```text
Dependency Inversion
+
Protocol
```

---

# 142. 泛型 IdGenerator 是否需要

可以设计：

```python
class IdGenerator[T](Protocol):

    def generate(self) -> T:
        ...
```

支持：

```text
IdGenerator[str]
IdGenerator[int]
```

但如果全系统 ID 已统一为 `str`，那不泛型化反而更简单。

---

# 143. 抽象成本控制

如果整个系统约定：

```text
ID 对外统一 str
```

那么：

```python
class IdGenerator(Protocol):

    def generate(self) -> str:
        ...
```

可能比泛型版本更好。

原则：

> 不为了理论上的未来灵活性提前泛型化所有东西。

---

# 144. 推荐的 `iron-components-python` Typing 风格

```text
Public API
→ Strong Typing

SPI
→ Protocol

Options
→ Typed Dataclass

Result
→ Dataclass / Enum

Callback
→ Generic Callable

Collection
→ Sequence / Mapping / Iterable

Internal Local
→ Type Inference

Any
→ 尽量边界化

Cast
→ 尽量少
```

---

# 145. 不需要给所有局部变量手写类型

不必：

```python
name: str = "iron"
count: int = 1
enabled: bool = True
```

通常：

```python
name = "iron"
count = 1
enabled = True
```

就够了。

类型设计真正应该投入在 API、SPI、Template、Callback、DTO、State、Configuration。

---

# 146. 常见错误一：Any 泛滥

```python
def execute(
    data: Any,
    options: Any,
) -> Any:
    ...
```

看似有 Type Hint，实际几乎关闭静态检查。

---

# 147. 常见错误二：Optional 泛滥

```python
def create_order() -> Order | None:
```

如果失败其实属于 Exception，就不应该把 None 作为正常返回值。

---

# 148. 常见错误三：全部使用具体 Collection

```python
def execute(
    events: list[Event],
    headers: dict[str, str],
) -> None:
    ...
```

如果只读，可以设计：

```python
def execute(
    events: Sequence[Event],
    headers: Mapping[str, str],
) -> None:
    ...
```

---

# 149. 常见错误四：ABC 泛滥

不要把 Java 所有 `interface` 机械翻译成 Python `ABC`。

SPI / Port 应优先考虑 Protocol。

---

# 150. 常见错误五：Protocol 泛滥

反过来也不能什么都是 Protocol。

如果需要：

```text
Shared Implementation
Shared State
Template Method
Lifecycle
```

ABC 或普通 Base Class 更合理。

---

# 151. 常见错误六：Generic 泛滥

```python
class Service[T1, T2, T3, T4]:
    ...
```

必须问：

> 这些 Type Parameter 是否真的维持了调用者关心的类型关系？

没有就删。

---

# 152. 常见错误七：cast 当类型转换

```python
cast(int, value)
```

不会把对象转换成 int。

真正转换是：

```python
int(value)
```

---

# 153. 常见错误八：Type Hint 当 Runtime Validation

```python
age: int
```

不代表外部传入 `"hello"` 会自动被 Python 拒绝。

---

# 154. 常见错误九：TypedDict 当 Domain Entity

复杂稳定领域对象：

```text
Order
User
MessageEnvelope
LockResult
```

不应长期全部用 TypedDict。

优先考虑 dataclass、Pydantic Model 或真正领域类。

---

# 155. 常见错误十：忽略 None

```python
user = find_user(...)
user.name
```

如果：

```python
find_user() -> User | None
```

类型检查器提醒你处理 None，正是它的价值。

---

# 156. 阶段 3 十大结论

1. Type Hint 是静态契约，不是 Runtime 强制。
2. `T | None` 表示 None 是合法结果。
3. Python `Optional[T]` 不是 Java Optional 容器。
4. `Any` 与 `object` 完全不同。
5. Generic 用来保留类型关系。
6. Protocol 是 Python SPI / Port 的关键能力。
7. ABC 适合共享实现和继承体系。
8. Callable 让 Template / Callback 类型安全。
9. API 参数优先声明最小能力。
10. Runtime Validation 与 Type Hint 必须分层。

---

# 157. 阶段 1 ~ 阶段 3 串联

```text
阶段 1
Python 怎么写
↓
变量 / if / for / list / dict / function

阶段 2
Python 为什么这样运行
↓
Name Binding
Object
Mutable / Immutable
Identity / Equality
Copy

阶段 3
大型项目如何建立类型边界
↓
Type Hint
Union
Generic
Callable
Protocol
ABC
TypedDict
NewType
```

---

# 158. Java → Python 类型设计判断流程

```text
只是描述能力？
↓
Protocol

需要共享实现？
↓
ABC / Base Class

只是回调？
↓
Callable

需要保持输入输出类型关系？
↓
Generic

简单数据对象？
↓
dataclass

JSON-like dict？
↓
TypedDict

底层相同但领域语义不同？
↓
NewType

少量固定值？
↓
Literal / Enum
```

---

# 159. 阶段 3 自测

1. Python Type Hint 为什么不等于 Java Compile Type？
2. `User | None` 和 Java `Optional<User>` 有什么区别？
3. Python `Optional[User]` 实际等价什么？
4. `Any` 和 `object` 有什么区别？
5. 为什么组件代码应减少 Any？
6. `list[str]` 与 `Sequence[str]` 有什么区别？
7. `dict[str,str]` 与 `Mapping[str,str]` 有什么区别？
8. Generic 的核心目的是什么？
9. 为什么 `first[T](list[T]) -> T` 比 `object -> object` 更有价值？
10. `Callable[[], T]` 对应 Java 什么？
11. `Callable[[T], None]` 对应 Java 什么？
12. Protocol 和 Java interface 最大区别是什么？
13. Structural Typing 是什么？
14. Protocol 与 ABC 怎么选择？
15. 为什么 SPI 很适合 Protocol？
16. `@runtime_checkable` 是否等价 Java interface Runtime Check？
17. NewType 与 Type Alias 有什么区别？
18. Literal 与 Enum 怎么选？
19. TypedDict 与 dataclass 有什么区别？
20. Final 为什么不等于 Java final？
21. Python `@overload` 为什么不是 Runtime overload？
22. cast 为什么不是 Runtime conversion？
23. isinstance 为什么可以帮助 Type Narrowing？
24. Annotated 为什么 FastAPI 常用？
25. ParamSpec 为什么对 Decorator 重要？
26. `list[Dog]` 为什么不能直接当 `list[Animal]`？
27. Sequence 为什么通常更灵活？
28. Type Hint 与 Runtime Validation 有什么区别？
29. 为什么 Options 不建议 `dict[str, Any]`？
30. 为什么 Python typing 不是写得越多越好？

---

# 160. 最值得记住的模式一：Protocol

```python
class LockProvider(Protocol):

    def acquire(
        self,
        key: str,
    ) -> LockResult:
        ...
```

可以理解：

```text
Java interface
+
Structural Typing
```

---

# 161. 最值得记住的模式二：Generic Template

```python
def execute[T](
    action: Callable[[], T],
) -> T:
    ...
```

对应 Java：

```java
<T> T execute(Supplier<T> action)
```

这是 Retry / Transaction / Lock Template 都会用到的核心模式。

---

# 162. 最值得记住的模式三：Optional API

```python
def find_user(
    user_id: UserId,
) -> User | None:
    ...
```

类型签名直接表达：

> 找不到是正常结果之一。

---

# 163. 阶段 3 最终总结

阶段 3 真正需要掌握的，不是 `typing` 模块到底有多少类，而是下面这组工程模型：

```text
Python Runtime
是动态的

Python API
仍然可以有强契约

Python SPI
可以通过 Protocol 优雅表达

Python Template
可以通过 Generic + Callable 保留完整类型

Python 外部输入
必须 Runtime Validation
```

这才是生产级 Python 类型系统真正的价值。

下一阶段进入：

> **阶段 4 —— Pythonic 设计：Module、Function、Dataclass、Protocol、ABC、Builder、Factory、Strategy、Template、Context Manager，以及 Java 设计模式在 Python 中如何简化。**
