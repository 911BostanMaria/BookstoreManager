from src.domain.rental import Rental
import random
from src.validators.validationexception import ValidationException
from src.repository.book_repo import BookRepository

class RentalRepository:
    def __init__(self):
        self._rentals = []
        self._most_rented = []
        self._most_active_client = []
        self._most_rented_author = []
        self.book_repo = BookRepository()

    def add_twenty_rentals(self):
        """
        :return: Adds twenty randomly generated rentals to the list.
        """
        for i in range(1, 21, 1):
            start_date = random.randint(1, 30)
            end_date = random.randint(start_date + 1, 31)
            id_pick = random.randint(1, 21)
            self._rentals.append(Rental(i, id_pick, i, start_date, end_date))
            self._most_rented.append([id_pick, 1])

    def rent_a_book(self, rental):
        """
        :param rental: The rental we want to add to the rental list.
        :return: Appends rental to the rental list if the book can be rented, else returns false.
        """
        if self.find_by_id(rental) is not False:
            raise ValidationException(["ID already exists."])
        self._rentals.append(rental)

    def return_book(self, book_ids):
        """
        :param book_ids: The ID of the rental we want to delete.
        :return: None. Deletes rental from the rental list.
        """
        ok = True
        len_of_rentals = len(self._rentals)
        i = 0
        operation_list = []
        try:
            while i <= len_of_rentals:
                if self._rentals[i].book_id == book_ids:
                    operation_list.append(['return', [self._rentals[i].rental_id, book_ids, self._rentals[i].client_id,
                                                      self._rentals[i].rented_date, self._rentals[i].returned_date]])
                    self._rentals.remove(self._rentals[i])
                    i = i - 1
                    len_of_rentals -= 1
                    ok = False
                i += 1
        except IndexError:
            pass
        if not ok:
            return operation_list
        else:
            raise ValidationException(["Inexisting ID."])

    def return_book_client(self, client_ids):
        """
        :param client_ids: The ID of the client who wants to return a book.
        :return: None. Deletes rental from the rental list.
        """
        ok = True
        len_of_rentals = len(self._rentals)
        i = 0
        operation_list = []
        try:
            while i <= len_of_rentals:
                if self._rentals[i].client_id == client_ids:
                    operation_list.append(['return', [self._rentals[i].rental_id, self._rentals[i].book_id, client_ids,
                                                      self._rentals[i].rented_date, self._rentals[i].returned_date]])
                    self._rentals.remove(self._rentals[i])
                    i = i - 1
                    len_of_rentals -= 1
                    ok = False
                i += 1
        except IndexError:
            pass
        if not ok:
            return operation_list
        else:
            raise ValidationException(["Inexisting ID."])

    def find_by_id(self, rental_id):
        """
        :param rental_id: The ID of the rental we need to find in the rental list.
        :return: Returns the rental if it is found, else returns false.
        """
        for obj in self._rentals:
            if rental_id == obj.rental_id:
                return obj
        return False

    def list_rentals(self):
        for obj in self._rentals:
            print(str(obj))

    def get_list(self):
        return self._rentals

    def get_most_rented(self):
        return self._most_rented

    def get_most_active(self):
        return self._most_active_client

    def most_active_client(self, rental):
        ok = 0
        for obj in self._most_active_client:
            if rental.client_id == obj[0]:
                obj[1] = obj[1] + 1
                ok = 1
        if ok == 0:
            self._most_active_client.append(([rental.client_id, 1]))

    def rent_stats(self, rental):
        ok = 0
        for obj in self._most_rented:
            if rental.book_id == obj[0]:
                obj[1] = obj[1] + 1
                ok = 1
        if ok == 0:
            self._most_rented.append([rental.book_id, 1])

    def get_author_stats_list(self):
        return self._most_rented_author

    def most_rented_author(self, rental):
        l = dict()
        book_list = self.book_repo.get_book_list()
        for item in book_list:
            if book_list[item].author not in l:
                l[book_list[item].author] = 1
            else:
                l[book_list[item].author] += 1
        author_list = list(l.items())
        author_list.sort(key=lambda x: x[1], reverse=True)
        return author_list

