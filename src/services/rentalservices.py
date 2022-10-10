from src.domain.rental import Rental
from src.validators.validationexception import ValidationException


class RentalServices:
    def __init__(self, rental, validator, book_repo, client_repo, book_valid, client_valid):
        self._rental = rental
        self._validator = validator
        self._book_repo = book_repo
        self._client_repo = client_repo
        self._book_valid = book_valid
        self._client_valid = client_valid

    def rent_a_book_service(self, rental_id, book_id, client_id, start, end):
        self._book_valid.validate_id(book_id)
        self._client_valid.validate_client_id(client_id)
        book_ok = 0
        client_ok = 0
        for obj in self._book_repo.get_book_list():
            if obj.book_id == book_id:
                book_ok = 1
        for obj in self._client_repo.get_client_list():
            if obj.client_id == client_id:
                client_ok = 1
        if book_ok == 0 or client_ok == 0:
            raise ValidationException("Not an existing ID.")
        rental = Rental(rental_id, book_id, client_id, start, end)
        self._validator.validate(rental)
        for obj in self._rental.get_list():
            if book_id == obj.book_id:
                raise ValidationException(["Book already rented."])
        self._rental.rent_a_book(rental)
        self.most_rented_book_service(rental)
        self.most_active_client_service(rental)

    def return_a_book(self, book_id):
        alright = 0
        other_alright = 0
        self._validator.validate_return(book_id)
        for obj in self._book_repo.get_book_list():
            if obj.book_id == book_id:
                other_alright = 1
        if other_alright == 0:
            return
        for obj in self._rental.get_list():
            if obj.book_id == book_id:
                alright = 1
        if alright == 1:
            return self._rental.return_book(book_id)
        else:
            raise ValidationException(["Can't return. Book not rented."])

    def return_a_book_client(self, client_id):
        alright = 0
        other_alright = 0
        self._validator.validate_return(client_id)
        for obj in self._client_repo.get_client_list():
            if obj.client_id == client_id:
                other_alright = 1
        if other_alright == 0:
            return
        for obj in self._rental.get_list():
            if obj.client_id == client_id:
                alright = 1
        if alright == 1:
            return self._rental.return_book_client(client_id)
        else:
            raise ValidationException(["Cannot return. Client did not rent any book."])

    def most_rented_book_service(self, rental):
        self._validator.validate(rental)
        self._rental.rent_stats(rental)

    def most_active_client_service(self, rental):
        self._validator.validate(rental)
        self._rental.most_active_client(rental)

    def sort_desc_client(self):
        lists = self._rental.get_most_active()
        lists.sort(key=lambda x: x[1], reverse=True)
        return lists

    def sort_desc_book(self):
        lists = self._rental.get_most_rented()
        lists.sort(key=lambda x: x[1], reverse=True)
        return lists

    def sort_desc_author(self):
        lists = self._rental.get_author_stats_list()
        lists.sort(key=lambda x: x[1], reverse=True)
        return lists

    def remove_both_service(self, book_id, client_id):
        self._client_valid.validate_client_id(client_id)
        self._book_valid.validate_id(book_id)
        self._rental.return_by_both_ids(book_id, client_id)

    def most_rented_author_service(self):
        author_list = self._rental.most_rented_author
        for item in author_list:
            print(str(item))
