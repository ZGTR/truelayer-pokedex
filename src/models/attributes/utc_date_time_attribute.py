from dateutil.tz import tzutc
from src.models.attributes import CoreAttribute


class UTCDateTimeAttribute(CoreAttribute):
    def serialize(self, value):
        if isinstance(value, str):
            value = self.parse_string(value)

        return super().serialize(value)

    def deserialize(self, value):
        value = super().deserialize(value)
        if value.tzinfo is None:
            value = value.replace(tzinfo=tzutc())

        return value

    def parse_string(self, value):
        return self.deserialize(value)
