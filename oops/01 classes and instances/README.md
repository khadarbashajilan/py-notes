# Classes & Instances — Theory & Revision Notes

Python OOP fundamentals — classes, instances, dunder methods, class/static methods, and design patterns. These notes explain the *theory* first; use them as a primer before attempting interview questions.

---

## Topic 1 — `topic1.py` (Basic Class & Instance)

### Core Concepts

**What is a class?**
- A class is a **blueprint** for creating objects. It bundles data (attributes) and behavior (methods) together.
- Defined with the `class` keyword. By convention, class names use `PascalCase`.

**What is an instance?**
- An instance is a **concrete object** created from a class. Each instance has its own set of instance attributes.

**Object creation flow (`__new__` → `__init__`):**
1. `__new__` — Allocates memory and returns a new object. Called first. Rarely overridden.
2. `__init__` — Initializes the newly created object. Sets up instance attributes. Returns `None`.
3. The instance is automatically passed as the first argument (`self`) to `__init__`.

**`self` — The instance reference:**
- `self` is a convention (not a keyword). It refers to the current instance.
- Python automatically passes the instance as the first argument when you call a method on an object.
- Inside the class, you use `self` to access instance attributes and other instance methods.

**The `__str__` method:**
- Called by `print()`, `str()`, and f-strings to produce a human-readable string.
- Must return a string. If not defined, Python falls back to `__repr__`.

### Instance Methods
- Regular methods defined inside a class that take `self` as the first parameter.
- They operate on **instance data** — the attributes stored on `self`.

### Key Design Points

| Concept | Explanation |
|---------|-------------|
| `__new__` | Creates the object. Returns a new instance. Rarely used. |
| `__init__` | Initializes the object. Sets attributes. Used 99% of time. |
| `self` | The instance itself. Passed automatically. Convention, not keyword. |
| `__str__` | Human-readable output for `print()`, `str()`, f-strings. |

### Common Pitfalls
- **Mutable default arguments:** `def __init__(self, items=[])` evaluates the list once at definition time — all instances share the same list.
- **`__init__` must return `None`:** Returning a non-`None` value raises `TypeError`.
- **`self` naming:** While you could name it anything, always use `self` for readability.

---

## Topic 2 — `topic2.py` (Class vs Instance Attributes)

### Core Concepts

**Class Attributes:**
- Defined directly inside the class body, outside any method.
- **Shared** across all instances of the class.
- Accessed via `ClassName.attribute` or `self.attribute` (but `self` can shadow it).
- Useful for constants, default values, counters shared across all instances.

**Instance Attributes:**
- Set on `self`, typically inside `__init__`.
- **Unique** to each instance.
- Accessed via `self.attribute`.

### Attribute Lookup Order (MRO)
```
Instance → Class → Parent classes
```
Python follows the **Method Resolution Order (MRO)** when looking up an attribute:
1. Check instance `__dict__` first.
2. If not found, check class `__dict__`.
3. If not found, check parent classes in MRO order.

### The Shadowing Trap

```python
obj.x = val   # Creates a NEW instance attribute that shadows the class attribute
Class.x = val # Modifies the actual class attribute
```
- Assigning to `self.x` never modifies the class attribute — it creates or updates an instance attribute that shadows the class one.

### Mutable Class Attributes
- If a class attribute is a **mutable** object (list, dict, set), modifying it *through* any instance affects all instances — because the mutation happens on the shared object itself.
- This is a common source of bugs. Reassigning (`self.x = [1,2]`) creates a new instance attribute; mutating (`self.x.append(3)`) modifies the shared class attribute.

### Key Points

| Concept | Class Attribute | Instance Attribute |
|---------|----------------|-------------------|
| Where defined | In class body, outside methods | On `self`, usually in `__init__` |
| Scope | Shared by all instances | Unique per instance |
| Shadowing | Can be shadowed by instance attr | Always takes priority in lookup |
| Modification | `ClassName.attr = val` | `self.attr = val` |

---

## Topic 3 — `topic3.py` (`__str__` vs `__repr__`)

### Core Concepts

**`__str__` — For end users:**
- Called by `print()`, `str()`, and f-strings (`f"{obj}"`).
- Should return a **readable**, user-friendly string.
- If `__str__` is not defined, Python falls back to `__repr__`.

**`__repr__` — For developers:**
- Called by `repr()`, the REPL, debuggers, and container `print()` calls.
- Should return an **unambiguous** string, ideally one that could recreate the object.
- Does **not** fall back to `__str__`.

### The Official Guideline
- `__repr__` should be **eval-able** where practical: `VideoGame(title='Mario', genre='Platformer', rating=4)`.
- If that's not feasible, use angle brackets with type and key info: `<VideoGame: Mario>`.

