from __future__ import annotations

from flask_jwt_extended import current_user
from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.indexes import IncludeProjection

from src.bootstrap_stages.stage00.logger_setup import logger
from src.bootstrap_stages.stage02.ddb_constants import DDbConstants
from src.enums import Country
from src.enums.impaird_hand import ImpairedHand
from src.enums.user_type import UserType
from src.helpers import date_helper
from src.helpers.utils import Utils
from src.models.attributes.email_attribute import EmailAttribute
from src.models.attributes.enum_attribute import EnumUnicodeAttribute
from src.models.attributes.utc_date_time_attribute import UTCDateTimeAttribute
from src.models.base import BaseModel, BaseGlobalSecondaryIndex


class UsernameIndex(BaseGlobalSecondaryIndex):
    class Meta:
        index_name = DDbConstants.NAME_GSI_USERS_USERNAME
        table_name = DDbConstants.NAME_TABLE_USERS
        projection = IncludeProjection(['password', 'id'])
        host = DDbConstants.DB_HOST
        region = DDbConstants.DB_REGION
        read_capacity_units = 1
        write_capacity_units = 1

    username = UnicodeAttribute(hash_key=True)


class UserModel(BaseModel):
    class Meta:
        table_name = DDbConstants.NAME_TABLE_USERS
        host = DDbConstants.DB_HOST
        region = DDbConstants.DB_REGION
        read_capacity_units = 1
        write_capacity_units = 1

    id = UnicodeAttribute(hash_key=True, default_for_new=lambda: Utils.get_random_id())
    username_index = UsernameIndex()
    username = UnicodeAttribute()
    last_login = UTCDateTimeAttribute(null=True, default=None)
    creation_date = UTCDateTimeAttribute(null=False, default_for_new=lambda: date_helper.get_now())
    email = EmailAttribute()
    user_type = EnumUnicodeAttribute(UserType, default_for_new=lambda: UserType.PATIENT_BASIC)
    password = UnicodeAttribute()
    firstname = UnicodeAttribute()
    lastname = UnicodeAttribute()
    impaired_hand = EnumUnicodeAttribute(ImpairedHand, null=True, default_for_new=lambda: ImpairedHand.NONE)
    country = EnumUnicodeAttribute(Country, null=True, default=Country.UK.value)
    utc_offset_mins = NumberAttribute(null=False, default=0)

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def update_last_login(self):
        try:
            self.update(
                actions=[
                    UserModel.last_login.set(date_helper.get_now(self.utc_offset_mins))
                ]
            )

            return True, ''
        except Exception as ex:
            logger.error(ex.args[0])
            return False, ex.args[0]

    @classmethod
    def get_users_allowed_response(cls):
        return cls.get_all(
            attributes_to_get=[
                "id",
                "username",
                "last_login",
                "user_type",
                "firstname",
                "lastname",
                "impaired_hand"
            ])

    @classmethod
    def set_impaired_hand(cls, impaired_hand):
        try:
            current_user.update([
                UserModel.impaired_hand.set(impaired_hand)
            ])
            return True, ''
        except Exception as ex:
            logger.error(ex.args[0])
            return False, ex.args[0]
