
class ExceptionPokeApiError (Exception):
    MESSAGE = 'An error happened while calling pokeapi.co'

    def __str__(self):
        return MESSAGE

    def __init__(self, message=MESSAGE):
        super().__init__(message)
