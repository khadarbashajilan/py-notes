# Classes & Instances — Interview Prep

Interview-focused revision on Python OOP fundamentals — classes, instances, dunder methods, class/static methods, and design patterns.

---

## Topic 1 — `topic1.py` (Basic Class & Instance)

### Common Interview Questions

**Q: What happens when you call `Book("The Hobbit", "J.R.R. Tolkien", 310)`?**
- Python allocates memory, calls `__new__`, then calls `__init__` with the arguments.
- `__init__` sets instance attributes (`self.title`, `self.author`, `self.pages`).
- `self` is the newly created instance — Python passes it automatically.

**Q: What is the difference between `__init__` and `__new__`?**
- `__new__` creates the object (returns a new instance). Rarely overridden.
- `__init__` initializes the object (sets attributes). Used 99% of the time.
- `__new__` is called first, then `__init__`.

**Q: What is `self`?**
- `self` is the instance itself. It's a convention, not a keyword — you could name it `this`, but don't.
- Python passes the instance as the first argument automatically. The method definition must accept it.

**Q: What is `__str__` and when is it called?**
- Called by `print()`, `str()`, and f-strings.
- Must return a string. Should be human-readable.
- Falls back to `__repr__` if not defined.

**Q: How do you know if a method should be an instance method vs something else?**
- If it needs `self` (instance data), it's an instance method.
- If it needs `cls` (class data), it's a class method (`@classmethod`).
- If it needs neither, but is conceptually related, it's a static method (`@staticmethod`).

### Interview Edge Cases

- **Mutable default arguments in `__init__`** — A classic trap. Never use `def __init__(self, items=[])` — the list is shared across all instances.
- **`self` is not a keyword** — You could use any name, but every Python dev expects `self`.
- **`__init__` can return only `None`** — Returning anything else raises `TypeError`.

---

## Topic 2 — `topic2.py` (Class vs Instance Attributes)

### Common Interview Questions

**Q: What is the difference between a class attribute and an instance attribute?**
- **Class attribute:** Defined in the class body, shared by all instances. Accessed as `ClassName.attr` or `self.attr` (but `self.attr` can shadow it).
- **Instance attribute:** Set on `self` in `__init__` (or anywhere). Unique to each instance.

**Q: What happens when you access `self.discount_rate` vs `Product.discount_rate`?**
- `self.discount_rate` — Python first checks instance attributes, then class attributes, then parent classes.
- `Product.discount_rate` — Direct class access, skips instance lookup.

**Q: How would you implement a counter that tracks how many objects of a class were created?**
```python
class Product:
    count = 0
    def __init__(self, name):
        self.name = name
        Product.count += 1
```

**Q: Can you modify a class attribute through an instance?**
```python
obj.discount_rate = 0.2   # Creates a NEW instance attribute, shadows the class attribute
Product.discount_rate = 0.2  # Modifies the actual class attribute
```

### Interview Edge Cases

- **Shadowing trap** — Writing `self.x = val` when `x` is a class attribute doesn't modify the class attribute. It creates a new instance attribute that shadows it.
- **Mutable class attributes** — If a class attribute is mutable (list, dict), modifying it via any instance affects all instances. This is a common bug.
- **Lookup order** — Instance → Class → Parent classes. Python's MRO (Method Resolution Order) determines the search path.

---

## Topic 3 — `topic3.py` (`__str__` vs `__repr__`)

### Common Interview Questions

**Q: What is the difference between `__str__` and `__repr__`?**
| `__str__` | `__repr__` |
|---|---|
| For end users | For developers |
| Called by `print()`, `str()` | Called by `repr()`, REPL, debuggers |
| Should be readable | Should be unambiguous |
| Falls back to `__repr__` | Does **not** fall back to `__str__` |

**Q: What is the "official" guideline for `__repr__`?**
- Should return a string that could be used to recreate the object. E.g., `VideoGame(title='Mario', genre='Platformer', rating=4)`.
- If that's not practical, at least include the object's type and key state in angle brackets: `<VideoGame: Mario>`.

**Q: When would you define only `__repr__` and not `__str__`?**
- If the repr is already readable enough for both audiences. `__str__` falls back to `__repr__` when absent, so one method can serve both purposes.

**Q: What does the REPL use?**
- The REPL calls `repr()`, so `__repr__` determines what you see when you type an object's name in the REPL.

### Interview Edge Cases

- **Collections use `repr` for their elements** — When you print a list, it calls `repr()` on each element, not `str()`. So `print([game])` uses `__repr__`, not `__str__`.
- **`__repr__` should be unambiguous** — If you can't make it eval-able, at least include type + id or key fields in a standard format.
- **F-strings use `__str__`** — `f"{game}"` calls `__str__`. Use `f"{game!r}"` to force `__repr__`.

---

## Topic 4 — `topic4.py` (Class Methods, Static Methods & Alternative Constructors)

### Common Interview Questions

**Q: What is the difference between `@classmethod` and `@staticmethod`?**

| `@classmethod` | `@staticmethod` |
|---|---|
| Receives `cls` (the class) | Receives nothing extra |
| Can access/modify class state | Cannot access class or instance state |
| Used for alternative constructors | Used for utility functions |
| Can be inherited and will use the child class | Same, but doesn't know which class called it |

**Q: What is an alternative constructor?**
- A `@classmethod` that creates instances in a different way than `__init__`.
- Example: `BankAccount.create_account(name, balance)` or `BankAccount.from_string("Alice-500")`.
- Convention: use `from_*` or `create_*` naming.

**Q: When should you use `@staticmethod` vs a standalone function?**
- `@staticmethod` goes inside the class if the function is conceptually tied to the class (e.g., `BankAccount.is_valid_balance`).
- Use a standalone function if it's general-purpose and not tightly coupled.

**Q: How does `@classmethod` work with inheritance?**
- `cls` is the actual class that the method is called on, not the class where it's defined.
- So if `SavingsAccount.create_account(...)` is called, `cls` is `SavingsAccount`, not `BankAccount`.

**Q: What does the underscore prefix mean in `_next_account_number`?**
- Python convention for "internal use" / "private". Not enforced by the interpreter.
- `_var` — "protected" (internal use, but accessible).
- `__var` — name mangling (`_ClassName__var`), used to avoid subclass collisions.

### Interview Edge Cases

- **`@classmethod` vs inheritance gotcha** — If a `@classmethod` stores state on `cls`, each subclass gets its own copy of that state (because `cls` changes). This can be intentional or a bug.
- **When to NOT use `@staticmethod`** — If you find yourself referencing `ClassName` inside the method (like `BankAccount.minimum_balance`), consider whether the logic should be a class method or whether the reference should be `type(self).minimum_balance`.
- **`@classmethod` as a factory pattern** — Alternative constructors (`from_string`, `from_dict`, `from_csv`) are a common and clean design pattern in Python.

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

## Gotchas to Remember

1. `self.x = val` **shadows** the class attribute — doesn't modify it.
2. Mutable class attributes (lists, dicts) are **shared** — mutations affect all instances.
3. `__str__` falls back to `__repr__` — but not vice versa.
4. `print([obj])` uses `repr()` on elements, not `str()`.
5. `@classmethod` receives the **calling class** via `cls`, which changes with inheritance.
6. `__init__` must return `None` — returning anything else raises `TypeError`.
7. Default mutable arguments (`def __init__(self, x=[])`) are **evaluated once at definition time**, not per-call.
