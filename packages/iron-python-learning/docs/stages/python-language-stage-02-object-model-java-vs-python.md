# Python 语言基础学习笔记：阶段 2 —— 对象、引用、可变/不可变、参数传递、`==` / `is`、浅拷贝/深拷贝（Java → Python 对照版）

> 学习目标：基于 Java 对象与引用模型，建立 Python 的 Name Binding / Object Model 心智模型。  
> 适用对象：熟悉 Java，希望准确理解 Python 对象语义、参数传递、共享状态与复制行为的开发者。  
> Python 基线：Python 3.12  
> 核心原则：**不要把 Python 变量理解成“装值的盒子”，而要理解成“名字绑定对象”。**

---

# 1. 阶段 2 学习目标

完成本阶段后，需要能够准确回答：

- Python 变量到底是什么？
- `a = b` 到底有没有复制对象？
- 为什么修改 `list` 会影响另一个变量？
- 为什么修改 `str` 不会？
- Python 函数参数到底是值传递还是引用传递？
- `==` 和 `is` 的区别是什么？
- Python 的 `==` 更像 Java 的 `==` 还是 `.equals()`？
- Python 的 `is` 更像 Java 的什么？
- 什么是 shallow copy？
- 什么是 deep copy？
- 为什么 `def foo(items=[])` 是经典坑？
- 为什么 `tuple` 不可变，但里面的 `list` 还能变化？
- 为什么 `list` 不能作为 `dict` key？
- 为什么组件中的 Options / Config 往往适合设计成 immutable？
- 为什么 API 不应该随便暴露内部 mutable object？

本阶段会成为后续这些能力的基础：

```text
对象模型
↓
typing
↓
dataclass
↓
Protocol
↓
decorator
↓
closure
↓
asyncio
↓
FastAPI / LangGraph State
```

---

# 2. Java 与 Python 对象模型总对照

| 主题 | Java | Python | 核心理解 |
|---|---|---|---|
| 变量 | primitive value / object reference | name binding object | Python 更强调“名字绑定对象” |
| 对象 | `new Xxx()` | 几乎一切都是对象 | `int / str / function / class` 都可视为对象 |
| 引用共享 | 多个变量可引用同一对象 | 多个 name 可绑定同一对象 | 本质非常接近 |
| 重新赋值 | 改变变量保存的值/引用 | rebind name | 不会自动修改原对象 |
| 可变对象 | `ArrayList / HashMap` | `list / dict / set` | 可原地修改 |
| 不可变对象 | `String / Integer` 等 | `int / str / tuple / frozenset` 等 | “修改”通常产生新对象 |
| 对象 identity | 对象 `==` | `is` | 是否同一个对象 |
| 值 equality | `.equals()` | `==` | 内容/值是否相等 |
| 参数传递 | pass-by-value | object sharing / assignment semantics | 调用时参数名绑定到同一对象 |
| 浅拷贝 | copy constructor / clone | `copy.copy()` / `.copy()` | 只复制外层 |
| 深拷贝 | 手工实现居多 | `copy.deepcopy()` | 递归复制对象图 |
| immutable value object | record + final | frozen dataclass 等 | 组件配置常用 |
| Map key | `equals/hashCode` | `__eq__/__hash__` | hash 必须稳定 |

---

# 3. Python 变量：Name Binding

## Java

```java
String name = "iron";
```

Java 中通常理解为：

```text
声明一个 String 类型变量 name，
它保存一个 String 对象的引用。
```

## Python

```python
name = "iron"
```

更准确的理解：

```text
name
 │
 ▼
"iron"
```

也就是：

> 名字 `name` 绑定到了一个 `str` 对象。

因此：

```python
name = "iron"
name = 100
```

完全合法。

结构变化：

```text
第一次：
name ─────> "iron"

第二次：
name ─────> 100
```

---

# 4. Java 静态变量类型 vs Python 动态名字绑定

## Java

```java
String value = "iron";

// 编译错误
value = 100;
```

变量 `value` 本身带有静态类型：

```text
String
```

## Python

```python
value = "iron"
value = 100
```

名字本身没有固定运行时声明类型。

但对象仍然有类型：

```python
print(type("iron"))
print(type(100))
```

分别是：

```text
<class 'str'>
<class 'int'>
```

因此最准确的一句话是：

> Python 不是“没有类型”，而是“对象有类型，名字不固定绑定某一种类型”。

---

# 5. Python 几乎一切都是对象

Python：

```python
count = 10
name = "iron"
items = []
```

`10`、`"iron"`、`[]` 都是对象。

甚至函数：

```python
def execute() -> None:
    pass

handler = execute
handler()
```

类本身也可以作为对象：

```python
class User:
    pass

clazz = User
user = clazz()
```

Java 要实现类似能力，往往需要：

```text
Function / Supplier / Consumer
Method Reference
Class<T>
Reflection
```

Python 从语言层面直接支持。

---

# 6. `id()`：观察对象 identity

Python：

```python
a = ["iron"]
b = a

print(id(a))
print(id(b))
```

`id(a)` 与 `id(b)` 相同，说明它们绑定的是同一个对象：

