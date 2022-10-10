from src.validators.validationexception import ValidationException
from src.validators.bookvalidator import BookValidator
from src.validators.clientvalidator import ClientValidator
from src.validators.rentalvalidation import RentalValidator
from src.repository.client_repo import ClientRepository
from src.repository.book_repo import BookRepository
from src.repository.rental_repo import RentalRepository
from src.services.rentalservices import RentalServices
from src.services.clientservices import ClientServices
from src.services.bookservices import BookServices
from src.services.undoo_redo import UndoRedo
from src.domain.book import Book
from src.domain.client import Client
from src.validators.serviceerrors import ServiceError


class UserInterface:
    def __init__(self):
        self._book_repo = BookRepository()
        self._client_repo = ClientRepository()
        self._rental_repo = RentalRepository()
        self._book_validator = BookValidator()
        self._client_validator = ClientValidator()
        self._rental_validator = RentalValidator()
        self._book_services = BookServices(self._book_repo, self._book_validator)
        self._client_services = ClientServices(self._client_repo, self._client_validator)
        self._rental_services = RentalServices(self._rental_repo, self._rental_validator, self._book_repo,
                                               self._client_repo, self._book_validator, self._client_validator)
        self._undo_service = UndoRedo(self._book_services, self._client_services, self._rental_services)

    @staticmethod
    def print_menu():
        print("1 for adding a book.")
        print("2 for deleting a book.")
        print("3 for updating a book.")
        print("4 for listing book list.")
        print("5 for searching for a book by author or title.")
        print("6 for searching for a book by ID.")
        print(" ")
        print("7 for adding a client.")
        print("8 for deleting a client.")
        print("9 for updating a client.")
        print("10 for listing client.")
        print("11 for searching for a client by ID.")
        print("12 for searching for a client by name.")
        print(" ")
        print("13 for renting a book.")
        print("14 for returning a book.")
        print("15 for listing rentals.")
        print("16 for most rented book.")
        print("17 for most active client.")
        print("18 for most rented author.")
        print(" ")
        print("19 for undo.")
        print("20 for redo.")
        print(" ")
        print("21 for exit.")

    def ui_add_book(self):
        try:
            book_id = int(input("Enter book id:"))
        except ValueError:
            print("Invalid ID.")
            return
        book_name = input("Enter book name:")
        author_name = input("Enter author name:")
        try:
            self._book_services.add_book_service(book_id, book_name, author_name)
            self._undo_service.add_command_to_stack('bAdd', Book(book_id, book_name, author_name))
        except ValidationException as err:
            print(err)

    def ui_remove_book(self):
        try:
            book_ids = int(input("Enter book id:"))
        except ValueError:
            print("Invalid ID.")
            return
        ok = True
        book_list = self._book_repo.get_book_list()
        rental_list = self._rental_repo.get_list()
        for obj in rental_list:
            if obj.book_id == book_ids:
                ok = False
        operation_list = []
        if ok:
            for obj in book_list:
                if obj.book_id == book_ids:
                    try:
                        self._book_services.remove_book_service(book_ids)
                        operation_list.append(['bRemove', Book(book_ids, obj.title, obj.author)])
                        self._undo_service.add_command_to_stack('cascade', operation_list)
                    except ValidationException as err:
                        print(err)
        else:
            for obj in book_list:
                if obj.book_id == book_ids:
                    try:
                        operation_list = self._rental_services.return_a_book(book_ids)
                        self._book_services.remove_book_service(book_ids)
                        operation_list.append(['bRemove', Book(book_ids, obj.title, obj.author)])
                        self._undo_service.add_command_to_stack('cascade', operation_list)
                    except ValidationException as err:
                        print(err)

    def ui_update_book(self):
        try:
            book_id = int(input("Enter book id:"))
        except ValueError:
            print("Invalid ID.")
            return
        new_book_name = input("Enter new book name.")
        new_author_name = input("Enter new author name.")
        lists = self._book_repo.get_book_list()
        try:
            for obj in lists:
                if book_id == obj.book_id:
                    self._undo_service.add_command_to_stack("bUpdate", [book_id, obj.title, new_book_name, obj.author,
                                                                        new_author_name])
                    self._book_services.update_book_service(book_id, new_book_name, new_author_name)
        except ValidationException as err:
            print(err)

    def ui_list_books(self):
        for obj in self._book_repo.get_book_list():
            print(str(obj))

    def ui_add_a_client(self):
        try:
            client_id = int(input("Enter client id:"))
        except ValueError:
            print("Invalid ID.")
            return
        client_name = input("Enter client name:")
        try:
            self._client_services.add_client_service(client_id, client_name)
            self._undo_service.add_command_to_stack('cAdd', Client(client_id, client_name))
        except ValidationException as err:
            print(err)

    def ui_remove_a_client(self):
        try:
            client_ids = int(input("Enter client id:"))
        except ValueError:
            print("Invalid ID.")
            return
        ok = True
        client_list = self._client_repo.get_client_list()
        rental_list = self._rental_repo.get_list()
        for obj in rental_list:
            if obj.client_id == client_ids:
                ok = False
        operation_list = []
        if ok:
            for obj in client_list:
                if obj.client_id == client_ids:
                    try:
                        self._client_services.remove_client_service(client_ids)
                        operation_list.append(['cRemove', Client(client_ids, obj.client_name)])
                        self._undo_service.add_command_to_stack('cascade', operation_list)
                    except ValidationException as err:
                        print(err)
        else:
            for obj in client_list:
                if obj.client_id == client_ids:
                    try:
                        operation_list = self._rental_services.return_a_book_client(client_ids)
                        self._client_services.remove_client_service(client_ids)
                        operation_list.append(['cRemove', Client(client_ids, obj.client_name)])
                        self._undo_service.add_command_to_stack('cascade', operation_list)
                    except ValidationException as err:
                        print(err)

    def ui_update_a_client(self):
        try:
            client_id = int(input("Enter client id:"))
        except ValueError:
            print("Invalid ID.")
            return
        client_name = input("Enter client name:")
        lists = self._client_repo.get_client_list()
        try:
            for obj in lists:
                if client_id == obj.client_id:
                    self._undo_service.add_command_to_stack("cUpdate", [client_id, obj.client_name, client_name])
                    self._client_services.update_client_service(client_id, client_name)
        except ValidationException as err:
            print(err)
        try:
            self._client_services.update_client_service(client_id, client_name)
        except ValidationException as err:
            print(err)

    def ui_list_clients(self):
        for obj in self._client_repo.get_client_list():
            print(str(obj))

    def ui_rent_a_book(self):
        try:
            rental_id = int(input("Enter rental ID:"))
            book_id = int(input("Enter book ID:"))
            client_id = int(input("Enter client ID:"))
            start = int(input("Enter renting date:"))
            end = int(input("Enter returning date:"))
        except ValueError:
            print("Not valid.")
            return
        try:
            self._undo_service.add_command_to_stack("rent", [rental_id, book_id, client_id, start, end])
            self._rental_services.rent_a_book_service(rental_id, book_id, client_id, start, end)
        except ValidationException as err:
            print(err)

    def ui_return_book(self):
        try:
            book_ids = int(input("Enter book ID:"))
        except ValueError:
            print("Not an integer.")
            return
        try:
            lists = self._rental_repo.get_list()
            for obj in lists:
                if obj.book_id == book_ids:
                    self._undo_service.add_command_to_stack("return", [obj.rental_id, book_ids, obj.client_id,
                                                                       obj.rented_date, obj.returned_date])
                    self._rental_services.return_a_book(book_ids)
        except ValidationException as err:
            print(err)

    def ui_list_rentals(self):
        for obj in self._rental_repo.get_list():
            print(str(obj))

    def ui_search_book_by_author_or_title(self):
        user_input = input("Search for your book by author:")
        try:
            search = self._book_services.search_book_by_author_or_title_service(user_input)
            for obj in search:
                print(str(obj))
        except ValidationException as err:
            print(err)

    def ui_search_book_by_id(self):
        try:
            user_input = int(input("Search for your book by ID:"))
        except ValueError:
            print("Invalid ID.")
            return
        try:
            obj = self._book_services.search_book_by_id_service(user_input)
            print(obj)
        except ValidationException as err:
            print(err)

    def ui_search_client_name(self):
        try:
            user_input = input("Search for your client by name:")
        except ValueError:
            print("Invalid name input.")
            return
        try:
            search = self._client_services.search_client_name_service(user_input)
            for obj in search:
                print(str(obj))
        except ValidationException as err:
            print(err)

    def ui_search_client_by_id(self):
        try:
            user_input = int(input("Search for your client by ID:"))
        except ValueError:
            print("Invalid ID.")
            return
        try:
            obj = self._client_services.search_client_id_service(user_input)
            print(str(obj))
        except ValidationException as err:
            print(err)

    def ui_list_most_rented(self):
        for obj in self._rental_services.sort_desc_book():
            print("Book ID: " + str(obj[0]) + " rented " + str(obj[1]) + " times")

    def ui_list_most_active(self):
        for obj in self._rental_services.sort_desc_client():
            print("Client with the ID " + str(obj[0]) + " rented " + str(obj[1]) + " books")

    def ui_list_most_rented_author(self):
        self._rental_services.most_rented_author_service()

    def ui_undo_command(self):
        self._undo_service("undo")
        print("Undo operation went successfully!")

    def ui_redo_command(self):
        self._undo_service("redo")
        print("Redo operation went successfully!")

    def main(self):
        self._book_repo.add_twenty_books()
        self._client_repo.add_20_clients()
        self._rental_repo.add_twenty_rentals()
        while True:
            self.print_menu()
            command = input(">>>")
            if command == '1':
                self.ui_add_book()
            elif command == '2':
                self.ui_remove_book()
            elif command == '3':
                self.ui_update_book()
            elif command == '4':
                self.ui_list_books()
            elif command == '5':
                self.ui_search_book_by_author_or_title()
            elif command == '6':
                self.ui_search_book_by_id()
            elif command == '7':
                self.ui_add_a_client()
            elif command == '8':
                self.ui_remove_a_client()
            elif command == '9':
                self.ui_update_a_client()
            elif command == '10':
                self.ui_list_clients()
            elif command == '11':
                self.ui_search_client_by_id()
            elif command == '12':
                self.ui_search_client_name()
            elif command == '13':
                self.ui_rent_a_book()
            elif command == '14':
                self.ui_return_book()
            elif command == '15':
                self.ui_list_rentals()
            elif command == '16':
                self.ui_list_most_rented()
            elif command == '17':
                self.ui_list_most_active()
            elif command == '18':
                self.ui_list_most_rented_author()
            elif command == '19':
                try:
                    self.ui_undo_command()
                except ServiceError as err:
                    print(err)
            elif command == '20':
                try:
                    self.ui_redo_command()
                except ServiceError as err:
                    print(err)
            elif command == '21':
                return


ui = UserInterface()
ui.main()
