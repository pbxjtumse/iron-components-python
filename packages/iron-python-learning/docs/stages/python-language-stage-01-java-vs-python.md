# Python 语言基础学习笔记：阶段 1 —— 核心语法（Java → Python 对照版）

> 学习目标：以 Java 开发经验为基础，快速建立 Python 语言心智模型。  
> 适用对象：熟悉 Java / Spring / Maven，希望快速转向 Python 工程开发、技术组件与 AI 开发。  
> Python 基线：Python 3.12  
> 学习原则：**不是重新学习编程，而是建立 Java → Python 的映射关系。**

---

# 1. 阶段 1 学习目标

完成本阶段后，需要能够：

- 阅读常见 Python 代码；
- 使用变量、条件、循环、函数与常见数据结构；
- 理解 Python 与 Java 在类型系统上的核心差异；
- 掌握 Python 的字符串、集合、参数与模块基础；
- 初步写出符合 Python 风格的代码；
- 避免把 Python 写成“没有大括号的 Java”。

本阶段暂时不深入：

- Python 对象模型；
- 深浅拷贝；
- 装饰器实现原理；
- Protocol / ABC；
- Generator；
- Context Manager；
- asyncio；
- pytest；
- uv workspace。

这些会在后续阶段逐步展开。

---

# 2. Java 与 Python 总体对照

| 能力 | Java | Python | 核心理解 |
|---|---|---|---|
| 源文件 | `.java` | `.py` | Python 一个 `.py` 文件本身就是 Module |
| 包 | `package` | package/module | Python 包结构更轻 |
| 变量声明 | `String name` | `name = "iron"` | Python 变量名不绑定固定类型 |
| 类型 | 静态类型 | 动态类型 + 类型提示 | 对象有类型，变量名不固定类型 |
| 方法 | method | function / method | Python 更强调独立 function |
| 类 | `class` | `class` | 语义类似，但 Python 不强调 Class First |
| 空值 | `null` | `None` | 判断使用 `is None` |
| 布尔 | `true/false` | `True/False` | 首字母大写 |
| List | `List<T>` | `list[T]` | Python 内置 |
| Map | `Map<K,V>` | `dict[K,V]` | Python 最常用结构之一 |
| Set | `Set<T>` | `set[T]` | Python 内置 |
| 元组 | 无完全对应 | `tuple` | 轻量不可变组合 |
| if | `if (...) {}` | `if ...:` | Python 使用缩进表达代码块 |
| for | enhanced for | `for x in items:` | 更简洁 |
| switch | `switch` | `match` | Python 3.10+ 支持结构模式匹配 |
| 异常 | `throw/catch` | `raise/except` | Python 没 checked exception |
| 字符串格式化 | `String.format` / formatted | f-string | Python 推荐 f-string |
| main | `public static void main` | `if __name__ == "__main__"` | Python 文件可执行也可 import |
| Maven POM | `pom.xml` | `pyproject.toml` | Python 现代项目统一入口 |
| Maven/Gradle | Maven / Gradle | uv | uv 还管理虚拟环境与 Python 版本 |

---

# 3. 变量与类型

## Java

```java
String name = "iron";
int count = 10;
double price = 19.9;
boolean enabled = true;
```

## Python

```python
name = "iron"
count = 10
price = 19.9
enabled = True
```

| Java | Python |
|---|---|
| `String` | `str` |
| `int` | `int` |
| `long` | `int` |
| `double` | `float` |
| `boolean` | `bool` |
| `null` | `None` |

Python 的 `int` 不像 Java 区分 `byte / short / int / long`，整数可以自动扩展精度。

---

# 4. Python 类型系统与 Java 的最大差异

## Java

```java
String value = "iron";

// 编译错误
value = 100;
```

## Python

```python
value = "iron"
value = 100
```

这是合法的。

核心理解：

> Python 的对象有类型，但变量名本身不固定类型。

```text
Java

String name
       │
       ▼
     "iron"
```

```text
Python

name ───────> "iron"

之后

name ───────> 100
```

---

# 5. Type Hint 类型提示

## Java

```java
int add(int a, int b) {
    return a + b;
}
```

## Python

```python
def add(a: int, b: int) -> int:
    return a + b
```

