from src.validators.validationexception import ValidationException


class BookValidator:
    @staticmethod
    def validate(book):
        errors = []
        if book.book_id < 0 or not float(book.book_id) == int(book.book_id):
            errors.append("Invalid ID!")
        if book.title == "":
            errors.append("Invalid title!")
        if book.author == "" :
            errors.append("Invalid author!")
        if len(errors) > 0:
            raise ValidationException(errors)

    @staticmethod
    def validate_id(book_id):
        errors = []
        if int(book_id) < 0 or not float(book_id) == int(book_id):
            errors.append("Not a valid ID.")
        if len(errors) > 0:
            raise ValidationException(errors)

    @staticmethod
    def validate_title(book_title):
        errors = []
        if book_title == "":
            errors.append("Invalid title!")
        if len(errors) > 0:
            raise ValidationException(errors)

    @staticmethod
    def validate_author(book_author):
        errors = []
        if book_author == "":
            errors.append("Invalid author!")
        if len(errors) > 0:
            raise ValidationException(errors)
