from typing import Optional, List

from pynamodb import attributes
from pynamodb.expressions.condition import Condition
from pynamodb.indexes import GlobalSecondaryIndex
from pynamodb.models import Model

from src.bootstrap_stages.stage02.ddb_constants import DDbConstants
from src.core.models.collection import Collection
from src.helpers.utils import Utils
from src.models.attributes.utc_date_time_attribute import UTCDateTimeAttribute


class BaseQueryable:
    @classmethod
    def query_page(cls,
                   hash_key,
                   range_key_condition=None,
                   filter_condition=None,
                   scan_index_forward=None,
                   consistent_read=False,
                   limit=None,
                   last_evaluated_key=None,
                   attributes_to_get=None,
                   **filters):
        items = cls.query(
            hash_key,
            range_key_condition,
            filter_condition,
            scan_index_forward,
            consistent_read,
            limit,
            last_evaluated_key,
            attributes_to_get,
            **filters)
        return Collection(list(items))

    @classmethod
    def query_pages(cls,
                    hash_key,
                    range_key_condition=None,
                    filter_condition=None,
                    scan_index_forward=None,
                    consistent_read=False,
                    limit=None,
                    last_evaluated_key=None,
                    attributes_to_get=None,
                    **filters):

        all_items = Collection([])
        while True:

            batch = cls.query(
                hash_key,
                range_key_condition,
                filter_condition,
                scan_index_forward,
                consistent_read,
                limit - all_items.length() if limit is not None else limit,
                last_evaluated_key,
                attributes_to_get,
                **filters)

            last_evaluated_key = batch.last_evaluated_key

            all_items += Collection(list(batch)[:limit]) if limit is not None else Collection(list(batch))

            if limit is not None and all_items.length() == limit:
                break

            if last_evaluated_key is None:
                break

        return all_items


class BaseGlobalSecondaryIndex(GlobalSecondaryIndex, BaseQueryable):
    pass


class BaseModel(Model, BaseQueryable):
    class Meta:
        table_name = None

    @classmethod
    def get_or_none(cls,
                    hash_key,
                    range_key=None,
                    consistent_read=False,
                    attributes_to_get=None):
        try:
            return cls.get(hash_key=hash_key, range_key=range_key, consistent_read=consistent_read,
                           attributes_to_get=attributes_to_get)
        except:
            return None

    @classmethod
    def get_all(cls, filter_condition: Optional[Condition] = None, attributes_to_get=None) -> Collection:
        all_items = Collection([])
        last_evaluated_key = None

        while True:
            batch = cls.scan(filter_condition=filter_condition, last_evaluated_key=last_evaluated_key,
                            attributes_to_get=attributes_to_get)
            last_evaluated_key = batch.last_evaluated_key

            all_items += Collection(list(batch))
            if last_evaluated_key is None:
                break

        return all_items

    @classmethod
    def batch_insert(cls, records: List[Model]):
        all_items = []
        for chunk in Utils.chunks(records, DDbConstants.MAX_MIGRATION_CHUNK):
            with cls.batch_write() as batch:
                items = [cls(**record) for record in chunk]
                for item in items:
                    batch.save(item)
                all_items += items
        return all_items

    @staticmethod
    def batch_delete(data: List[Model]):
        """
        delete all the data from the database
        :param data: the data to be deleted
        """
        model = data[0]
        for chunk in Utils.chunks(data, DDbConstants.MAX_MIGRATION_CHUNK):
            with model.batch_write() as batch:
                for item in chunk:
                    batch.delete(item)

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            if isinstance(attr, attributes.MapAttribute):
                if getattr(self, name):
                    yield name, getattr(self, name).as_dict()
            elif isinstance(attr, attributes.UTCDateTimeAttribute):
                if getattr(self, name):
                    yield name, attr.serialize(getattr(self, name))

            elif isinstance(attr, UTCDateTimeAttribute):
                if getattr(self, name):
                    yield name, attr.serialize(getattr(self, name))
            elif isinstance(attr, attributes.ListAttribute):
                if getattr(self, name):
                    yield name, getattr(self, name)
                    # yield name, attr.serialize(getattr(self, name))

            elif isinstance(attr, attributes.NumberAttribute):
                # if numeric return value as is.
                yield name, getattr(self, name)
            elif getattr(self, name) is None:
                pass
            else:
                yield name, attr.serialize(getattr(self, name))

    def as_dict(self):
        return dict(self)

    @classmethod
    def batch_get(cls, items, consistent_read=None, attributes_to_get=None) -> Collection:
        return Collection(list(super().batch_get(items, consistent_read, attributes_to_get)))

    @classmethod
    def from_dict(cls, raw):
        item = Utils.dict_to_dynamodb_item(raw)['M']
        return cls.from_raw_data(item)

    def __getitem__(self, item):
        return self.__getattribute__(item)