Python 类型提示主要服务于：

- IDE；
- Pyright；
- mypy；
- API 契约；
- 阅读代码；
- 重构。

它默认不会像 Java 编译器一样阻止：

```python
add("1", "2")
```

因此生产 Python 通常采用：

```text
Python Runtime
+
Type Hint
+
Static Checker
+
pytest
```

---

# 6. None 与 null

| Java | Python |
|---|---|
| `null` | `None` |
| `value == null` | `value is None` |
| `value != null` | `value is not None` |

推荐：

```python
if value is None:
    ...
```

不推荐：

```python
if value == None:
    ...
```

---

# 7. String / str

## Java

```java
String name = " iron ";

name.trim();
name.toLowerCase();
name.toUpperCase();
name.startsWith("ir");
name.endsWith("on");
name.replace("iron", "python");
```

## Python

```python
name = " iron "

name.strip()
name.lower()
name.upper()
name.startswith("ir")
name.endswith("on")
name.replace("iron", "python")
```

| Java | Python |
|---|---|
| `trim()` | `strip()` |
| `toLowerCase()` | `lower()` |
| `toUpperCase()` | `upper()` |
| `startsWith()` | `startswith()` |
| `endsWith()` | `endswith()` |
| `replace()` | `replace()` |
| `split()` | `split()` |
| `String.join()` | `separator.join()` |
| `length()` | `len()` |

---

# 8. 字符串格式化

## Java

```java
String result = "name=%s, age=%d".formatted(name, age);
```

## Python

```python
result = f"name={name}, age={age}"
```

推荐优先使用 f-string：

```python
component = "iron-foundation"
version = "0.1.0"

message = f"{component} version={version}"
```

---

# 9. list 与 Java List

## Java

```java
List<String> names = new ArrayList<>();

names.add("A");
names.add("B");
```

## Python

```python
names = ["A", "B"]

names.append("C")
```

| Java | Python |
|---|---|
| `list.add(x)` | `items.append(x)` |
| `list.get(0)` | `items[0]` |
| `list.size()` | `len(items)` |
| `list.remove(x)` | `items.remove(x)` |
| `list.contains(x)` | `x in items` |
| `list.isEmpty()` | `not items` |

---

# 10. list 下标与切片

```python
items = ["a", "b", "c", "d"]
```

| Python | 结果 | Java 类比 |
|---|---|---|
| `items[0]` | `"a"` | `items.get(0)` |
| `items[-1]` | `"d"` | `items.get(items.size() - 1)` |
| `items[0:2]` | `["a", "b"]` | `subList(0, 2)` |
| `items[:2]` | `["a", "b"]` | 从头取到 2 |
| `items[2:]` | `["c", "d"]` | 从 2 取到末尾 |
| `items[-2:]` | `["c", "d"]` | 取最后两个 |

切片遵循：

```text
[start, end)
```

---

# 11. dict 与 Java Map

## Java

```java
Map<String, Object> data = new HashMap<>();

data.put("name", "iron");
data.put("version", 1);
```

## Python

```python
data = {
    "name": "iron",
    "version": 1,
}
```

访问：

```python
data["name"]
```

安全读取：

```python
data.get("name")
```

带默认值：

```python
timeout = data.get("timeout", 30)
```

Java 对应：

```java
map.getOrDefault("timeout", 30);
```

### 重要区别

```python
data["missing"]
```

不存在时抛：

```text
KeyError
```

而：

```python
data.get("missing")
```

返回：

```python
None
```

---

# 12. tuple

Python：

```python
point = (10, 20)
```

拆包：

```python
x, y = point
```

函数：

```python
def get_user() -> tuple[str, int]:
    return "iron", 1
```

调用：

```python
name, level = get_user()
```

Java 没有完全等价的语言级 tuple，通常会使用：

```java
record UserInfo(String name, int level) {}
```

---

# 13. set

## Java

```java
Set<String> ids = new HashSet<>();
```

## Python

```python
ids = {"a", "b", "c"}
```

添加：

```python
ids.add("d")
```

集合运算：

| 操作 | Python |
|---|---|
| 并集 | `a \| b` |
| 交集 | `a & b` |
| 差集 | `a - b` |
| 是否包含 | `x in a` |