### When to Define Only `__repr__`
- If the repr is already readable enough for both developers and end users.
- Since `__str__` falls back to `__repr__`, one method can serve both purposes.

### Container Behavior (Important)
- When you print a list/tuple/dict of objects, Python calls `repr()` on each element, **not** `str()`.
  ```python
  print([game])  # Uses __repr__, not __str__
  ```
- This is because containers use `repr()` for their elements.

### String Formatting

| Expression | Method Called |
|------------|--------------|
| `print(obj)` | `__str__` |
| `str(obj)` | `__str__` |
| `f"{obj}"` | `__str__` |
| `f"{obj!r}"` | `__repr__` |
| `repr(obj)` | `__repr__` |
| REPL (typing `obj`) | `__repr__` |
| `print([obj])` | `repr()` on elements → `__repr__` |

---

## Topic 4 — `topic4.py` (Class Methods, Static Methods & Alternative Constructors)

### Core Concepts

**Instance Methods (`self`):**
- Receive `self` — the instance.
- Can access and modify instance attributes.
- Default method type. Use when logic depends on instance data.

**Class Methods (`@classmethod`, `cls`):**
- Receive `cls` — the class itself (not the instance).
- Can access and modify **class-level** state (class attributes).
- Commonly used as **alternative constructors** — factory methods that create instances differently than `__init__`.
- `cls` is the **calling class**, so with inheritance, `cls` changes to the child class.

**Static Methods (`@staticmethod`):**
- Receive neither `self` nor `cls`.
- Behave like regular functions but live in the class namespace.
- Used for utility functions conceptually tied to the class.
- Cannot access class or instance state directly (though you can reference `ClassName.attr` explicitly).

### Comparison

| Aspect | `@classmethod` | `@staticmethod` |
|--------|---------------|-----------------|
| First param | `cls` (the class) | Nothing extra |
| Access class state | Yes (via `cls`) | No (must hardcode class name) |
| Access instance state | No | No |
| Inheritance behavior | `cls` follows child class | No awareness of caller |
| Use case | Alternative constructors, class-level state mgmt | Utility/logic tied to class |

### Alternative Constructors (Factory Pattern)
- A `@classmethod` that returns a new instance.
- Provides an alternative way to create objects besides `__init__`.
- Naming convention: `from_*` or `create_*`.
- Examples: `BankAccount.create_account(name, balance)`, `BankAccount.from_string("Alice-500")`.

### Naming Conventions for "Private" Attributes

| Prefix | Meaning | Behavior |
|--------|---------|----------|
| `_var` | "Protected" / internal use | Convention only. Accessible from outside. |
| `__var` | "Private" | Name mangling: `_ClassName__var`. Prevents accidental subclass collisions. |
| `__var__` | Dunder / magic method | Reserved for Python's special methods. |

### Key Design Notes

- **`@classmethod` with inheritance:** Each subclass gets its own `cls`, so class-level state stored via `cls.attr` is independent per subclass.
- **`@staticmethod` vs standalone function:** Use `@staticmethod` when the function is conceptually tied to the class (e.g., `BankAccount.is_valid_balance`). Use a standalone function if it's general-purpose.
- **When to NOT use `@staticmethod`:** If you find yourself hardcoding `ClassName` inside a static method (e.g., `BankAccount.minimum_balance`), consider whether it should be a `@classmethod` instead.

---

## Quick Reference: OOP in Python

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Class definition | `class Foo:` | Blueprint |
| Constructor | `def __init__(self):` | Initialize instance |
| Instance method | `def method(self):` | Operates on instance |
| Class method | `@classmethod def method(cls):` | Operates on class |
| Static method | `@staticmethod def method():` | Utility in class namespace |
| `__str__` | `def __str__(self):` | User-friendly string |
| `__repr__` | `def __repr__(self):` | Developer-friendly string |
| Class attribute | `x = val` in class body | Shared state |
| Instance attribute | `self.x = val` | Per-object state |

---

## Common Gotchas

1. **Shadowing:** `self.x = val` shadows the class attribute — doesn't modify it.
2. **Mutable class attributes:** Lists/dicts as class attributes are **shared** — mutations affect all instances.
3. **`__str__` fallback:** `__str__` falls back to `__repr__` — but not vice versa.
4. **Containers use `repr`:** `print([obj])` calls `repr()` on elements, not `str()`.
5. **`@classmethod` inheritance:** `cls` is the **calling class**, which changes with inheritance.
6. **`__init__` return:** Must return `None` — returning anything else raises `TypeError`.
7. **Mutable defaults:** `def __init__(self, x=[])` is evaluated once at definition time, not per-call.
8. **Attribute lookup order:** Instance → Class → Parent classes (MRO).
