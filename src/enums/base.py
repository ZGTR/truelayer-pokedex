from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def values(cls):
        values = []
        for item in cls:
            values.append(item.value)

        return values

    @classmethod
    def names(cls):
        names = []
        for item in cls:
            names.append(item.name)

        return names

    @classmethod
    def as_list(cls):
        items = []
        for item in cls:
            items.append(item)

        return items