---

# 14. if / elif / else

## Java

```java
if (score >= 90) {
    ...
} else if (score >= 80) {
    ...
} else {
    ...
}
```

## Python

```python
if score >= 90:
    ...
elif score >= 80:
    ...
else:
    ...
```

Python：

- 没有 `{}`；
- 使用 `:`；
- 使用缩进划分代码块；
- 推荐 4 个空格。

---

# 15. Truthy / Falsy

Java 经常：

```java
if (items != null && !items.isEmpty()) {
}
```

Python：

```python
if items:
    ...
```

以下值通常判断为 False：

```python
None
False
0
0.0
""
[]
{}
set()
```

但要注意：

```python
if not value:
```

不等于：

```python
if value is None:
```

因为 `0`、`""`、`[]` 等也属于 False。

---

# 16. for

## Java

```java
for (String name : names) {
    System.out.println(name);
}
```

## Python

```python
for name in names:
    print(name)
```

---

# 17. enumerate

Java：

```java
for (int i = 0; i < names.size(); i++) {
    String name = names.get(i);
}
```

Python 推荐：

```python
for index, name in enumerate(names):
    print(index, name)
```

通常不要机械写：

```python
for i in range(len(names)):
    ...
```

除非真的需要按下标操作。

---

# 18. range

Java：

```java
for (int i = 0; i < 5; i++) {
}
```

Python：

```python
for i in range(5):
    ...
```

结果：

```text
0 1 2 3 4
```

还可以：

```python
range(1, 10)
range(1, 10, 2)
```

对应：

```text
range(start, end, step)
```

---

# 19. while / break / continue

| Java | Python |
|---|---|
| `while (running) {}` | `while running:` |
| `break;` | `break` |
| `continue;` | `continue` |

Python 还有：

```python
pass
```

例如：

```python
if enabled:
    pass
```

表示语法上保留代码块，但暂时什么都不做。

---

# 20. 函数

## Java

```java
String hello(String name) {
    return "hello " + name;
}
```

## Python

```python
def hello(name: str) -> str:
    return f"hello {name}"
```

| Java | Python |
|---|---|
| 方法通常属于 class | function 可以独立存在 |
| 返回类型写前面 | 返回类型写在 `->` 后 |
| 参数类型强制 | Type Hint 可选 |
| `{}` | `:` + 缩进 |

---

# 21. 函数是一等对象

Java：

```java
Function<String, String> fn = this::hello;
```

Python：

```python
fn = hello
result = fn("iron")
```

Python 中函数本身就是对象。

这是后续理解这些能力的基础：

```text
Decorator
Callback
Dependency Injection
FastAPI
LangChain
LangGraph
```

---

# 22. 默认参数

Java 往往通过方法重载：

```java
connect("localhost");
connect("localhost", 6379);
```

Python：

```python
def connect(
    host: str,
    port: int = 6379,
    timeout: float = 3.0,
) -> None:
    ...
```

调用：

```python
connect("localhost")
```

---

# 23. Keyword Argument

Python：

```python
connect(
    host="localhost",
    timeout=5.0,
)
```

Java 没有真正原生的 Named Argument。

因此 Python 很多场景不需要复杂 Builder。

---

# 24. Builder：Java 与 Python

## Java

```java
LockOptions.builder()
    .leaseTime(30)
    .waitTime(5)
    .autoRenew(true)
    .build();
```

## Python

```python
LockOptions(
    lease_time=30,
    wait_time=5,
    auto_renew=True,
)
```

核心原因：

> Python 的 Keyword Argument 本身已经提供很好的调用可读性。

---

# 25. *args

Java：

```java
void execute(Object... args) {
}
```

Python：

```python
def execute(*args):
    ...
```

调用：

```python
execute(1, 2, 3)
```

内部：

```python
args
```

是一个 `tuple`。

---

# 26. **kwargs

Python：

```python
def execute(**kwargs):
    ...
```

调用：

```python
execute(
    timeout=30,
    retry=3,
)
```

内部：

```python
kwargs
```

是一个 `dict`。

以后在框架、SDK 和 AI 开发中非常常见。

---

# 27. lambda

Java：