```text
a ─────┐
       ▼
   ["iron"]
       ▲
b ─────┘
```

注意：

> `id()` 适合学习对象模型，不应该被当成业务 ID。

它与我们后续 `iron-foundation/id` 中的 UUID、Snowflake ID 完全不是一回事。

---

# 7. Java 对象引用与 Python name binding 很接近

## Java

```java
List<String> a = new ArrayList<>();
List<String> b = a;
```

结构：

```text
a ─────┐
       ▼
  ArrayList
       ▲
b ─────┘
```

## Python

```python
a = []
b = a
```

结构：

```text
a ─────┐
       ▼
     list
       ▲
b ─────┘
```

所以“多个变量/名字共享同一个 mutable object”这一点，Java 与 Python 很接近。

---

# 8. `=` 不等于复制对象

```python
a = [1, 2, 3]
b = a
```

不要理解成：

```text
复制 a 得到 b
```

实际是：

```text
a ─────┐
       ▼
   [1,2,3]
       ▲
b ─────┘
```

执行：

```python
b.append(4)
```

那么：

```python
print(a)
```

结果：

```python
[1, 2, 3, 4]
```

---

# 9. Java 完全一样

```java
List<Integer> a = new ArrayList<>(List.of(1, 2, 3));
List<Integer> b = a;

b.add(4);
```

此时 `a` 同样变成：

```text
[1, 2, 3, 4]
```

因此：

> Python `b = a` 的共享对象语义，与 Java 的引用赋值基本一致。

---

# 10. Mutable 与 Immutable

| Python 类型 | 可变性 | Java 粗略类比 |
|---|---|---|
| `int` | Immutable | `Integer` |
| `float` | Immutable | `Double` |
| `bool` | Immutable | `Boolean` |
| `str` | Immutable | `String` |
| `tuple` | 外层结构 Immutable | record / immutable tuple-like |
| `frozenset` | Immutable | 不可变 Set |
| `list` | Mutable | `ArrayList` |
| `dict` | Mutable | `HashMap` |
| `set` | Mutable | `HashSet` |
| 普通自定义 class | 通常 Mutable | 普通 Java Bean |

---

# 11. Immutable：`int`

```python
a = 10
b = a
```

可以理解为：

```text
a ───┐
     ▼
     10
     ▲
b ───┘
```

执行：

```python
b = b + 1
```

并没有把 `10` 对象改成 `11`，而是让 `b` 重新绑定：

```text
a ─────> 10
b ─────> 11
```

---

# 12. Java `Integer` 对照

```java
Integer a = 10;
Integer b = a;

b = b + 1;
```

结果：

```text
a = 10
b = 11
```

因为 Java `Integer` 同样是 immutable。

---

# 13. Immutable：`str`

Python：

```python
name = "iron"
name.upper()

print(name)
```

仍然得到：

```text
iron
```

正确写法：

```python
name = name.upper()
```

原因：

> `str` 不可变，`upper()` 返回新的字符串对象。

---

# 14. Java `String` 对照

```java
String name = "iron";
name.toUpperCase();

System.out.println(name);
```

仍然是：

```text
iron
```

必须：

```java
name = name.toUpperCase();
```

所以：

```text
Java String
≈
Python str
```

在 immutable 语义上非常接近。

---

# 15. Mutable：`list`

```python
items = [1, 2, 3]
items.append(4)
```

这里是：

> 原对象自身被修改。

而不是重新创建一个 list。

```text
before:
items ─────> [1,2,3]

after:
items ─────> [1,2,3,4]
```

---

# 16. Java `ArrayList` 对照

```java
List<Integer> items = new ArrayList<>(List.of(1, 2, 3));
items.add(4);
```

也是原对象被修改。

因此：

```text
Python list
≈
Java ArrayList
```

在 mutable 语义上非常自然。

---

# 17. Mutate 与 Rebind：必须区分

假设：

```python
a = [1, 2]
b = a
```

## Mutate

```python
b.append(3)
```

结果：

```python
a == [1, 2, 3]
b == [1, 2, 3]
```

因为共同对象发生变化。

## Rebind

```python
b = [9, 9]
```

结构变成：

```text
a ─────> [1,2,3]
b ─────> [9,9]
```

这里只是 `b` 换了绑定对象。

---

# 18. Java Mutate vs Reassign

Java：

```java
List<Integer> a = new ArrayList<>();
List<Integer> b = a;

b.add(1);              // mutate
b = new ArrayList<>(); // reassign
```

对应 Python：

```python
a = []
b = a

b.append(1)  # mutate
b = []       # rebind
```

二者的思路几乎完全一致。

---

# 19. Python 参数传递到底是什么

不要简单死背：

```text
Python 是引用传递
```

也不要只记：

```text
Python 是值传递
```

更适合工程理解的是：

> 函数调用时，实参引用的对象会绑定给形参名字。

常见术语：

```text
Call by Sharing
Pass by Assignment
Object Sharing
```

---

# 20. 参数传递：Immutable 例子

```python
def change(value: int) -> None:
    value = 100

number = 10
change(number)

print(number)
```

结果：

```text
10
```

进入函数时：

```text
number ───┐
          ▼
          10
          ▲
value ────┘
```

