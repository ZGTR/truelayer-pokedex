
class ExceptionPokemonDoesNotExists (Exception):
    MESSAGE = 'Can not find a pokemon with this name'

    def __str__(self):
        return MESSAGE

    def __init__(self, message=MESSAGE):
        super().__init__(message)