```java
x -> x * 2
```

Python：

```python
lambda x: x * 2
```

Python lambda 只适合简单表达式。

复杂逻辑：

```python
def handler():
    ...
```

比复杂 lambda 更清晰。

---

# 28. List Comprehension

Java Stream：

```java
users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .toList();
```

Python：

```python
names = [
    user.name
    for user in users
    if user.active
]
```

简单例子：

```python
squares = [x * x for x in range(10)]
```

建议：

> 简单逻辑使用推导式；复杂业务逻辑拆开写。

---

# 29. in / not in

Java：

```java
items.contains("iron");
map.containsKey("iron");
```

Python：

```python
"iron" in items
"iron" in data
```

否定：

```python
"iron" not in items
```

---

# 30. and / or / not

| Java | Python |
|---|---|
| `&&` | `and` |
| `\|\|` | `or` |
| `!` | `not` |

例如：

```python
if enabled and count > 0:
    ...
```

---

# 31. == 与 is

Python：

```python
a == b
```

表示：

> 值是否相等。

Python：

```python
a is b
```

表示：

> 是否是同一个对象。

阶段 1 最常用：

```python
value is None
```

对象 identity 的细节留到阶段 2。

---

# 32. 异常

## Java

```java
throw new IllegalArgumentException("invalid value");
```

## Python

```python
raise ValueError("invalid value")
```

---

# 33. try / except

## Java

```java
try {
    execute();
} catch (IllegalArgumentException e) {
    log.error("error", e);
} finally {
    cleanup();
}
```

## Python

```python
try:
    execute()
except ValueError as exc:
    ...
finally:
    cleanup()
```

| Java | Python |
|---|---|
| `throw` | `raise` |
| `catch` | `except` |
| `finally` | `finally` |
| `Exception e` | `as exc` |

---

# 34. Python 没有 Checked Exception

Java：

```java
void read() throws IOException
```

Python 没有同等机制：

```python
def read() -> str:
    raise OSError("read failed")
```

调用者不会被语言强制捕获。

因此 Python API 更依赖：

- 异常设计；
- Docstring；
- 测试；
- 类型提示；
- 文档约定。

---

# 35. Module：Java 开发者必须转换的概念

目录：

```text
iron_foundation/
└── time/
    └── clock.py
```

`clock.py`：

```python
def now_millis() -> int:
    ...
```

调用：

```python
from iron_foundation.time.clock import now_millis
```

Java 粗略类比：

```java
import com.xjtu.iron.foundation.time.ClockUtils;
```

但核心差异是：

> Python 的 `.py` 文件本身就是命名空间，因此不需要为了组织静态函数再套一个 Utils Class。

---

# 36. Java Utils → Python Module Function

## Java

```java
public final class IdUtils {

    public static String uuid() {
        ...
    }
}
```

## 不推荐的 Python 机械翻译

```python
class IdUtils:

    @staticmethod
    def uuid():
        ...
```

## 更自然的 Python

```python
# uuid.py

def uuid4_str() -> str:
    ...
```

调用：

```python
from iron_foundation.id.uuid import uuid4_str
```

这是 Java → Python 设计迁移中非常重要的一点。

---

# 37. import

### 方式一

```python
import datetime

datetime.datetime.now()
```

### 方式二

```python
from datetime import datetime

datetime.now()
```

### 方式三

```python
import datetime as dt

dt.datetime.now()
```

不推荐：

```python
from xxx import *
```

原因：

- 污染命名空间；
- 容易命名冲突；
- 不容易追踪符号来源。

---

# 38. __name__ 与 main

Python：

```python
def main() -> None:
    print("hello")


if __name__ == "__main__":
    main()
```

粗略类比 Java：

```java
public static void main(String[] args) {
}
```

但 Python 文件同时可以：

```text
直接运行
+
被其他 Module import
```

---

# 39. 注释与 Docstring

Java：

```java
// comment

/**
 * Generate ID.
 */
```

Python：

```python
# comment


def generate_id() -> str:
    """Generate a new ID."""
```

`"""..."""` 更准确地说是字符串字面量；放在模块、类、函数开头时可作为 Docstring。

---

# 40. Python 命名规范

