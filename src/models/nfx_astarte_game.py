from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute
from pynamodb.indexes import AllProjection

from src.bootstrap_stages.stage02.ddb_constants import DDbConstants
from src.enums.game_type import GameType
from src.helpers.utils import Utils
from src.models import EnumUnicodeAttribute, BaseGlobalSecondaryIndex
from src.models.base import BaseModel


class NfxAstarteGameModel(BaseModel):
    class Meta:
        table_name = DDbConstants.NAME_TABLE_NFX_ASTARTE_GAMES
        host = DDbConstants.DB_HOST
        region = DDbConstants.DB_REGION
        read_capacity_units = 1
        write_capacity_units = 1

    id = UnicodeAttribute(hash_key=True, default_for_new=lambda: Utils.get_random_id())
    game_type = EnumUnicodeAttribute(GameType)
    active = BooleanAttribute()
    order = NumberAttribute()
    instruction_video_url = UnicodeAttribute(null=True)
    title = UnicodeAttribute(null=True)
    subtitle = UnicodeAttribute(null=True)
    description = UnicodeAttribute(null=True)

    @classmethod
    def get_all_temp_fix_for_home_v1(cls):
        items = cls.get_all(NfxAstarteGameModel.active == True).serialize()

        # Temp fix for the current client.
        for item in items:
            item['id'] = int(item['id'])

        return items
