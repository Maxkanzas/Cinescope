import pytest
import requests
from api.api_manager import ApiManager


class TestAuthAPI:

    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        print(response_data)

        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        # assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_login_invalid_password(self, api_manager: ApiManager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": "kdsjfalk;jdf0239"
        }
        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()
        assert "message" in response_data, "В ответе отсутствует message"
        assert "error" in response_data, "В ответе отсутствует error"
        assert "statusCode" in response_data, "В ответе отсутствует statusCode"

    def test_login_invalid_email(self, api_manager: ApiManager, registered_user):
        login_data = {
            "email": "nonexistent@email.com",
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data, expected_status=500)
        response_data = response.json()
        assert "message" in response_data, "В ответе отсутствует message"
        assert "statusCode" in response_data, "В ответе отсутствует statusCode"
        assert response_data["statusCode"] == 500
        assert response_data["message"] == "Internal server error"

    def test_login_empty_body(self, api_manager: ApiManager):
        login_data = None
        response = api_manager.auth_api.login_user(login_data, expected_status=500)
        response_data = response.json()
        assert "message" in response_data, "В ответе отсутствует message"
        assert "statusCode" in response_data, "В ответе отсутствует statusCode"
        assert response_data["statusCode"] == 500
        assert response_data["message"] == "Internal server error"

    def test_create_user_method_exists(self, api_manager: ApiManager):
        """
        Простейшая проверка: метод существует и возвращает response.
        """
        # Минимальные данные (могут быть невалидными)
        dummy_data = {"email": "test@test.com"}

        # Просто вызываем метод, чтобы убедиться, что он не падает
        response = api_manager.user_api.create_user(dummy_data)

        # Даже не проверяем статус, просто убеждаемся, что это Response
        assert response is not None
        assert hasattr(response, "status_code")