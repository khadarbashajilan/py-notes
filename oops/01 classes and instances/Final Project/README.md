# Library Book Tracker

A simple library management system demonstrating **Object-Oriented Programming (OOP)** in Python.

## How OOP Solves the Problem

Without OOP, we'd manage books using scattered variables and functions — a list of titles, another list of authors, separate status flags, etc. This gets messy and error-prone.

OOP lets us **bundle data + behavior** into a single `Book` class. Each book is an **object** that knows its own title, author, ISBN, and availability — and can **check itself out** or **return itself**. The code becomes organized, reusable, and mirrors the real world.

## The `Book` Class — Method by Method

### `__init__(self, title, author, isbn, is_available=True)`
Constructor. Creates a new book with a title, author, ISBN, and availability (default: available). Increments the class-level counter `total_books` each time a book is created.

### `checkout(self)`
Instance method. Marks the book as checked out (`is_available = False`) if it's currently available. Returns a success or error message. This keeps the checkout logic **inside the book object** rather than in scattered conditionals.

### `return_book(self)`
Instance method. Marks the book as available (`is_available = True`) if it was checked out. Returns a success or error message. Same benefit as `checkout` — the object manages its own state.

### `from_csv_isbn(cls, book_str)` — *classmethod*
Alternative constructor. Takes a comma-separated string like `"Title,Author,12345"`, validates the ISBN, and returns a new `Book` instance. This provides a **clean way to create books from external data** (CSV files, user input, etc.).

### `is_valid_isbn(isbn)` — *staticmethod*
Validates that an ISBN is exactly 5 digits. This utility method belongs to the `Book` class conceptually but doesn't need `self` or `cls` — hence it's a static method.

### `__str__(self)`
Returns a human-readable string like `'The Great Gatsby' by F. Scott Fitzgerald — Available`. Used when you `print()` a book object.

### `__repr__(self)`
Returns a developer-readable string like `Book('The Great Gatsby', 'F. Scott Fitzgerald', '12345', True)`. Useful for debugging.

### `total_books` — *class variable*
Tracks how many `Book` instances have been created across the entire program.

## OOP Pillars Demonstrated

| Pillar | How It's Used |
|---|---|
| **Encapsulation** | Book data (title, author, etc.) and operations (checkout, return) live together in one class |
| **Class Methods** | `from_csv_isbn()` creates books from strings without needing a separate builder function |
| **Static Methods** | `is_valid_isbn()` is a helper tied to the `Book` concept |
| **Instance vs Class State** | Each book has its own `is_available`; `total_books` is shared across all books |

## Files

| File | Purpose |
|---|---|
| `LibraryBookTracker.py` | The `Book` class with all methods |
| `main.py` | CLI terminal loop using Rich (not covered here) |
