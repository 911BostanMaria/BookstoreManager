from src.domain.book import Book


class BookServices:
    def __init__(self, book_repo, validator):
        self._book_repo = book_repo
        self._validator = validator

    def add_book_service(self, id_book, title_book, author_book):
        """
        Updates book using book validators and book repository.
        """
        book = Book(id_book, title_book, author_book)
        self._validator.validate(book)
        self._book_repo.add_a_book(book)

    def remove_book_service(self, book_to_remove):
        """
        Removes book using book repository.
        """
        if self._book_repo.find_by_id(book_to_remove) is not False:
            self._book_repo.remove_book(book_to_remove)
        else:
            raise ValueError("ID not found.")

    def update_book_service(self, ids, title, author):
        """
        Updates book using book validators and book repository.
        """

        self._validator.validate_title(title)
        self._validator.validate_author(author)
        self._validator.validate_id(ids)
        self._book_repo.update_book_list(ids, title, author)

    def search_book_by_author_or_title_service(self, user_input):
        if str(user_input) == "":
            raise ValueError("Cannot be an empty string.")
        return self._book_repo.search(user_input)

    def search_book_by_id_service(self, user_input):
        if str(user_input) == "":
            raise ValueError("Cannot be an empty string.")
        return self._book_repo.search_book_by_id(user_input)
