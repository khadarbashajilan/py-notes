class Book:
    total_books = 0

    def __init__(self, title, author, isbn, is_available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = is_available
        Book.total_books += 1

    def checkout(self):
        if not self.is_available:
            return f"'{self.title}' is already checked out."
        self.is_available = False
        return f"Successfully Checked Out '{self.title}'"

    def return_book(self):
        if self.is_available:
            return f"'{self.title}' was already in the library."
        self.is_available = True
        return f"Successfully Returned '{self.title}'"

    @classmethod
    def from_csv_isbn(cls,book_str):
        title, author, isbn = book_str.split(",")

        if not cls.is_valid_isbn(isbn.strip()):
            raise ValueError("Invalid ISBN. It must be exactly a 5-digit number.")
        return cls(title.strip(),author.strip(),isbn.strip())

    @staticmethod
    def is_valid_isbn(isbn):
        return isbn.isdigit() and len(isbn) == 5
  
    def __str__(self):
        status = "Available" if self.is_available else "Checked Out"
        return f"'{self.title}' by {self.author} — {status}"

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.isbn}', {self.is_available})"








