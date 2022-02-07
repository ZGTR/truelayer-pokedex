from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection

from src.bootstrap_stages.stage02.ddb_constants import DDbConstants
from src.models.base import BaseModel, BaseGlobalSecondaryIndex


class ClientIdIndex(BaseGlobalSecondaryIndex):
    class Meta:
        index_name = DDbConstants.NAME_GSI_CLIENTS_CLIENT_ID
        table_name = DDbConstants.NAME_TABLE_CLIENTS
        projection = AllProjection()
        host = DDbConstants.DB_HOST
        region = DDbConstants.DB_REGION
        read_capacity_units = 1
        write_capacity_units = 1

    client_id = UnicodeAttribute(hash_key=True)


class ApiClientModel(BaseModel):
    class Meta:
        table_name = DDbConstants.NAME_TABLE_CLIENTS
        host = DDbConstants.DB_HOST
        region = DDbConstants.DB_REGION
        read_capacity_units = 1
        write_capacity_units = 1

    id = UnicodeAttribute(hash_key=True)
    client_id = UnicodeAttribute()
    client_secret = UnicodeAttribute()

    client_id_index = ClientIdIndex()

    @classmethod
    def get_by_client_data(cls, client_id, client_secret):
        return cls.client_id_index.query_page(
            hash_key=client_id,
            filter_condition=(cls.client_secret == client_secret)
        ).first()
