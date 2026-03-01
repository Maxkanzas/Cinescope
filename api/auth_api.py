from custom_requester.custom_requester import CustomRequester
from constants import LOGIN_ENDPOINT, USER_ENDPOINT, REGISTER_ENDPOINT


class AuthAPI(CustomRequester):
    """
      Класс для работы с аутентификацией.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru")

    def login_user(self, login_data, expected_status=201):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user_creds):
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self._update_session_headers(**{"authorization": "Bearer " + token})

    def create_user(self, data_user: dict, expected_status=201, need_logging=True):
        return self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=data_user,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def register_user(self, user_data: dict, expected_status=201, need_logging=True):
        """
        Регистрация нового пользователя (публичный эндпоинт).
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
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