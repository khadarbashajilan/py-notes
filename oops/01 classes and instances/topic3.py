class VideoGame:
    def __init__(self, title, genre, rating):
        self.title = title
        self.genre = genre
        self.rating = rating

    def __str__(self):
        rating = "⭐" * self.rating
        return f"{self.title} ({self.genre}) - {rating}"

    def __repr__(self):
        return f"VideoGame(title='{self.title}', genre='{self.genre}', rating={self.rating})"

game = VideoGame("Mario", "Platformer", 4)
print(game)
print(repr(game))
