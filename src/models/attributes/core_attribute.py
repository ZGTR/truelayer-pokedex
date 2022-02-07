

class CoreAttribute:

    def __init__(self,
                 enum,
                 hash_key=False,
                 range_key=False,
                 null=None,
                 default=None,
                 default_for_new=None,
                 attr_name=None):
        self._enum = enum
        self._enum_values = self._enum.values()