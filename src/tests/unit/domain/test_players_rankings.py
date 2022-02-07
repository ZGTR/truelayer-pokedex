from src.helpers.date_helper import get_yesterday
from src.models.user import UserModel
from src.domain.players_rankings import PlayersRankings
from src.tests.base_test import BaseTest
from unittest import mock

class TestPlayersRankings(BaseTest):

    @mock.patch("src.models.UserModel.get_users_allowed_response")
    def test_get_today_ranking_response_for_user(self, getUsersMock):
        fakeUserId = "372046ea999311e9a80deebee6457737"

        # config mocks
        userModel = UserModel()
        userModel.id = fakeUserId
        userModel.username = "fakeUsername"
        userModel.last_login = get_yesterday()
        userModel.user_type = "PatientBasic"
        userModel.firstname = "fakeUserFirstName"
        userModel.lastname = "fakeUserLastName"
        userModel.impaired_hand = "Left"


        getUsersMock.return_value = [
            userModel
        ]

        PlayersRankings().populate_leaderboard_table_from_sessions()

        user_ranking = PlayersRankings().get_today_ranking_digest_for_user(fakeUserId)

        self.assertIsNotNone(user_ranking)