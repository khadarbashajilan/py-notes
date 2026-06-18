class Book:
    def __init__(self, title, author, pages):
        """Initialize a Book instance with title, author, and page count."""
        self.title = title
        self.author = author
        self.pages = pages

    def describe(self):
        """Return a formatted description of the book."""
        return f"The book '{self.title}' by {self.author} has {self.pages} pages"

    def is_long(self):
        """Return True if the book has more than 300 pages."""
        return self.pages > 300

    def __str__(self):
        """Return a readable string representation of the book."""
        return f"📖 '{self.title}' by {self.author} ({self.pages} pages)"

# Create books manually
book1 = Book("The Hobbit", "J.R.R. Tolkien", 310)
book2 = Book("1984", "George Orwell", 328)
book3 = Book("The Catcher in the Rye", "J.D. Salinger", 277)

# Test them
print("--- Individual books ---")
print(book1)  # Uses __str__
print(book1.describe())  # Uses describe()
print(f"Is '{book1.title}' long? {book1.is_long()}")  # True (310>300)
print(f"Is '{book3.title}' long? {book3.is_long()}")  # False

# Your loop example (improved)
print("\n--- Books from loop ---")
books_from_loop = []
for i in range(4):
    title = f'Book_{i}'  # f-string is cleaner
    pages = i * 100
    author = f'Author_{i}'
    books_from_loop.append(Book(title, author, pages))

for book in books_from_loop:
    print(book.describe())
    print(f"  Long book? {book.is_long()}")

# ============================================================
# Concept: Classes and Instances
# ============================================================
# A class is a blueprint for creating objects. An instance is a
# concrete object created from that blueprint. Each instance has
# its own attribute values (title, author, pages) but shares the
# methods defined in the class. Here, Book is the class; book1,
# book2, book3, and the loop-created books are instances.
#
# Key Terminology:
#   - Class:    A user-defined prototype (e.g., Book)
#   - Instance: A specific object created from a class
#   - __init__: The constructor method that runs when a new
#               instance is created
#   - self:     Refers to the current instance inside class methods
#   - Method:   A function defined inside a class
#   - __str__:  A special method that returns a human-readable
#               string representation of the object
# ============================================================"