执行：

```python
value = 100
```

只是：

```text
number ─────> 10
value  ─────> 100
```

---

# 21. Java primitive 参数对照

```java
void change(int value) {
    value = 100;
}

int number = 10;
change(number);
```

最终 `number` 仍然是 10。

---

# 22. 参数传递：Mutable 例子

```python
def add_item(items: list[str]) -> None:
    items.append("python")

values = ["java"]
add_item(values)

print(values)
```

结果：

```python
["java", "python"]
```

结构：

```text
values ─────┐
            ▼
        ["java"]
            ▲
items ──────┘
```

函数内部执行 `append()` 修改的是共享对象。

---

# 23. Java 对象参数对照

```java
void addItem(List<String> items) {
    items.add("python");
}

List<String> values = new ArrayList<>();
values.add("java");

addItem(values);
```

最终调用方同样可以看到修改。

---

# 24. 参数内部重新赋值

Python：

```python
def replace(items: list[str]) -> None:
    items = ["python"]

values = ["java"]
replace(values)

print(values)
```

结果：

```python
["java"]
```

因为内部只是 rebind：

```text
values ─────> ["java"]
items  ─────> ["python"]
```

---

# 25. Java 对照

```java
void replace(List<String> items) {
    items = new ArrayList<>();
}
```

也不会让调用方变量自动指向这个新 List。

---

# 26. 参数传递最推荐的心智模型

```text
调用之前：

outside_name ─────> Object

调用函数：

outside_name ─────┐
                  ▼
                Object
                  ▲
parameter_name ───┘
```

函数内部：

```text
Mutate Object
→ 调用者能观察到

Rebind parameter_name
→ 调用者变量不会被重新绑定
```

---

# 27. `==` 与 `is`

Python：

```python
a == b
```

通常表示：

> Equality：值/内容是否相等。

Python：

```python
a is b
```

表示：

> Identity：是否就是同一个对象。

---

# 28. Java 对应关系

对于普通 Java 对象：

```java
a == b
```

表示：

> 是否同一个对象引用。

而：

```java
a.equals(b)
```

表示：

> 值/业务语义是否相等。

因此可以粗略记：

| Java | Python |
|---|---|
| 对象 `a == b` | `a is b` |
| `a.equals(b)` | `a == b` |

这是阶段 2 必须记住的一张表。

---

# 29. `==`：值相等

```python
a = [1, 2]
b = [1, 2]

print(a == b)
```

结果：

```text
True
```

但是：

```python
print(a is b)
```

是：

```text
False
```

因为是两个不同 list 对象。

---

# 30. `is`：同一对象

```python
a = [1, 2]
b = a
```

此时：

```python
a == b  # True
a is b  # True
```

因为：

```text
a ───┐
     ▼
  [1,2]
     ▲
b ───┘
```

---

# 31. `is None`

Python 标准写法：

```python
if value is None:
    ...
```

原因：

> `None` 是一个特殊 singleton 对象。

所以这里比较 identity 非常符合语义。

---

# 32. 不要用 `is` 比较业务值

错误：

```python
status = "success"

if status is "success":
    ...
```

正确：

```python
if status == "success":
    ...
```

因为我们要比较的是字符串内容。

---

# 33. 为什么 `is` 有时看起来也能比较小整数

例如：

```python
a = 10
b = 10

print(a is b)
```

某些实现中可能得到 True。

这是由于 CPython 可能存在：

```text
small integer cache
string interning
```

属于解释器优化，不是业务语义。

生产规则：

```text
值比较 → ==
身份比较 → is
None    → is None
```

---

# 34. Python `==` 可以自定义

```python
class User:
    def __init__(self, name: str) -> None:
        self.name = name
```

```python
a = User("iron")
b = User("iron")
```

默认 `a == b` 通常是 False。

如果实现：

```python
def __eq__(self, other: object) -> bool:
    ...
```

就可以定义值相等规则。

Java 对应：

```java
@Override
public boolean equals(Object other) {
    ...
}
```

所以：

```text
Python __eq__
≈
Java equals
```

---

# 35. `is` 不可重载

`==` 可以通过 `__eq__()` 改变行为。

`is` 不能。

因此：

> `is` 永远代表 Object Identity。

---

# 36. Tuple Immutable 的真实含义

```python
data = (
    "iron",
    [1, 2],
)
```

不能：

```python
data[0] = "python"
```

也不能：

```python
data[1] = []
```

但是可以：

```python
data[1].append(3)
```

结果：

```python
("iron", [1, 2, 3])
```

---

# 37. 为什么 tuple 里面的 list 还能改

tuple 保证的是：

> tuple 自身保存的元素绑定关系不能被替换。

结构：

```text
tuple
  │
  ├────> "iron"
  │
  └────> list
           │
           └── mutable
```

所以 list 自身仍然可以变化。

---

# 38. Java `final` 类比

Java：

```java
final List<String> items = new ArrayList<>();
```

不允许：

```java
items = anotherList;
```

但允许：

```java
items.add("iron");
```

因此：

```text
final reference
≠
deep immutable object
```

这个思想与 Python tuple 持有 mutable 元素很类似。

---

