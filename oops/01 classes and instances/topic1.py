class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def describe(self):
        # Return instead of print (more flexible)
        return f"The book '{self.title}' by {self.author} has {self.pages} pages"

    def is_long(self):
        return self.pages > 300

    def __str__(self):
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
