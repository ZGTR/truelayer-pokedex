from src.models.base import BaseModel

class ApiClientModel(BaseModel):
    @classmethod
    def get_by_client_data(cls, client_id, client_secret):
        # Normally we get this from the DB. For now, we'll simply hard code it here or in the config.
        return dict(
            id = 1,
            client_id = "123",
            client_secret = "123"
        )