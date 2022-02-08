
class ExceptionApiTranslationTooManyRequests (Exception):
    MESSAGE = 'Too many requests within 1 hour for the translation API. Please check their docs.'

    def __str__(self):
        return self.MESSAGE

    def __init__(self, message=MESSAGE):
        super().__init__(message)