# 39. Python `Final`

```python
from typing import Final

MAX_RETRY: Final = 3
```

它主要是静态类型层面的约束：

```text
IDE
Pyright
mypy
```

不能简单理解为 Java `final` 的运行时完全等价物。

---

# 40. 三种必须区分的复制语义

## 不复制

```python
b = a
```

## 浅拷贝

```python
b = a.copy()
```

或：

```python
import copy
b = copy.copy(a)
```

## 深拷贝

```python
import copy
b = copy.deepcopy(a)
```

---

# 41. 赋值：完全共享

```python
a = [1, 2, 3]
b = a
```

```text
a ───┐
     ▼
 [1,2,3]
     ▲
b ───┘
```

所以：

```python
a is b
```

True。

---

# 42. Shallow Copy：复制外层

```python
a = [1, 2, 3]
b = a.copy()
```

此时：

```python
a == b  # True
a is b  # False
```

表示：

> 内容相同，但外层已经是两个对象。

---

# 43. list 常见浅拷贝方式

```python
b = a.copy()
```

```python
b = list(a)
```

```python
b = a[:]
```

```python
import copy
b = copy.copy(a)
```

对于 list，这些都属于浅拷贝思路。

---

# 44. 嵌套结构为什么暴露浅拷贝本质

```python
a = [
    ["java"],
    ["python"],
]

b = a.copy()
```

结构：

```text
          ┌────> Inner 1
Outer A ──┤
          └────> Inner 2

          ┌────> Inner 1
Outer B ──┤
          └────> Inner 2
```

外层不同，内层仍共享。

---

# 45. 浅拷贝经典行为

```python
b[0].append("spring")
```

那么 `a` 也会看到：

```python
[
    ["java", "spring"],
    ["python"],
]
```

因为：

```python
a[0] is b[0]
```

为 True。

---

# 46. Java 浅拷贝类比

```java
List<List<String>> a = ...;
List<List<String>> b = new ArrayList<>(a);
```

新的外层 ArrayList 已创建，但内部 `List<String>` 仍然引用原对象。

因此：

```text
new ArrayList<>(a)
≈
a.copy()
```

都是典型 shallow copy。

---

# 47. Deep Copy

Python：

```python
import copy

b = copy.deepcopy(a)
```

大致结构：

```text
a ─────> Outer A
          │
          ├────> Inner A1
          └────> Inner A2

b ─────> Outer B
          │
          ├────> Inner B1
          └────> Inner B2
```

这样修改 `b` 的内层通常不会影响 `a`。

---

# 48. Assignment / Shallow / Deep 总表

| 操作 | 外层对象 | 内层对象 | 说明 |
|---|---|---|---|
| `b = a` | 共享 | 共享 | 只是新增引用 |
| `a.copy()` | 新对象 | 共享 | 浅拷贝 |
| `copy.copy(a)` | 新对象 | 共享 | 通用浅拷贝 |
| `copy.deepcopy(a)` | 新对象 | 尽量新建 | 深拷贝 |

---

# 49. 不要无脑 `deepcopy()`

`deepcopy()` 不是“最安全默认方案”。

可能带来：

```text
性能开销
大对象图递归复制
复制本应共享的状态
资源对象无法合理复制
隐藏 ownership 问题
设计意图模糊
```

例如这些通常不应该随意 deep copy：

```text
Database Connection
Redis Client
HTTP Client
Socket
Thread Lock
Thread Pool
Logger
Cache
Provider
Repository
```

生产代码更应该问：

> 谁拥有这个对象？谁允许修改？哪些状态应该共享？

---

# 50. Defensive Copy：防御式复制

Java：

```java
this.items = new ArrayList<>(items);
```

Python：

```python
self.items = list(items)
```

含义：

> 获取输入集合外层结构的独立 ownership。

有明确原因时非常合理，但不要见 list 就无脑 copy。

---

# 51. API 暴露内部 Mutable Object 的风险

```python
class Config:
    def __init__(self) -> None:
        self._values = {
            "timeout": 30,
        }

    def values(self) -> dict[str, object]:
        return self._values
```

调用方：

```python
config.values()["timeout"] = 999
```

直接修改了 Config 内部状态。

---

# 52. Java 同样存在这个问题

```java
public Map<String, Object> getValues() {
    return values;
}
```

调用方：

```java
config.getValues().put("timeout", 999);
```

同样破坏封装。

因此：

> Mutable object ownership 是 Java/Python 都需要认真设计的 API 问题。

---

# 53. 返回浅拷贝

Python：

```python
def values(self) -> dict[str, object]:
    return self._values.copy()
```

如果 value 主要是：

```text
str
int
float
bool
None
```

这类 immutable 值，浅拷贝通常已经够用。

---

# 54. Read-only Interface 思路

后续类型系统阶段会详细讲：

```python
Mapping[str, object]
```

相比：

```python
dict[str, object]
```

它表达的是：

> API 只承诺“可读取映射”，不承诺调用者拥有修改能力。

Java 可以类比：

```text
只读视图
Collections.unmodifiableMap
```

---

# 55. Python 最经典坑：Mutable Default Argument

错误：

