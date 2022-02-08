
class ExceptionPokeApiError (Exception):
    MESSAGE = 'An error occurred while calling pokeapi.co.'

    def __str__(self):
        return self.MESSAGE

    def __init__(self, message=MESSAGE):
        super().__init__(message)
