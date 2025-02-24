class Book:
    def __init__(self, book_id, title, author, genre, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.quantity = quantity

    def update_info(self, title=None, author=None, genre=None, quantity=None):

        if title:
            self.title = title
        if author:
            self.author = author
        if genre:
            self.genre = genre
        if quantity is not None:
            self.quantity = quantity

    def __str__(self):
        return f"{self.book_id} - {self.title} ({self.author}) [{self.genre}] - SL: {self.quantity}"