```python
def add_item(
    item: str,
    items: list[str] = [],
) -> list[str]:
    items.append(item)
    return items
```

第一次：

```python
add_item("java")
```

得到：

```python
["java"]
```

第二次：

```python
add_item("python")
```

实际得到：

```python
["java", "python"]
```

---

# 56. 为什么默认 list 会共享

默认参数表达式在：

> 函数定义时求值一次。

可以理解：

```text
function object
      │
      └────> default list
```

每一次没有传入 `items` 时，都继续拿这个同一个 list。

---

# 57. Java 开发者为什么很容易踩坑

Java：

```java
void execute() {
    List<String> items = new ArrayList<>();
}
```

每次函数执行都会：

```text
new ArrayList<>()
```

而 Python：

```python
def execute(items=[]):
```

不是这个语义。

---

# 58. 正确写法

```python
def add_item(
    item: str,
    items: list[str] | None = None,
) -> list[str]:
    if items is None:
        items = []

    items.append(item)
    return items
```

这里的新 list 是在调用过程中创建的。

---

# 59. 默认参数安全原则

这些 immutable 默认值通常很自然：

```python
def execute(
    timeout: float = 3.0,
    enabled: bool = True,
    name: str = "iron",
) -> None:
    ...
```

对 mutable 默认值：

```text
list
dict
set
```

通常使用：

```python
None
```

再在函数内部创建。

---

# 60. dataclass 中同类问题

错误思路：

```python
from dataclasses import dataclass

@dataclass
class Task:
    tags: list[str] = []
```

正确：

```python
from dataclasses import dataclass, field

@dataclass
class Task:
    tags: list[str] = field(default_factory=list)
```

---

# 61. `default_factory` 的 Java 类比

Java：

```java
class Task {
    private List<String> tags = new ArrayList<>();
}
```

每个 `new Task()` 都得到自己的 List。

Python：

```python
field(default_factory=list)
```

表达相同意图：

> 每个实例创建自己的 list。

---

# 62. Class Attribute：共享状态

Python：

```python
class User:
    tags = []
```

这里 `tags` 是：

> Class Attribute。

```python
a = User()
b = User()

a.tags.append("java")
print(b.tags)
```

也会看到：

```python
["java"]
```

---

# 63. Java `static` 类比

Python：

```python
class User:
    tags = []
```

粗略对应：

```java
class User {
    static List<String> tags = new ArrayList<>();
}
```

都属于类级共享。

---

# 64. 实例属性正确方式

Python：

```python
class User:
    def __init__(self) -> None:
        self.tags: list[str] = []
```

此时：

```python
a = User()
b = User()
```

通常：

```python
a.tags is b.tags
```

为 False。

---

# 65. Java Instance Field 对照

```java
class User {
    private List<String> tags = new ArrayList<>();
}
```

每个对象都有自己的字段数据。

因此：

```text
Python self.tags
≈
Java instance field
```

---

# 66. Python 赋值模型非常统一

```python
a = 10
```

```python
user = User()
```

```python
handler = execute
```

```python
clazz = User
```

都可以统一理解：

```text
Name
 │
 ▼
Object
```

---

# 67. 函数参数也是局部 Name Binding

```python
def execute(data):
    ...
```

调用：

```python
execute(payload)
```

可以近似理解函数作用域内发生：

```text
data ─────> payload 所指向的对象
```

这个模型非常适合工程理解。

---

# 68. return 也不会自动复制

```python
def get_items(items: list[str]) -> list[str]:
    return items
```

```python
a = ["java"]
b = get_items(a)
```

那么：

```python
a is b
```

是 True。

`return` 不会自动做 defensive copy。

---

# 69. API 设计中的 Ownership

未来看到这些类型：

```text
Config
Options
Context
Headers
Metadata
State
```

都应该问：

```text
谁创建？
谁拥有？
谁可以改？
什么时候可以改？
是否共享？
是否需要 copy？
是否应该 immutable？
```

这已经不是 Python 语法问题，而是组件 API 设计问题。

---

# 70. 对 `iron-components-python` 的直接影响

未来我们会有：

```text
LockOptions
RetryOptions
MessageHeaders
TransactionContext
IdGeneratorConfig
```

这些对象的可变性会影响：

```text
线程安全
并发行为
API 可预测性
配置生命周期
调试难度
测试稳定性
```

---

# 71. Options 为什么通常适合 Immutable

假设运行中随意修改：

```python
options.max_attempts = 1000
```

可能出现：

```text
执行 A 使用 3
执行 B 使用 1000
```

配置生命周期变得不稳定。

因此：

```text
Options
Config Snapshot
Value Object
```

通常适合 immutable。

---

# 72. Java record → Python frozen dataclass

Java：

```java
public record RetryOptions(
        int maxAttempts,
        Duration delay) {
}
```

Python：

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RetryOptions:
    max_attempts: int
    delay_seconds: float
```

后续 Pythonic 设计阶段会详细展开。

---

# 73. `frozen=True` 不是 Deep Immutable

```python
@dataclass(frozen=True)
class Options:
    tags: list[str]
