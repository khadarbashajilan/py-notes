class VideoGame:
    def __init__(self, title, genre, rating):
        """Initialize a VideoGame with title, genre, and rating (1-5)."""
        self.title = title
        self.genre = genre
        self.rating = rating

    def __str__(self):
        """Return a human-readable string with star rating."""
        rating = "⭐" * self.rating
        return f"{self.title} ({self.genre}) - {rating}"

    def __repr__(self):
        """Return an unambiguous string that could recreate the object."""
        return f"VideoGame(title='{self.title}', genre='{self.genre}', rating={self.rating})"

game = VideoGame("Mario", "Platformer", 4)
print(game)
print(repr(game))

# ============================================================
# Concept: __str__ vs __repr__
# ============================================================
# __str__ is meant to be readable by humans (used by print()).
# __repr__ is meant to be unambiguous for developers (used by
# repr() and in the REPL). A good rule: __repr__ should look
# like a valid Python expression to recreate the object.
#
# Key Terminology:
#   - __str__:  Magic method for human-readable output
#   - __repr__: Magic method for unambiguous / developer output
#   - Magic Methods: Special methods with double underscores
#                    (dunder methods) that Python calls implicitly
#   - REPL:     Read-Eval-Print Loop (interactive Python shell)
# ============================================================"
