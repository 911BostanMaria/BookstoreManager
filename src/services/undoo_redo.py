from src.validators.serviceerrors import ServiceError
"""
Undo/Redo service class
This takes care of the undo/redo functionality
Functions that need to be able to undo/redo:
    -Add, remove, update books/clients
    -Rent/return a book
"""


class UndoRedo:
    def __init__(self, book_service, client_service, rental_service):
        self._bookService = book_service
        self._clientService = client_service
        self._rentalService = rental_service

        self._commandStackTop = -1
        self._commandStack = []

        self.__undoDict = {
             "bAdd": self.undo_add_book,
             "bRemove": self.undo_remove_book,
             "bUpdate": self.undo_update_book,
             "cAdd": self.undo_add_client,
             "cRemove": self.undo_remove_client,
             "cUpdate": self.undo_update_client,
              "rent": self.undo_rent_book,
             "return": self.undo_return_book,
             "cascade": self.undo_cascade_remove,
        }

        self.__redoDict = {
             "bAdd": self.redo_add_book,
             "bRemove": self.redo_remove_book,
             "bUpdate": self.redo_update_book,
             "cAdd": self.redo_add_client,
             "cRemove": self.redo_remove_client,
             "cUpdate": self.redo_update_client,
              "rent": self.redo_rent_book,
             "return": self.redo_return_book,
            "cascade": self.redo_cascade_remove,
        }

    def add_command_to_stack(self, action, obj):
        self._commandStackTop += 1
        self._commandStack.insert(self._commandStackTop, [action, obj])
        del self._commandStack[self._commandStackTop+1:]

    def get_last_operation(self):
        operation = self._commandStack[self._commandStackTop]
        self._commandStackTop -= 1
        return operation

    def get_last_operation_command(self, operation):
        return operation[0]

    def get_last_operation_obj(self, operation):
        return operation[1]

    def get_next_operation(self):
        operation = self._commandStack[self._commandStackTop + 1]
        self._commandStackTop += 1
        return operation

    def __call__(self, option):
        if option == "undo":
            if self._commandStackTop == -1:
                raise ServiceError(["There is nothing to undo."])
            last_operation = self.get_last_operation()
            action = self.get_last_operation_command(last_operation)
            obj = self.get_last_operation_obj(last_operation)
            self.__undoDict[action](obj)
        elif option == "redo":
            if self._commandStackTop == len(self._commandStack) - 1:
                raise ServiceError(["There is nothing to redo."])
            next_operation = self.get_next_operation()
            action = self.get_last_operation_command(next_operation)
            obj = self.get_last_operation_obj(next_operation)
            self.__redoDict[action](obj)

    """
    UNDO FUNCTIONALITIES. <3
    """
    def undo_add_book(self, book):
        self._bookService.remove_book_service(book.book_id)

    def undo_remove_book(self, book):
        self._bookService.add_book_service(book.book_id, book.title, book.author)

    def undo_cascade_remove(self, operations):
        new_operations = operations[:]
        while len(new_operations) > 0:
            operation = new_operations.pop()
            action = self.get_last_operation_command(operation)
            obj = self.get_last_operation_obj(operation)
            self.__undoDict[action](obj)

    def undo_update_book(self, book):
        self._bookService.update_book_service(book[0], book[1], book[3])

    def undo_add_client(self, client):
        self._clientService.remove_client_service(client.client_id)

    def undo_remove_client(self, client):
        self._clientService.add_client_service(client.client_id, client.client_name)

    def undo_update_client(self, client):
        self._clientService.update_client_service(client[0], client[1])

    def undo_rent_book(self, rental):
        self._rentalService.return_a_book(rental[1])

    def undo_return_book(self, rental):
        self._rentalService.rent_a_book_service(rental[0], rental[1], rental[2], rental[3], rental[4])


    """
    REDO FUNCTIONALITIES. >:(
    """
    def redo_add_book(self, book):
        self._bookService.add_book_service(book.book_id, book.title, book.author)

    def redo_update_book(self, book):
        self._bookService.update_book_service(book[0], book[2], book[4])

    def redo_add_client(self, client):
        self._clientService.add_client_service(client.client_id, client.client_name)

    def redo_remove_client(self, client):
        self._clientService.remove_client_service(client.client_id)

    def redo_update_client(self, client):
        self._clientService.update_client_service(client[0], client[2])

    def redo_rent_book(self, rental):
        self._rentalService.rent_a_book_service(rental[0], rental[1], rental[2], rental[3], rental[4])

    def redo_return_book(self, rental):
        self._rentalService.return_a_book(rental[1])

    def redo_remove_book(self, book):
        self._bookService.remove_book_service(book.book_id)

    def redo_cascade_remove(self, operations):
        for item in operations:
            action = self.get_last_operation_command(item)
            obj = self.get_last_operation_obj(item)
            self.__redoDict[action](obj)
