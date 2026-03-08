from constants.endpoints import USER_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class UserApi(CustomRequester):

    def __init__(self, session):
        self.session = session
        super().__init__(session, base_url="https://auth.dev-cinescope.coconutqa.ru")

    def get_user(self, user_locator, expected_status=200):
        return self.send_request(
            "GET",
            f"{USER_ENDPOINT}/{user_locator}",
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def changed_user_data(self, user_id, changed_data, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            data=changed_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            data=None,
            expected_status=expected_status
        )