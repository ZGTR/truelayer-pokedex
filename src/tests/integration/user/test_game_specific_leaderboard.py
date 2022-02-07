from src.tests.integration.integration_base_test import IntegrationBaseTest

class GameSpecificLeaderboardTest(IntegrationBaseTest):
    path = "/v1/user/game-specific-leaderboard"

    data_sources = ['integration/game-specific-leaderboard-users', 'integration/user/game-session-log/game-sessions-in-game-leaderboard']

    def test_getGameSpecificLeaderboard(self):

        request_body = dict(
            game_type="PacMan"
        )

        response = self.app.get(self.path, headers=self.get_authorization_header("1"), json=request_body)
        game_sessions = response.json["leaderboard_data"]

        self.assertTrue(valuesAreDescending(game_sessions, "score"))
        self.assertStatusCode(response, 200)


def valuesAreDescending(orderedList, field):
    prevValue = orderedList[0]

    for item in orderedList:
        if item == orderedList[0]: # skip first run
            continue
        
        if item[field] > prevValue[field]: # if current item value is greater than previous, items are not descending
            return False

        prevValue = item
    return True