```

虽然重新赋值可能受限：

```python
options.tags = []
```

但内部 list：

```python
options.tags.append("x")
```

仍然可能变化。

所以：

```text
frozen reference-like field
≠
deep immutable graph
```

---

# 74. 真正 Immutable Collection 的思路

如果语义确实要求不可变，可以考虑：

| Mutable | Immutable 思路 |
|---|---|
| `list` | `tuple` |
| `set` | `frozenset` |
| `dict` | read-only Mapping / immutable representation |

例如：

```python
tags: tuple[str, ...]
```

比：

```python
tags: list[str]
```

更明确表达“创建后不应该修改”。

---

# 75. hash 与 Mutable/Immutable

Python：

```python
data = {}
data["iron"] = 1
```

字符串可以作为 key。

但是：

```python
data[["iron"]] = 1
```

会报：

```text
TypeError: unhashable type: 'list'
```

---

# 76. 为什么 list 不能作为 dict key

`dict` 依赖 hash table。

如果 key 可以随时 mutate，hash 可能变化，定位关系就不稳定。

因此：

> 可变 list 默认不可 hash。

---

# 77. Java HashMap 对照

Java Map Key 需要正确实现：

```java
equals()
hashCode()
```

并且：

> 参与 hashCode 的字段，在对象作为 Key 生命周期内最好不要变化。

这个原则与 Python 的 hashable 设计完全相通。

---

# 78. tuple 为什么可以作为 dict key

```python
cache = {
    ("user", 1001): "iron",
}
```

合法的前提是：

> tuple 内部元素也必须可 hash。

例如：

```python
("user", 1001)
```

可以。

如果：

```python
("user", [1, 2])
```

由于 list 不可 hash，整个 tuple 也不能作为稳定 hash key。

---

# 79. Python Hash 与 Java HashMap 对照

| 概念 | Java | Python |
|---|---|---|
| 值相等 | `equals()` | `__eq__()` |
| hash | `hashCode()` | `__hash__()` |
| Map | `HashMap` | `dict` |
| Set | `HashSet` | `set` |
| Key 稳定性 | hash 字段不要变化 | hashable 对象保持 hash 稳定 |

---

# 80. Object Identity vs Business Identity

Python：

```python
a is b
```

只说明：

> 两个引用是不是同一个 Python Object。

不能说明：

```text
是不是同一个用户
是不是同一个订单
是不是同一个 lock key
```

业务 identity 应该由字段判断：

```python
a.user_id == b.user_id
```

---

# 81. Java 中也是同一个问题

```java
userA == userB
```

只表示是否同一 JVM 对象引用。

真正业务身份通常使用：

```java
userA.getUserId().equals(userB.getUserId())
```

因此：

> Object Identity 与 Domain Identity 必须分开。

---

# 82. 不要拿 `id()` 当业务 ID

错误：

```python
business_id = id(order)
```

`id()` 只表示当前运行时对象 identity。

它不是：

```text
UUID
Snowflake ID
Database ID
Business Key
```

所以后续 `iron-foundation/id` 与 Python 内置 `id()` 是两个完全不同的问题。

---

# 83. 嵌套 dict 的浅拷贝

```python
config = {
    "provider": {
        "name": "redis",
    }
}

other = config.copy()
```

结构：

```text
config ─────> Outer Dict A
                 │
                 └────> Inner Dict

other  ─────> Outer Dict B
                 │
                 └────> same Inner Dict
```

因此：

```python
other["provider"]["name"] = "memory"
```

可能影响原 `config`。

---

# 84. Deepcopy 不是数据库快照

```python
copy.deepcopy(state)
```

只是：

> Python 内存对象图复制。

它不等于：

```text
Database Snapshot
Transaction Isolation
MVCC
Versioned State
```

技术组件设计里不要混淆内存复制与事务一致性。

---

# 85. Mutable Shared State 与并发

假设：

```python
shared_config = {
    "timeout": 3,
}
```

多个并发执行共同修改：

```python
shared_config["timeout"] = 10
```

就会涉及：

```text
共享状态
更新时序
一致性
业务原子性
```

这与 Java 的共享 mutable state 问题完全一致。

---

# 86. GIL 不等于共享状态自动安全

即使 CPython 存在 GIL，也不能推出：

```text
共享 dict/list 无需并发设计
```

仍然需要判断：

```text
多步骤操作是否原子？
业务状态是否可能交错？
是否需要 Lock？
是否应避免共享？
是否采用 immutable snapshot？
```

后续并发阶段会详细展开。

---

# 87. 对 LangGraph / AI State 的影响

以后会大量遇到：

```text
State
Messages
Context
Checkpoint
```

同样需要判断：

```text
节点是在原地 mutate State？
还是返回新 State？
历史状态是否共享内部 list/dict？
checkpoint 是真正快照还是引用？
```

所以阶段 2 对 AI 工程同样非常重要。

---

# 88. Java → Python 对象模型思维转换

Java 开发者常见思路：

```text
变量有静态类型
变量保存值/引用
对象通过 new 创建
```

Python 更推荐：

```text
Object exists
↓
Name binds Object
↓
Object is Mutable or Immutable
↓
Multiple Names may share Object
↓
Mutation changes Object
↓
Assignment rebinds Name
```

---

# 89. 阶段 2 最关键流程图

```text
              Name
               │
               ▼
             Object
            /      \
           /        \
   Immutable       Mutable
      │               │
 int / str        list / dict
 tuple*           set / class
      │               │
