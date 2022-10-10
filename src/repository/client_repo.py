from src.domain.client import Client
import random
from src.validators.validationexception import ValidationException


class ClientRepository:
    def __init__(self):
        self._clients = []

    def get_client_list(self):
        return self._clients

    def add_20_clients(self):
        """
        :return: Adds twenty randomly generated clients to the client list.
        """
        name = ['Maria', 'Andrei', 'Andreea', 'Clara', 'Rares', 'Mihai', 'Denis', 'Dan', 'Erica']
        for i in range(1, 21, 1):
            self._clients.append(Client(i, random.choice(name)))

    def add_a_client(self, new_client):
        """
        :param new_client: New client to be added, must be given name and ID.
        :return: None. Appends client to the list.
        """
        if self.find_by_id(new_client.client_id) is False:
            self._clients.append(new_client)
        else:
            raise ValidationException(["Existing ID."])

    def find_by_id(self, given_id):
        """
        :param given_id: The ID of the client we want to find in the client list.
        :return: Returns the client if found, otherwise returns false.
        """
        for everyone in self._clients:
            if everyone.client_id == given_id:
                return True
        return False

    def remove_client(self, client_id):
        """
        :param client_id: The ID of the CLIENT we want to delete from the book list.
        :return: None. Deletes book from client list.
        """
        if self.find_by_id(client_id) is False:
            raise ValidationException(["Not an existing ID."])
        for obj in self._clients:
            if client_id == obj.client_id:
                self._clients.remove(obj)

    def update_client(self, client_id, client_name):
        """
        :param client_id:
        :param client_name:
        :return:
        """
        if self.find_by_id(client_id) is False:
            raise ValidationException("Not an existing ID.")
        for everyone in self._clients:
            if everyone.client_id == client_id:
                everyone.client_name = client_name

    def print_all_clients(self):
        """
        :return: Prints all clients in the client list.
        """
        for everyone in self._clients:
            print(str(everyone))

    def search_client_id(self, user_input):
        """
        :param user_input: The string we want to search for in the list of clients.
        :return: Prints all the objects containing the string.
        """
        if str(user_input).isnumeric():
            for obj in self._clients:
                if obj.client_id == user_input:
                    return obj

    def search_client_name(self, user_input):
        search_list = []
        if not str(user_input).isnumeric():
            user_input = user_input.lower()
            for obj in self._clients:
                name = obj.client_name
                name = name.split(" ")
                for i in range(0, len(name), 1):
                    name[i] = name[i].lower()
                    if name[i].find(user_input) > -1:
                        search_list.append(obj)
        return search_list
