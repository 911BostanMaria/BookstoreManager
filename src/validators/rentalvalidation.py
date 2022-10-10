from src.domain.rental import Rental
from src.validators.validationexception import ValidationException


class RentalValidator:
    @staticmethod
    def validate(rental):
        errors = []
        if isinstance(rental, Rental) is False:
            errors.append("Not a valid rental.")
        if int(rental.rental_id) < 1:
            errors.append('Not a valid rental ID.')
        if int(rental.book_id) < 1:
            errors.append('Not a valid book ID.')
        if int(rental.client_id) < 1:
            errors.append('Not a valid client ID.')
        if rental.rented_date > rental.returned_date:
            errors.append('Not a valid date input.')
        if rental.rented_date < 1 or rental.rented_date > 30 or rental.returned_date < 1 or rental.returned_date > 30:
            errors.append('Not ok!')
        if len(errors) > 0:
            raise ValidationException(errors)

    @staticmethod
    def validate_return(id_returned):
        errors = []
        if id_returned < 0:
            errors.append('Not a valid ID.')
        if len(errors) > 0:
            raise ValidationException(errors)
