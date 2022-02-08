import dataclasses
import decimal
import json
from datetime import datetime, date

from flask_babel import LazyString
from src.models import BaseModel


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, BaseModel):
            return o.as_dict()
        if isinstance(o, MapAttribute):
            return o.as_dict()
        if isinstance(o, LazyString):
            return str(o)
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, Collection):
            return o.serialize()
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return super().default(o)
