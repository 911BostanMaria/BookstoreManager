from src.validators.validationexception import ValidationException


class ClientValidator:
    @staticmethod
    def validate(client):
        errors = []
        if client.client_id < 0 or not float(client.client_id) == int(client.client_id):
            errors.append("Invalid ID!")
        if client.client_name == "":
            errors.append("Invalid name!")
        if len(errors) > 0:
            raise ValidationException(errors)

    @staticmethod
    def validate_client_id(client_id):
        errors = []
        if client_id < 0 or not float(client_id) == int(client_id):
            errors.append("Invalid ID!")
        if len(errors) > 0:
            raise ValidationException(errors)

    @staticmethod
    def validate_client_name(client_name):
        errors = []
        if client_name == "":
            errors.append("Invalid name!")
        if len(errors) > 0:
            raise ValidationException(errors)
