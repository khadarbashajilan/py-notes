# Shape Calculator — OOP Final Project

A Python project demonstrating core Object-Oriented Programming concepts including **Abstraction**, **Polymorphism**, **Inheritance**, and **Context Managers** through a shape calculation system.

---

## Project Structure

```
Final Project/
├── main.py                  # Entry point — creates shapes, displays info, logs data
├── log.txt                  # Output log file (generated at runtime)
├── shapes/
│   ├── __init__.py
│   ├── base_shape.py        # Abstract Base Class (ABC) for all shapes
│   ├── circle.py            # Circle implementation
│   ├── square.py            # Square implementation
│   ├── rectangle.py         # Rectangle implementation
│   └── triangle.py          # Triangle implementation
└── utils/
    ├── __init__.py
    ├── display.py            # Polymorphic display utility
    └── logger.py             # Context manager for file logging
```

---

## How to Run

```bash
python main.py
```

This will:
1. Print shape descriptions to the console.
2. Append shape data (area & perimeter) to `log.txt`.

---

## OOP Concepts Covered

### 1. Abstraction (Abstract Base Class — ABC)

**What is it?**
Abstraction means hiding complex implementation details and showing only the essential features of an object. In Python, we achieve this using the `ABC` (Abstract Base Class) from the `abc` module.

**How it's used here:**
`shapes/base_shape.py` defines a `Shape` class that inherits from `ABC`. It declares three abstract methods that **must** be implemented by any subclass:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    @abstractmethod
    def describe(self):
        pass
```

**Key points:**
- You **cannot instantiate** `Shape` directly — `Shape()` will raise a `TypeError`.
- Every concrete shape (Circle, Square, etc.) **must** implement `area()`, `perimeter()`, and `describe()`.
- If a subclass forgets to implement any abstract method, it becomes abstract itself and cannot be instantiated.
- This enforces a **contract** — all shapes guarantee they have `area()`, `perimeter()`, and `describe()`.

**Why use ABC?**
- Catches bugs early (missing method implementations raise errors at instantiation, not at runtime).
- Documents the expected interface clearly.
- Enables polymorphic code that works with any `Shape` subclass.

---

### 2. Polymorphism

**What is it?**
Polymorphism means "many forms." It allows objects of different classes to be treated through the same interface. Each class provides its own implementation of shared methods.

**How it's used here:**
All shape classes inherit from `Shape` and implement `area()`, `perimeter()`, and `describe()` differently:

```python
# Circle — uses pi * r^2
circle.area()  # pi * radius^2

# Square — uses side^2
square.area()  # side * side

# Triangle — uses 0.5 * base * height
triangle.area()  # 0.5 * base * height
```

The `print_all_info()` function treats all shapes the same way:

```python
def print_all_info(shapes):
    for shape in shapes:       # shape can be Circle, Square, Triangle, etc.
        print(shape.describe()) # Each shape's own describe() is called
```

**Polymorphism in action in `main.py`:**
```python
my_shapes = [Circle(5), Square(4)]  # List of different types
print_all_info(my_shapes)           # Same function works for all
```

**Key points:**
- The caller doesn't need to know the concrete type — it just calls `describe()`.
- Each shape provides its own version of `describe()`.
- This is **runtime polymorphism** (method dispatch happens at runtime based on the actual object type).

---

### 3. Inheritance

**What is it?**
Inheritance allows a new class to reuse attributes and methods from an existing class. The new class (child/subclass) extends the parent (superclass).

**How it's used here:**

```
Shape (ABC)          ← Abstract base class
├── Circle           ← Inherits from Shape
├── Square           ← Inherits from Shape
├── Rectangle        ← Inherits from Shape
└── Triangle         ← Inherits from Shape
```

```python
class Circle(Shape):          # Circle inherits from Shape
    def __init__(self, radius):
        self.radius = radius  # Circle-specific attribute

    def area(self):           # Implements abstract method
        return pi * self.radius ** 2
