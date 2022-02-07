from unittest.mock import patch

from src.tests.integration.integration_base_test import IntegrationBaseTest


# class AdminNfxAstarteGameTest(IntegrationBaseTest):
#     path = "/admin/v1/nfx-astarte-game"
#
#     data_sources = ['integration/admin/nfx-astarte-game']
#
#     @patch('uuid.uuid1')
#     def test_createGame_success(self, uuid):
#         uuid.return_value.hex = '123'
#
#         data = dict(
#             game_type="Musical",
#             active=False,
#             order=2,
#         )
#         response = self.app.post(self.path, json=data)
#
#         actual_response = response.get_json()
#         expected_response = dict(
#             success=True,
#             item=dict(
#                 **data,
#                 id="123"
#             )
#         )
#
#         self.assertStatusCode(response, 200)
#         self.assertEqual(expected_response, actual_response)
#
#     def test_deleteGame_foundAndDeleted(self):
#         game_id = "987654321"
#         response = self.app.delete(self.path + '/' + game_id)
#
#         self.assertStatusCode(response, 204)
#
#         response = self.app.delete(self.path + '/' + game_id)
#         self.assertStatusCode(response, 404)
