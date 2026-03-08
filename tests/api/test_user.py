import pytest

from api.api_manager import ApiManager
from constants.roles import Roles
from custom_requester.custom_requester import CustomRequester
from constants.endpoints import MOVIE_ENDPOINT, MOVIE_REVIEWS_ENDPOINT, MOVIE_GENRES_ENDPOINT
from schemas import CreateUserResponse, ErrorResponse, UpdateUserResponse


class TestUser:
    def test_create_user(self, common_super_admin, user_creation_data):
        response = common_super_admin.api.user_api.create_user(user_creation_data)
        data = CreateUserResponse(**response.json())
        user_id = data.id
        assert data.id is not None
        assert data.email == user_creation_data['email']
        assert data.fullName == user_creation_data['fullName']
        assert data.roles == user_creation_data['roles']
        assert data.verified == user_creation_data["verified"]
        assert data.createdAt is not None
        common_super_admin.api.user_api.delete_user(user_id)
        get_response = common_super_admin.api.user_api.get_user(user_id, expected_status=200)
        assert get_response.json() == {}

    def test_create_user_with_invalid_data(self, common_super_admin, user_creation_invalid_data):
        response = common_super_admin.api.user_api.create_user(user_creation_invalid_data, expected_status=400)
        data = ErrorResponse(**response.json())
        assert data.message is not None
        assert data.error == "Bad Request"

    def test_create_admin_without_permissions(self, common_user, user_creation_data):
        response = common_user.api.user_api.create_user(user_creation_data, expected_status=403)
        data = ErrorResponse(**response.json())
        assert data.message == "Forbidden resource"
        assert data.error == "Forbidden"

    def test_create_user_with_existing_email(self, common_super_admin, user_creation_data):
        common_super_admin.api.user_api.create_user(user_creation_data)
        response_second = common_super_admin.api.user_api.create_user(user_creation_data, expected_status=500)
        data = ErrorResponse(**response_second.json())
        assert data.message == "Internal server error"

    def test_changed_data_user(self, common_super_admin, user_creation_data, user_changed_data):
        created_user_response = common_super_admin.api.user_api.create_user(user_creation_data).json()
        get_id = created_user_response['id']
        changed_user_response = common_super_admin.api.user_api.changed_user_data(get_id, user_changed_data)
        data = UpdateUserResponse(**changed_user_response.json())
        assert data.email == user_creation_data['email']
        assert data.fullName == user_creation_data['fullName']
        assert data.roles == user_changed_data['roles']
        assert data.verified == user_changed_data["verified"]
        assert data.createdAt is not None
        common_super_admin.api.user_api.delete_user(get_id)
        get_response = common_super_admin.api.user_api.get_user(get_id, expected_status=200)
        assert get_response.json() == {}

    def test_changed_with_invalid_data(self, common_super_admin, user_creation_data, user_creation_invalid_data):
        created_user_response = common_super_admin.api.user_api.create_user(user_creation_data).json()
        get_id = created_user_response['id']
        changed_user_response = common_super_admin.api.user_api.changed_user_data(get_id, user_creation_invalid_data,
                                                                                  expected_status=400)
        data = ErrorResponse(**changed_user_response.json())
        assert data.message is not None
        assert data.error == "Bad Request"


    def test_changed_without_permissions(self, common_user, common_super_admin, user_creation_data, user_creation_invalid_data):
        created_user_response = common_super_admin.api.user_api.create_user(user_creation_data).json()
        get_id = created_user_response['id']
        changed_user_response = common_user.api.user_api.changed_user_data(get_id, user_creation_invalid_data, expected_status=500)
        data = ErrorResponse(**changed_user_response.json())
        assert data.message == "Internal server error"
