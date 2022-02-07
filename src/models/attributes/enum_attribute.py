from enum import Enum

from src.models.attributes import CoreAttribute


class EnumUnicodeAttribute(CoreAttribute):
    """
    An enumerated unicode attribute
    this is a wrapper attribute
    it just throws exception if the value is not in the allowed values
    """

    def __init__(self,
                 enum,
                 hash_key=False,
                 range_key=False,
                 null=None,
                 default=None,
                 default_for_new=None,
                 attr_name=None):
        super().__init__(hash_key, range_key, null, default, default_for_new, attr_name)
        self._enum = enum
        self._enum_values = self._enum.values()

    def serialize(self, value):
        """ Raises ValueError if input value not in ENUM, otherwise continues as parent class """
        if isinstance(value, Enum):
            value = value.value

        if type(value) is str and value not in self._enum_values:
            raise ValueError(f"{self.attr_name} must be one of {self._enum_values}, not '{value}'")

        return UnicodeAttribute.serialize(self, value)