“修改”通常         可以原地修改
得到新对象           当前对象
      │               │
      └──────┬────────┘
             │
       多个 Name 可共享
             │
      ┌──────┴──────┐
      │             │
   Rebind         Mutate
   名字换对象      对象自己变
      │             │
其他名字不变     共享者能看到
```

`tuple*`：tuple 自身不可变，但可能持有 mutable 元素。

---

# 90. Java → Python 快速判断法

看到 Python 一行涉及对象的代码，先问五个问题：

1. 当前对象是 Mutable 还是 Immutable？
2. 这一行是在 Mutate Object 还是 Rebind Name？
3. 当前对象是否被多个名字共享？
4. 函数参数是否可能修改调用方共享对象？
5. API 是否暴露了内部 mutable state？

这五个问题可以解决绝大部分 Python 对象语义问题。

---

# 91. 对 `iron-foundation/time` 的影响

Time 工具经常返回：

```text
int
float
datetime
```

其中 `int/float` 是 immutable。

例如：

```python
timestamp = current_time_millis()
```

调用方无法通过原地修改这个 int 去破坏工具内部状态。

因此基础时间函数 ownership 很简单。

---

# 92. 对 `iron-foundation/id` 的影响

ID 工具经常返回：

```text
str
int
UUID
```

通常都是 value 语义。

例如：

```python
def uuid4_str() -> str:
    ...
```

返回 `str` 很适合作为：

```text
Business Identifier
Dict Key
Cache Key
Message ID
```

---

# 93. 对后续组件 Options 的影响

未来：

```text
RetryOptions
LockOptions
MessageOptions
TransactionOptions
```

优先考虑：

```text
Value Object
Immutable
Explicit Ownership
```

而不是到处传一个：

```python
dict[str, object]
```

然后随时修改。

---

# 94. 动态语言为什么更需要明确边界

Python 允许：

```python
config["max_retyr"] = 100
```

即使 key 拼错，可能也要运行时才发现。

因此生产 Python 更依赖：

```text
Type Hint
Dataclass
Protocol
Validation
Test
```

用工程手段强化边界。

---

# 95. Java / Python 对象模型核心速查表

| Java | Python | 说明 |
|---|---|---|
| Object reference | Name Binding | Python 更强调名字 |
| `new ArrayList<>()` | `[]` / `list()` | mutable list |
| `new HashMap<>()` | `{}` / `dict()` | mutable dict |
| `String` | `str` | immutable |
| `Integer` | `int` | immutable |
| `List.add()` | `list.append()` | mutate |
| `list = new ...` | `items = [...]` | rebind/reassign |
| 对象 `a == b` | `a is b` | identity |
| `a.equals(b)` | `a == b` | equality |
| `null` | `None` | singleton |
| `a == null` | `a is None` | Python 标准写法 |
| Copy Constructor | `.copy()` | 常见 shallow copy |
| 深复制手工方案 | `copy.deepcopy()` | 不要滥用 |
| `static field` | class attribute | 类级共享 |
| instance field | `self.xxx` | 实例状态 |
| record | frozen dataclass | Value Object 思路 |
| `hashCode()/equals()` | `__hash__/__eq__` | hash key 语义 |

---

# 96. 阶段 2 常见误区

## 误区 1：Python 变量就是“装值的盒子”

更准确：

```text
Name binds Object
```

## 误区 2：`b = a` 会复制对象

错误。通常只是增加一个绑定关系。

## 误区 3：Python 是引用传递，所以函数能改调用方变量

不准确。函数可以 mutate 共享对象，但形参 rebind 不会重新绑定调用方名字。

## 误区 4：Python `==` 和 Java `==` 一样

错误。对于对象语义：

```text
Python ==  ≈ Java equals()
Python is  ≈ Java object ==
```

## 误区 5：`is` 可以比较字符串和整数

业务值比较统一使用 `==`。

## 误区 6：`.copy()` 已经完全独立

错误，它通常只是 shallow copy。

## 误区 7：`deepcopy()` 永远最安全

错误，可能引入性能和语义问题。

## 误区 8：tuple immutable，所以内部所有对象也 immutable

错误，tuple 可以持有 mutable object。

## 误区 9：GIL 保证共享 mutable state 安全

错误，并发语义仍需要设计。

---

# 97. 阶段 2 应形成的生产习惯

1. Options / Config / Value Object 优先考虑 immutable。
2. 明确 list/dict 的 ownership。
3. API 不随意返回内部 mutable object。
4. 避免 mutable default argument。
5. 值比较使用 `==`。
6. `None` 判断使用 `is None`。
7. 不无脑使用 `deepcopy()`。
8. 看到嵌套容器时，意识到 shallow copy 仍共享内部对象。
9. Class Attribute 中的 mutable object 要特别谨慎。
10. Mutable Runtime State 与 Immutable Value Object 明确区分。

---

# 98. 完整 Java → Python 对比例子：RetryOptions

## Java

```java
public final class RetryOptions {