```

**Key points:**
- `Shape` defines the interface (what all shapes must do).
- Each subclass provides the implementation (how each shape does it).
- Inheritance avoids code duplication — all shapes share the same base contract.

---

### 4. Context Manager Protocol

**What is it?**
A context manager is an object that defines a pair of methods (`__enter__` and `__exit__`) to set up and tear down a resource. Python's `with` statement uses this protocol.

**Why use it?**
- Ensures resources (files, network connections, locks) are **always cleaned up**, even if an exception occurs.
- Makes code cleaner and less error-prone than manual `try/finally` blocks.

**How it's used here (`utils/logger.py`):**

```python
class ShapeLogger:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        """Called when 'with' block starts — opens the file."""
        self.file = open(self.filename, 'a')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when 'with' block ends — closes the file."""
        if self.file:
            self.file.close()

    def write(self, shape):
        """Custom method to log shape data."""
        if self.file:
            log_entry = f"{shape} | Area: {shape.area():.2f} | Perimeter: {shape.perimeter():.2f}\n"
            self.file.write(log_entry)
```

**Usage:**
```python
with ShapeLogger('log.txt') as log:
    log.write(circle)
    log.write(square)
# File is automatically closed here, even if an exception occurred
```

**Execution flow:**
1. `ShapeLogger('log.txt')` → `__init__` stores the filename.
2. `__enter__()` is called → opens the file, returns `self`.
3. `log.write(shape)` → writes data to the open file.
4. `__exit__()` is called → closes the file automatically.

---

### 5. Alternative: `@contextmanager` Decorator

The class-based context manager works perfectly, but Python provides a **simpler, function-based** alternative using `@contextmanager` from the `contextlib` module. This avoids writing a full class with `__enter__` and `__exit__`.

**The `@contextmanager` approach:**

```python
from contextlib import contextmanager

@contextmanager
def shape_logger(filename='log.txt'):
    """Function-based context manager using @contextmanager."""
    file = None
    try:
        file = open(filename, 'a')

        class Logger:
            """Simple wrapper to provide a write() method."""
            def write(self, shape):
                log_entry = f"{shape} | Area: {shape.area():.2f} | Perimeter: {shape.perimeter():.2f}\n"
                file.write(log_entry)

        yield Logger()  # This value becomes the 'as' variable
    finally:
        if file:
            file.close()
```

**Usage (same as before):**
```python
with shape_logger('log.txt') as log:
    log.write(circle)
    log.write(square)
# File is automatically closed here
```

**Simpler version without a wrapper class (if you only need direct file access):**

```python
from contextlib import contextmanager

@contextmanager
def shape_logger(filename='log.txt'):
    """Minimal function-based context manager — yields the file directly."""
    file = open(filename, 'a')
    try:
        yield file
    finally:
        file.close()
```

**Usage:**
```python
with shape_logger('log.txt') as f:
    f.write(f"{circle} | Area: {circle.area():.2f}\n")
    f.write(f"{square} | Area: {square.area():.2f}\n")
```

**How `@contextmanager` works:**

| Step | What Happens |
|------|-------------|
| `yield` before the `with` block | Code **before** `yield` runs during `__enter__` |
| `yield value` | The yielded value becomes the `as` variable |
| Code **after** `yield` | Runs during `__exit__`, regardless of exceptions (if in `finally`) |

**Class-based vs `@contextmanager` — When to use which:**

| Feature | Class-based (`__enter__`/`__exit__`) | `@contextmanager` |
|---------|--------------------------------------|-------------------|
| Syntax | More verbose, requires a class | Concise, function-based |
| State | Easy to hold state via `self` | State is local variables |
| Reusability | Better for complex, reusable managers | Best for simple, one-off managers |
| Readability | Clear protocol structure | Linear code flow |
| Custom methods | Easy to add (e.g., `write()`) | Needs a wrapper class or yields the resource |

**Recommendation:** Use `@contextmanager` for simple resource management (files, locks). Use the class-based approach when you need custom methods or complex state management.

---

### 6. `__str__` vs `describe()`

In this project, `describe()` is a custom method that returns a formatted string. In Python, the convention is to use `__str__()` for this purpose so that `print(shape)` and `str(shape)` automatically call it.

**Optional improvement:**
```python
class Circle(Shape):
    # ... other methods ...

    def __str__(self):
        return f"Circle(radius = {self.radius}, area = {self.area():.2f}, perimeter = {self.perimeter():.2f})"

    def describe(self):
        return str(self)  # Reuse __str__
```

Then you could simply do:
```python
print(circle)  # Automatically calls __str__
```

---

### 7. Encapsulation (Note)

Encapsulation means bundling data and methods together and restricting direct access to internal state. In this project, shape attributes (`radius`, `side`, etc.) are public. For true encapsulation, you could use properties:

```python
class Circle(Shape):
    def __init__(self, radius):
        self._radius = radius  # Convention: underscore = "private"

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value
```

---

## Shape Implementations

| Shape | Attributes | Area Formula | Perimeter Formula |
|-------|-----------|--------------|-------------------|
| Circle | radius | π × r² | 2 × π × r |
| Square | side | side² | 4 × side |
| Rectangle | length, width | length × width | 2 × (length + width) |
| Triangle | base, height, side_a, side_c | 0.5 × base × height | side_a + base + side_c |

---

## Sample Output

**Console:**
```
Circle(radius = 5, area = 78.54, perimeter = 31.42)
Square(Side = 4, Area = 16, Perimeter = 16)
```

**log.txt:**
```
Circle(radius = 5, area = 78.54, perimeter = 31.42) | Area: 78.54 | Perimeter: 31.42
Square(Side = 4, Area = 16, Perimeter = 16) | Area: 16.00 | Perimeter: 16.00
```

---

## Key Takeaways

| Concept | What You Learn |
|---------|---------------|
| **Abstraction** | Define contracts with ABC; hide implementation behind interfaces |
| **Polymorphism** | Same method call, different behavior based on object type |
| **Inheritance** | Share code and enforce structure via base classes |
| **Context Manager** | Safely manage resources (files) with `with` statement |
| **`@contextmanager`** | Simpler function-based alternative to class context managers |
| **`@abstractmethod`** | Force subclasses to implement required methods |
