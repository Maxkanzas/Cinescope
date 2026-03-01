import pytest
from api import movies_api
from api.movies_api import MoviesAPI
from conftest import api_manager
from api.api_manager import ApiManager

class TestMoviesApi:
    def test_get_movies_default_params(self, api_manager:ApiManager):
        response = api_manager.movies_api.get_movies()
        response_data = response.json()
        assert response.status_code == 200
        assert "movies" in response_data, "В ответе отсутствует список movies"
        assert isinstance(response_data['movies'], list), "movies должен быть списком"
        assert "count" in response_data, "В ответе отсутствует поле count"
        assert "page" in response_data, "В ответе отсутствует поле page"
        assert "pageSize" in response_data, "В ответе отсутствует поле pageSize"
        assert "pageCount" in response_data, "В ответе отсутствует поле pageCount"
        if response_data["movies"]:
            first_movie = response_data["movies"][0]
            expected_fields = ["id", "name", "price", "description", "imageUrl", "location", "published", "genreId",
                               "genre", "createdAt", "rating"]
            for field in expected_fields:
                assert field in first_movie, f"В объекте фильма отсутствует поле {field}"

    def test_get_movies_with_filters(self, api_manager:ApiManager):
        params = {
            "pageSize": 5,
            "page": 2,
            "minPrice": 100,
            "maxPrice": 500,
            "locations": ["MSK"],
            "published": True,
            "genreId": 1,
            "createdAt": "desc"
        }
        response = api_manager.movies_api.get_movies(params=params)
        response_data = response.json()
        assert response.status_code == 200
        for movie in response_data['movies']:
            assert movie['price'] >= 100, f"Цена {movie['price']} меньше 100"
            assert movie['price'] <= 500, f"Цена {movie['price']} больше 100"
            assert movie['location'] == "MSK", f"Локация {movie['location']} не соответствует MSK"
            assert movie['genreId'] == 1, f"Жанр {movie['genreId']} не соответствует 1"
            assert movie['published'] is True, "Фильм не опубликован"

    def test_get_movies_invalid_params(self, api_manager: ApiManager):
        params = {
            "genreId": -1,
            "createdAt": "abc"
        }
        response = api_manager.movies_api.get_movies(params=params, expected_status=400)
        response_data = response.json()
        assert response.status_code == 400
        assert "message" in response_data
        assert "error" in response_data
        assert "statusCode" in response_data

    def test_get_movie_by_id(self, api_manager: ApiManager, admin_api_manager: ApiManager,
                                    auth_session_admin, movie_data_random):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        movie_id = response_create_movie_data['id']
        response_get_movie = api_manager.movies_api.get_movie(movie_id)
        response_get_movie_data = response_get_movie.json()
        assert response_create_movie_data['id'] == response_get_movie_data['id']
        assert response_create_movie_data['name'] == response_get_movie_data['name']
        assert response_create_movie_data['description'] == response_get_movie_data['description']
        assert response_create_movie_data['price'] == response_get_movie_data['price']
        assert response_create_movie_data['location'] == response_get_movie_data['location']
        assert response_create_movie_data['genreId'] == response_get_movie_data['genreId']
        assert response_create_movie_data['imageUrl'] == response_get_movie_data['imageUrl']
        assert response_create_movie_data['published'] == response_get_movie_data['published']

    def test_get_movie_invalid_id(self, api_manager: ApiManager):
        movie_id = 1
        response_get_movie = api_manager.movies_api.get_movie(movie_id, expected_status=404)
        response_get_movie_data = response_get_movie.json()
        assert response_get_movie_data['message'] == "Фильм не найден"
        assert response_get_movie_data['error'] == "Not Found"
        assert response_get_movie_data['statusCode'] == 404

    def test_create_movie(self, admin_api_manager: ApiManager, auth_session_admin, movie_data_random):
        response = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_data = response.json()
        assert response_data['name'] == movie_data_random['name']
        assert response_data['description'] == movie_data_random['description']
        assert response_data['price'] == movie_data_random['price']
        assert response_data['location'] == movie_data_random['location']
        assert response_data['genreId'] == movie_data_random['genreId']
        assert response_data['imageUrl'] == movie_data_random['imageUrl']
        assert response_data['published'] == movie_data_random['published']

    def test_create_duplicate_movie(self, admin_api_manager: ApiManager, auth_session_admin, movie_data_duplicate):
        response = admin_api_manager.movies_api.create_movie(movie_data_duplicate, expected_status=409)
        response_data = response.json()
        assert response.status_code == 409, f"Фильм с названием {movie_data_duplicate['name']} уже существует"
        assert "message" in response_data
        assert "error" in response_data
        assert "statusCode" in response_data

    def test_create_empty_movie(self, admin_api_manager: ApiManager, auth_session_admin, movie_data_empty):
        response = admin_api_manager.movies_api.create_movie(movie_data_empty, expected_status=400)
        response_data = response.json()
        expected_messages = [
            "name should not be empty",
            "Поле name должно быть строкой",
            "Поле price должно быть числом",
            "Поле description должно быть строкой",
            "Поле location должно быть одним из: MSK, SPB",
            "Поле location должно быть строкой",
            "Поле published должно быть булевым значением",
            "Поле genreId должно быть числом"
        ]
        assert response.status_code == 400, f"Фильм с названием {movie_data_empty['name']} уже существует"
        assert response_data["error"] == "Bad Request"
        assert response_data['message'] == expected_messages

    def test_delete_movie_by_id(self, admin_api_manager: ApiManager, auth_session_admin, movie_data_random):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        movie_id = response_create_movie_data['id']
        response_delete_movie = admin_api_manager.movies_api.delete_movie(movie_id)
        response_delete_movie_data = response_delete_movie.json()
        assert response_create_movie_data['id'] == response_delete_movie_data['id']
        assert response_create_movie_data['name'] == response_delete_movie_data['name']
        assert response_create_movie_data['description'] == response_delete_movie_data['description']
        assert response_create_movie_data['price'] == response_delete_movie_data['price']
        assert response_create_movie_data['location'] == response_delete_movie_data['location']
        assert response_create_movie_data['genreId'] == response_delete_movie_data['genreId']
        assert response_create_movie_data['imageUrl'] == response_delete_movie_data['imageUrl']
        assert response_create_movie_data['published'] == response_delete_movie_data['published']
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id, expected_status=404)
        response_get_movie_data = response_get_movie.json()
        assert response_get_movie_data['message'] == "Фильм не найден"
        assert response_get_movie_data['error'] == "Not Found"
        assert response_get_movie_data['statusCode'] == 404

    def test_delete_movie_empty(self, admin_api_manager: ApiManager, auth_session_admin, movie_data_random):
        movie_id = "@#$"
        response_delete_movie = admin_api_manager.movies_api.delete_movie(movie_id, expected_status=404)
        response_delete_movie_data = response_delete_movie.json()
        assert response_delete_movie_data['message'] == "Фильм не найден"
        assert response_delete_movie_data['error'] == "Not Found"
        assert response_delete_movie_data['statusCode'] == 404

    def test_patch_movie(self, admin_api_manager:ApiManager, auth_session_admin, movie_data_random, movie_data_update):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        movie_id = response_create_movie_data['id']
        response_update_movie = admin_api_manager.movies_api.patch_movie(movie_id, movie_data_update)
        response_update_movie_data = response_update_movie.json()
        assert response_update_movie_data['id'] == movie_id
        expected_fields = ['id', 'name', 'price', 'description', 'imageUrl',
                           'location', 'published', 'rating', 'genreId', 'createdAt', 'genre']
        for field in expected_fields:
            assert field in response_update_movie_data, f"Поле {field} отсутствует в ответе"

    def test_patch_movie_invalid_param(self, admin_api_manager:ApiManager, auth_session_admin, movie_data_random, movie_invalid_data):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        movie_id = response_create_movie_data['id']
        response_update_movie = admin_api_manager.movies_api.patch_movie(movie_id, movie_invalid_data, expected_status=400)
        response_update_movie_data = response_update_movie.json()
        assert response_update_movie_data['message'][0] == "Поле name должно быть строкой"
        assert response_update_movie_data['error'] == "Bad Request"

    def test_patch_movie_notfound(self, admin_api_manager:ApiManager, auth_session_admin, movie_data_update):
        movie_id = 1
        response_update_movie = admin_api_manager.movies_api.patch_movie(movie_id, movie_data_update, expected_status=404)
        response_update_movie_data = response_update_movie.json()
        assert response_update_movie_data['message'] == "Фильм не найден"
        assert response_update_movie_data['error'] == "Not Found"