    private final int maxAttempts;
    private final List<String> retryableErrors;

    public RetryOptions(
            int maxAttempts,
            List<String> retryableErrors) {
        this.maxAttempts = maxAttempts;
        this.retryableErrors = new ArrayList<>(retryableErrors);
    }

    public int getMaxAttempts() {
        return maxAttempts;
    }

    public List<String> getRetryableErrors() {
        return List.copyOf(retryableErrors);
    }
}
```

体现：

```text
Value Object
Final Field
Defensive Copy
避免暴露 Mutable Internal State
```

---

# 99. Python 对应思路

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RetryOptions:
    max_attempts: int
    retryable_errors: tuple[str, ...]
```

使用：

```python
options = RetryOptions(
    max_attempts=3,
    retryable_errors=(
        "timeout",
        "connection_error",
    ),
)
```

Python 更短的原因：

```text
dataclass
+
tuple immutable
+
keyword arguments
```

替代大量 Java 样板代码。

---

# 100. 不是所有对象都应该 Immutable

例如 Runtime Context：

```python
class ExecutionContext:
    def __init__(self) -> None:
        self.attempt = 0
        self.metadata: dict[str, object] = {}

    def increment_attempt(self) -> None:
        self.attempt += 1
```

它本来就代表：

> 执行过程中的动态状态。

所以 mutable 是合理的。

---

# 101. Java Runtime Context 对照

```java
public class ExecutionContext {

    private int attempt;
    private final Map<String, Object> metadata = new HashMap<>();

    public void incrementAttempt() {
        attempt++;
    }
}
```

所以：

> Mutable 本身不是坏事，关键看领域语义。

---

# 102. Value Object vs Runtime State

| 类型 | 推荐可变性 |
|---|---|
| `RetryOptions` | Immutable |
| `LockOptions` | Immutable |
| `MessageOptions` | Immutable |
| `IdGeneratorConfig` | Immutable |
| `ExecutionContext` | Mutable |
| `LockRuntimeState` | Mutable |
| `RetryRuntimeState` | Mutable |
| Cache | Mutable |
| Metrics Recorder | Stateful |
| Provider Client | Stateful Resource |

这与 Java 技术组件设计思想完全一致。

---

# 103. 阶段 2 最终六句话

```text
1. Python 变量本质上是名字绑定对象。

2. = 默认不会复制对象。

3. Mutable Object 可以原地修改。

4. 多个名字共享 Mutable Object 时，Mutation 可以被其他引用观察到。

5. Rebind 只是让当前名字指向另一个对象。

6. == 比较 Equality，is 比较 Identity。
```

---

# 104. 阶段 2 自测题

如果下面问题可以清楚回答，本阶段基本过关：

1. Python 的变量为什么更准确叫“名字”？
2. `a = b` 是否会自动复制对象？
3. `list` 和 `str` 在可变性上有什么区别？
4. 为什么 `b.append()` 可能影响 `a`？
5. 为什么 `b = [...]` 不会重新绑定 `a`？
6. Python 函数参数为什么不能简单理解成传统“引用传递”？
7. 调用函数时，形参和实参的对象关系是什么？
8. Python `a == b` 更接近 Java 的哪个操作？
9. Python `a is b` 更接近 Java 的哪个操作？
10. 为什么 `None` 推荐 `is None`？
11. 为什么字符串不能用 `is` 做业务内容比较？
12. `copy.copy()` 与 `copy.deepcopy()` 的核心区别是什么？
13. 为什么浅拷贝嵌套 list 后，内层仍可能相互影响？
14. 为什么不应该无脑使用 `deepcopy()`？
15. `def foo(items=[])` 为什么危险？
16. 为什么 `field(default_factory=list)` 更安全？
17. Python class attribute 为什么类似 Java static field？
18. `tuple` 为什么不可变但内部 list 仍可以 mutate？
19. 为什么 list 不能作为 dict key？
20. 为什么作为 hash key 的对象应保持 hash 稳定？
21. 为什么 Options 通常适合 immutable？
22. 为什么 Runtime Context 又可能适合 mutable？
23. API 直接返回内部 dict 有什么风险？
24. `frozen=True` 是否代表 deep immutable？
25. `id(obj)` 与技术组件中的业务 ID 有什么本质区别？

---

# 105. 与阶段 1 的衔接

阶段 1 解决：

```text
Python 代码怎么写？
```

阶段 2 解决：

```text
Python 代码为什么会这样运行？
```

阶段 1 是语法入口。

阶段 2 是对象模型入口。

真正吃透阶段 2 后，会直接帮助理解：

```text
dataclass
Config / Options
API Ownership
Cache
Context
Concurrency
Async State
LangGraph State
技术组件边界
```

---

# 106. 下一阶段

下一篇进入：

> **阶段 3 —— Python 类型系统：Type Hint、Union、Optional、Generic、TypeVar、Protocol、ABC、Callable（Java → Python 对照版）**

继续统一使用：

```text
Java 概念
↓
Python 对应能力
↓
双代码对照
↓
核心差异
↓
生产实践
↓
常见坑
↓
iron-components-python 落地
↓
速查表
↓
自测题
```
