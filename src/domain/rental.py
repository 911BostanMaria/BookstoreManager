from datetime import date


class Rental:
    def __init__(self, rental_id, book_id, client_id, rented_date, returned_date):
        self._rental_id = rental_id
        self._book_id = book_id
        self._client_id = client_id
        self._rented_date = rented_date
        self._returned_date = returned_date

    @property
    def rental_id(self):
        return self._rental_id

    @rental_id.setter
    def rental_id(self, new_id):
        self._rental_id = new_id

    @property
    def book_id(self):
        return self._book_id

    @property
    def client_id(self):
        return self._client_id

    @property
    def rented_date(self):
        return self._rented_date

    @rented_date.setter
    def rented_date(self, start):
        self._rented_date = start

    @property
    def returned_date(self):
        return self._returned_date

    @returned_date.setter
    def returned_date(self, end):
        self._returned_date = end

    def __len__(self):
        # Returns len of the rental.
        if self._returned_date is not None:
            return (self._returned_date - self._rented_date).days + 1
        today = date.today()
        return (today - self._rented_date).days + 1

    def __str__(self):
        return "Rental: " + str(self._rental_id) + "\nBook: " + str(self._book_id) + "\nClient: " + str(
            self._client_id) + ' Period: ' + str(self._rented_date) + ' December to ' + str(self.returned_date) +\
               ' December'
