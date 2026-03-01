from requests import Response

from constants import USER_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    """
    Класс для работы с пользователями.
    """
    def __init__(self, session):
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru/")

    def create_user(self, user_data, expected_status=201, need_logging=True)-> Response:
        return self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def get_user(self, user_id, expected_status=200):
        """
        Получение информации о пользователе.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )

    def update_user(self, user_id, user_data, expected_status=200):
        """
        Обновление данных пользователя.
        """
        return self.send_request(
            method="PUT",
            endpoint=f"/users/{user_id}",
            data=user_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Удаление пользователя.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )