import pytest
import requests
from api.api_manager import ApiManager
from schemas import RegisterUserResponse, LoginUserResponse, ErrorResponse, RefreshTokenResponse


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        response = api_manager.auth_api.register_user(user_data=test_user.model_dump())
        response_data = RegisterUserResponse(**response.json())
        assert response_data.email == test_user.email, "Email не совпадает"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        login_data = {
            "email": registered_user.email,
            "password": registered_user.password
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = LoginUserResponse(**response.json())
        assert response_data.accessToken is not None, "Токен доступа отсутствует в ответе"
        assert response_data.accessToken != "", "Токен не должен быть пустым"

    def test_login_invalid_password(self, api_manager: ApiManager, registered_user):
        login_data = {
            "email": registered_user.email,
            "password": "kdsjfalk;jdf0239"
        }
        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        error_data = ErrorResponse(**response.json())
        assert error_data.message == "Неверный логин или пароль"
        assert error_data.error == "Unauthorized"

    def test_login_invalid_email(self, api_manager: ApiManager, registered_user):
        login_data = {
            "email": 123,
            "password": registered_user.password
        }
        response = api_manager.auth_api.login_user(login_data, expected_status=500)
        error_data = ErrorResponse(**response.json())
        assert error_data.message == "Internal server error"

    def test_login_empty_body(self, api_manager: ApiManager):
        login_data = None
        response = api_manager.auth_api.login_user(login_data, expected_status=500)
        error_data = ErrorResponse(**response.json())
        assert error_data.message == "Internal server error"

    def test_logout(self, api_manager: ApiManager):
        response = api_manager.auth_api.logout()
        assert response.status_code == 200

    @pytest.mark.parametrize("user_role, expected_status", [
        ("common_super_admin", 201),
        ("common_admin", 201),
        ("common_user", 201)
    ], ids=[
        "Refresh token as SUPER_ADMIN",
        "Refresh token as ADMIN",
        "Refresh token as USER"
    ])
    def test_refresh_token(self, request, user_role, expected_status):
        user = request.getfixturevalue(user_role)
        response = user.api.auth_api.refresh_token(expected_status=expected_status)
        response_data = RefreshTokenResponse(**response.json())
        assert response_data.accessToken is not None, "Токен доступа отсутствует в ответе"
        assert response_data.refreshToken is not None, "Токен не обновился"
        assert response_data.expiresIn is not None

    @pytest.mark.parametrize("user_role, expected_status", [
        ("common_super_admin", 401),
        ("common_admin", 401),
        ("common_user", 401)
    ], ids=[
        "SUPER_ADMIN not authorized",
        "ADMIN not authorized",
        "USER not authorized"
    ])
    def test_refresh_token_unauthorized(self, request, user_role, expected_status, api_manager):
        user = request.getfixturevalue(user_role)
        user.api.auth_api.session.headers.pop('Authorization', None)
        response = api_manager.auth_api.refresh_token(expected_status=expected_status)
        error_data = ErrorResponse(**response.json())
        assert "Unauthorized" in error_data.error or "token" in error_data.message.lower()

    def test_confirm_email_invalid_token(self, common_user):
        response = common_user.api.auth_api.confirm_email(
            token="any_invalid_token_12345",
            expected_status=400  # ← Меняем ожидаемый статус на 400
        )
        error_data = ErrorResponse(**response.json())
        assert error_data.message == "Неверный токен"
        assert error_data.statusCode == 400
