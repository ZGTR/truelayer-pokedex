from typing import Optional, List

class BaseModel:
    class Meta:
        table_name = None

    def as_dict(self):
        return dict(self)

    @classmethod
    def from_dict(cls, raw):
        item = Utils.dict_to_dynamodb_item(raw)['M']
        return cls.from_raw_data(item)

    def __getitem__(self, item):
        return self.__getattribute__(item)
