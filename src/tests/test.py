from src.domain.book import Book
from src.domain.client import Client
from src.domain.rental import Rental

from src.repository.client_repo import ClientRepository
from src.repository.rental_repo import RentalRepository
from src.repository.book_repo import BookRepository

from src.validators.rentalvalidation import RentalValidator
from src.validators.bookvalidator import BookValidator
from src.validators.clientvalidator import ClientValidator

from src.validators.validationexception import ValidationException
import unittest


class Tests(unittest.TestCase):
    def test_create_book(self):
        book = Book(1, "Carte", "Aurel")
        self.assertEqual(book.book_id, 1)
        self.assertEqual(book.title, "Carte")
        self.assertEqual(book.author, "Aurel")
        book._book_id = 3
        self.assertEqual(book.book_id, 3)
        book._author = "Maria"
        self.assertEqual(book.author, "Maria")
        book._title = "Noua carte"
        self.assertEqual(book.title, "Noua carte")

    def test_create_client(self):
        client = Client(1, "Aurel")
        self.assertEqual(client.client_id, 1)
        self.assertEqual(client.client_name, "Aurel")
        client._client_id = 4
        self.assertEqual(client.client_id, 4)
        client._client_name = "Maria"
        self.assertEqual(client.client_name, "Maria")

    def test_create_rental(self):
        rental = Rental(1, 2, 3, 4, 5)
        self.assertEqual(rental.rental_id, 1)
        self.assertEqual(rental.book_id, 2)
        self.assertEqual(rental.client_id, 3)
        self.assertEqual(rental.rented_date, 4)
        self.assertEqual(rental.returned_date, 5)
        rental._book_id = 2
        self.assertEqual(rental.book_id, 2)
        rental._rental_id = 100
        self.assertEqual(rental.rental_id, 100)
        rental._client_id = 1000
        self.assertEqual(rental.client_id, 1000)
        rental._rented_date = 8
        self.assertEqual(rental.rented_date, 8)
        rental._returned_date = 30
        self.assertEqual(rental.returned_date, 30)

    def test_book_validator(self):
        book = Book(-1, "Maria", "ok")
        self.assertRaises(ValidationException, BookValidator.validate, book)
        book = Book(1, "", "ok")
        self.assertRaises(ValidationException, BookValidator.validate, book)
        book = Book(1, "Maria", "")
        self.assertRaises(ValidationException, BookValidator.validate, book)

    def test_client_validator(self):
        client = Client(-1, "Aurel")
        self.assertRaises(ValidationException, ClientValidator.validate, client)
        client = Client(1, "")
        self.assertRaises(ValidationException, ClientValidator.validate, client)

    def test_rental_validator(self):
        rental = Rental(-1, 1, 2, 3, 4)
        self.assertRaises(ValidationException, RentalValidator.validate, rental)
        rental = Rental(1, -1, 2, 3, 4)
        self.assertRaises(ValidationException, RentalValidator.validate, rental)
        rental = Rental(1, 1, -2, 3, 4)
        self.assertRaises(ValidationException, RentalValidator.validate, rental)
        rental = Rental(1, 2, 3, 10, 5)
        self.assertRaises(ValidationException, RentalValidator.validate, rental)
        rental = Rental(1, 2, 3, 10, -1)
        self.assertRaises(ValidationException, RentalValidator.validate, rental)

    def test_add_book_repo(self):
        repository = BookRepository()
        self.assertEqual(len(repository.get_book_list()), 0)
        repository.add_a_book(Book(1, 'Maria', 'Aurel'))
        self.assertEqual(len(repository.get_book_list()), 1)
        repository.add_a_book(Book(2, 'Maria', 'Aurel'))
        self.assertEqual(repository.get_book_list(), [Book(1, 'Maria', 'Aurel'), Book(2, 'Maria', 'Aurel')])
        self.assertRaises(ValidationException, repository.add_a_book, Book(1, 'Maria', 'Aurel'))

    def test_remove_book_repo(self):
        repository = BookRepository()
        self.assertEqual(len(repository.get_book_list()), 0)
        repository.add_a_book(Book(1, 'Maria', 'Aurel'))
        self.assertEqual(len(repository.get_book_list()), 1)
        repository.remove_book(1)
        self.assertEqual(len(repository.get_book_list()), 0)
        self.assertEqual(repository.get_book_list(), [])
        self.assertRaises(ValidationException, repository.remove_book, 1)

    def test_update_book(self):
        repository = BookRepository()
        self.assertEqual(len(repository.get_book_list()), 0)
        repository.add_a_book(Book(1, 'Maria', 'Aurel'))
        repository.update_book_list(1, "Aurel", "Maria")
        self.assertEqual(repository.get_book_list(), [Book(1, "Aurel", "Maria")])

    def test_add_client(self):
        repository = ClientRepository()
        self.assertEqual(repository.get_client_list(), [])
        repository.add_a_client(Client(1, 'Aurel'))
        self.assertEqual(len(repository.get_client_list()), 1)
        self.assertEqual(repository.get_client_list(), [Client(1, 'Aurel')])

    def test_remove_client(self):
        repository = ClientRepository()
        self.assertEqual(repository.get_client_list(), [])
        repository.add_a_client(Client(1, 'Aurel'))
        self.assertEqual(len(repository.get_client_list()), 1)
        self.assertEqual(repository.get_client_list(), [Client(1, 'Aurel')])
        repository.remove_client(1)
        self.assertEqual(repository.get_client_list(), [])

    def test_update_client(self):
        repository = ClientRepository()
        self.assertEqual(repository.get_client_list(), [])
        repository.add_a_client(Client(1, 'Aurel'))
        self.assertEqual(len(repository.get_client_list()), 1)
        self.assertEqual(repository.get_client_list(), [Client(1, 'Aurel')])
        repository.update_client(1, 'Maria')
        self.assertEqual(repository.get_client_list(), [Client(1, 'Maria')])

    def test_add_rental(self):
        repository = RentalRepository()
        self.assertEqual(repository.get_list(), [])
        repository.add_twenty_rentals()
        self.assertRaises(ValidationException, repository.rent_a_book, 1)

    def test_remove_rental(self):
        repository = RentalRepository()
        self.assertEqual(repository.get_list(), [])
        repository.add_twenty_rentals()
        repository.return_book(1)
        repository.return_book(2)
        repository.return_book(3)
