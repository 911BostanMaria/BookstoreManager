from src.domain.book import Book
import random
from src.validators.validationexception import ValidationException


class BookRepository:
    def __init__(self):
        self._book_repo = []

    def get_book_list(self):
        return self._book_repo

    def add_twenty_books(self):
        """
        :return: None. Appends ten books to the book list.
        """
        title = ['In Search of Lost Time', "One Hundred Years of Solitude", "Hamlet", "War and Peace",
                 "The Great Gatsby", "The Odyssey", "Madame Bovary", "The Divine Comedy", "Lolita",
                 "Nineteen Eighty Four"]
        author = ['Marcel Proust', "Gabriel Garcia Marquez", "William Shakespeare", "Leo Tolstoy",
                  "F. Scott Fitzgerald", "Homer", "Gustave Flaubert", "Dante Alighieri", "Vladimir Nabokov",
                  "George Orwell"]
        for i in range(1, 21, 1):
            self._book_repo.append(Book(i, random.choice(title), random.choice(author)))

    def add_a_book(self, new_book):
        """
        :return: None. Appends a book to the book list.
        """
        if self.find_by_id(new_book.book_id) is False:
            self._book_repo.append(new_book)

    def find_by_id(self, book_id):
        """
        :param book_id: The ID of the book we need to find in the book list.
        :return: Returns the book if it is found, else returns false.
        """
        for obj in self._book_repo:
            if book_id == obj.book_id:
                return True
        return False

    def remove_book(self, book_id):
        """
        :param book_id: The ID of the book we want to delete from the book list.
        :return: None. Deletes book from book list.
        """
        ok = False
        for obj in self._book_repo:
            if book_id == obj.book_id:
                self._book_repo.remove(obj)
                ok = True
        if ok is False:
            raise ValidationException(['Not an existing book ID.'])

    def update_book_list(self, ids, new_title, new_author):
        """
        :param ids: The ID of the book we want to update.
        :param new_title: The title we want to update the book with.
        :param new_author:
        :return: None. Updates ID.
        """
        if self.find_by_id(ids) is False:
            raise ValidationException(["Not an existing book ID."])
        for obj in self._book_repo:
            if obj.book_id == ids:
                obj.title = new_title
                obj.author = new_author

    def search(self, user_input):
        search_list = []
        if not str(user_input).isnumeric():
            user_input = user_input.lower()
            for obj in self._book_repo:
                author = obj.author
                author = author.split(" ")
                title = obj.title
                title = title.split(" ")
                for i in range(0, len(title), 1):
                    title[i] = title[i].lower()
                    if title[i].find(user_input) > -1:
                        search_list.append(obj)
                for i in range(0, len(author), 1):
                    author[i] = author[i].lower()
                    if author[i].find(user_input) > -1:
                        search_list.append(obj)
        return search_list

    def search_book_by_id(self, user_input):
        for obj in self._book_repo:
            if obj.book_id == user_input:
                return obj
