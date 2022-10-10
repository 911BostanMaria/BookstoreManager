from src.repository.client_repo import Client
from src.validators.validationexception import ValidationException

class ClientServices:
    def __init__(self, clients, validator):
        self._clients = clients
        self._validator = validator

    def add_client_service(self, id_client, name_client):
        """
        Updates client list using client validators and client repository.
        """
        client = Client(id_client, name_client)
        self._validator.validate(client)
        self._clients.add_a_client(client)

    def remove_client_service(self, client_to_remove):
        """
        Removes client using client repository.
        """
        self._validator.validate_client_id(client_to_remove)
        self._clients.remove_client(client_to_remove)

    def update_client_service(self, initial, client_name):
        """
        Updates client using book validators and book repository.
        """
        self._validator.validate_client_id(initial)
        self._validator.validate_client_name(client_name)
        self._clients.update_client(initial, client_name)

    def search_client_id_service(self, user_input):
        if str(user_input) == "":
            raise ValidationException(["Cannot be an empty string."])
        return self._clients.search_client_id(user_input)

    def search_client_name_service(self, user_input):
        if str(user_input) == "":
            raise ValidationException(["Cannot be an empty string."])
        return self._clients.search_client_name(user_input)