| 类型 | Java | Python |
|---|---|---|
| Class | `DistributedLockClient` | `DistributedLockClient` |
| Method | `generateOwnerToken` | `generate_owner_token` |
| Variable | `lockOptions` | `lock_options` |
| Constant | `MAX_RETRY_COUNT` | `MAX_RETRY_COUNT` |
| File | `LockOptions.java` | `lock_options.py` |
| Package | `distributedlock` | `distributed_lock` |

Python 主流约定：

```text
Class       PascalCase
Function    snake_case
Variable    snake_case
Constant    UPPER_CASE
Module      snake_case.py
```

---

# 41. 分号与大括号

Java：

```java
if (enabled) {
    execute();
}
```

Python：

```python
if enabled:
    execute()
```

Python 不需要：

```text
;
{
}
```

推荐统一使用：

```text
4 spaces
```

进行缩进。

---

# 42. 为什么 Python 通常比 Java 短

Java：

```java
public final class TimeUtils {

    private TimeUtils() {
    }

    public static long currentTimeMillis() {
        return System.currentTimeMillis();
    }
}
```

Python：

```python
def current_time_millis() -> int:
    ...
```

并不是 Python “不讲设计”。

而是 Python 将：

```text
Module
Function
Keyword Argument
Decorator
Context Manager
```

都做成语言级能力，因此很多 Java 中为弥补语言表达能力而产生的样板结构不再需要。

---

# 43. Java 开发者最容易写出的“Java 风格 Python”

容易写成：

```text
AbstractXxxFactory
DefaultXxxFactoryImpl
XxxManager
XxxService
XxxUtils
XxxHelper
XxxContext
XxxHolder
```

这些东西不是不能存在。

问题是：

> 不要因为 Java 里习惯这么做，就默认 Python 里也应该这么做。

Python 更常见的思考顺序：

```text
Module
↓
Function
↓
Dataclass
↓
Protocol
↓
Class
```

是否需要 Class，取决于是否真正存在：

```text
State
Behavior
Polymorphism
Lifecycle
```

---

# 44. 阶段 1 总速查表

| Java | Python | 重要度 |
|---|---|---:|
| `String` | `str` | ★★★ |
| `int / long` | `int` | ★★ |
| `double` | `float` | ★★ |
| `boolean` | `bool` | ★★ |
| `null` | `None` | ★★★ |
| `List<T>` | `list[T]` | ★★★ |
| `Map<K,V>` | `dict[K,V]` | ★★★ |
| `Set<T>` | `set[T]` | ★★ |
| record / Pair | `tuple` | ★★ |
| method | `def` | ★★★ |
| enhanced for | `for x in items` | ★★★ |
| index for | `enumerate()` | ★★★ |
| `String.format` | f-string | ★★★ |
| method overload | default / keyword args | ★★★ |
| `Object...` | `*args` | ★★ |
| Named Argument 无 | keyword args / `**kwargs` | ★★★ |
| Stream map/filter | comprehension | ★★★ |
| `throw` | `raise` | ★★★ |
| `catch` | `except` | ★★★ |
| `null == x` | `x is None` | ★★★ |
| `list.contains(x)` | `x in list` | ★★★ |
| `&& / \|\| / !` | `and / or / not` | ★★★ |
| Utils Class | Module Function | ★★★ |
| `pom.xml` | `pyproject.toml` | ★★★ |
| Maven / Gradle | uv | ★★★ |

---

# 45. 一个完整的 Java → Python 小例子

## Java

```java
public Map<String, Object> buildMessage(
        String businessKey,
        Map<String, Object> payload,
        boolean enabled) {

    if (!enabled) {
        return Map.of();
    }

    return Map.of(
        "business_key", businessKey,
        "payload", payload
    );
}
```

## Python

```python
def build_message(
    business_key: str,
    payload: dict[str, object],
    enabled: bool = True,
) -> dict[str, object]:
    if not enabled:
        return {}

    return {
        "business_key": business_key,
        "payload": payload,
    }
```

这个 Python 例子已经包含：

- `def`
- Type Hint
- `dict`
- 默认参数
- Keyword Argument 友好接口
- Truthy/Falsy
- snake_case
- `return`

---

# 46. 阶段 1 最重要的五个结论

