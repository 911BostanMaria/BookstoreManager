class ValidationException(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        errors = ""
        for obj in self._message:
            errors = errors + obj
            errors = errors + '\n'
        return errors
