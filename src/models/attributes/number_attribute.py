from src.models.attributes import CoreAttribute


class NumberAttribute(CoreAttribute):
    """
    Due to bug in PynamoDB, we need to override this attribute
    https://github.com/pynamodb/PynamoDB/issues/627
    """

    def deserialize(self, value):
        if self.null is True and value is None:
            return None
        return super().deserialize(value)