## 结论 1：Python 不是没有类型

准确说：

> 对象有类型，变量名不绑定固定类型。

---

## 结论 2：生产 Python 不建议完全动态裸奔

推荐：

```text
Dynamic Runtime
+
Type Hint
+
Static Checker
+
Test
```

---

## 结论 3：Java Utils Class 经常应变成 Python Module Function

Java：

```text
TimeUtils.currentTimeMillis()
```

Python：

```text
clock.current_time_millis()
```

或者：

```python
from iron_foundation.time import current_time_millis
```

---

## 结论 4：Python 不应该坚持 Class First

Java 开发者需要逐渐建立：

```text
Module
↓
Function
↓
Dataclass
↓
Protocol
↓
Class
```

的判断习惯。

---

## 结论 5：Python 真正的生产力在后面的语言能力

除了基础语法，更重要的是：

```text
Object Model
Typing
Dataclass
Protocol
Decorator
Context Manager
Generator
Asyncio
pytest
Packaging
```

---

# 47. 阶段 1 自测

如果下面问题能够直接回答，阶段 1 基本过关：

1. Python 为什么可以让同一个变量名先指向 `str`，后来又指向 `int`？
2. `None` 为什么推荐使用 `is None` 判断？
3. `list[-1]` 是什么意思？
4. `dict["x"]` 与 `dict.get("x")` 有什么区别？
5. `if items:` 会把哪些值视为 False？
6. `enumerate(items)` 解决了 Java 中哪类循环问题？
7. Python 为什么比 Java 更少使用 Builder？
8. `*args` 和 `**kwargs` 分别是什么？
9. Python Module 和 Java Class 的关键区别是什么？
10. 为什么 `TimeUtils` 在 Python 中通常没必要存在？
11. `==` 和 `is` 的初步区别是什么？
12. 为什么生产项目仍然建议使用 Type Hint？

---

# 48. 后续阶段统一学习模板

从阶段 2 开始，统一采用以下结构：

```text
1. 本阶段目标

2. Java → Python 总映射表

3. 每个概念：
   Java 写法
   ↓
   Python 写法
   ↓
   核心差异
   ↓
   生产实践
   ↓
   常见坑

4. iron-components-python 中如何使用

5. 阶段速查表

6. 自测题
```

---

# 49. 后续路线

## 阶段 2：对象模型

重点：

- Object / Reference；
- identity；
- mutable / immutable；
- 参数传递；
- shallow copy / deep copy；
- `==` / `is`；
- hash；
- 可变默认参数；
- Java 引用模型与 Python 的异同。

## 阶段 3：类型系统

重点：

- Type Hint；
- Union；
- Optional；
- Generic；
- TypeVar；
- Protocol；
- ABC；
- Callable；
- Python 3.12 泛型语法。

## 阶段 4：Pythonic 设计

重点：

- Function First；
- Module；
- Dataclass；
- Enum；
- Property；
- Composition；
- Java 设计模式在 Python 中如何简化。

## 阶段 5：工程基础

重点：

- Exception；
- Logging；
- Config；
- Serialization；
- Validation；
- pathlib。

## 阶段 6：高级语言能力

重点：

- Iterator；
- Generator；
- Decorator；
- Closure；
- Context Manager。

## 阶段 7：并发

重点：

- Thread；
- Process；
- GIL；
- asyncio；
- async / await；
- Task；
- Queue。

## 阶段 8：测试与工程化

重点：

- pytest；
- fixture；
- mock；
- coverage；
- ruff；
- pyright；
- uv。

---

# 50. 最终学习目标

目标不是成为：

> 会 Python 语法的 Java 开发者。

而是形成：

```text
Java 工程经验
+
Python 语言习惯
+
Python 工程化
+
AI 技术栈
```

最终能够自然地建设：

```text
iron-components-python
│
├── iron-foundation
├── retry
├── concurrent
├── transaction
├── idempotent
├── message
└── ...
```

并继续向：

```text
FastAPI
LangChain
LangGraph
Agent Runtime
AI Engineering
```

延伸。

---

> 下一篇：**阶段 2 —— Python 对象、引用、可变/不可变与参数传递（Java → Python 对照版）**
