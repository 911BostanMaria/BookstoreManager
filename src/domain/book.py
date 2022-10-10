class Book:
    def __init__(self, book_id, title, author):
        self._book_id = book_id
        self._title = title
        self._author = author

    @property
    def book_id(self):
        return self._book_id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @book_id.setter
    def book_id(self, new_id):
        self._book_id = new_id

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @author.setter
    def author(self, new_author):
        self._author = new_author

    def __eq__(self, other):
        # Check if the id already exists.
        if isinstance(other, Book) is False:
            return False
        return self._book_id == other._book_id

    def __str__(self):
        return str(self._book_id) + ', ' + str(self._title) + ' written by ' + str(self._author)
