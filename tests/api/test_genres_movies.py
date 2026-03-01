import pytest
from api import movies_api
from api.movies_api import MoviesAPI
from conftest import test_user, api_manager
from api.api_manager import ApiManager


class TestGenresMoviesApi:

    def test_get_genres_movie(self, api_manager:ApiManager):
        response = api_manager.genres_api.get_genres_movie()
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "id" in data[0]
        assert "name" in data[0]

    def test_get_genre_movie_by_id(self, api_manager:ApiManager):
        response_get_genre = api_manager.genres_api.get_genre_movie(1)
        data = response_get_genre.json()
        assert data["id"] ==  1
        assert data["name"] ==  "Драма"

    def test_get_not_found_genre(self, api_manager:ApiManager):
        response_get_genre = api_manager.genres_api.get_genre_movie(9999, expected_status=404)
        data = response_get_genre.json()
        assert data["message"] ==  "Жанр не найден"
        assert data["error"] ==  "Not Found"
        assert data["statusCode"] == 404

    def test_create_genres_movie(self, admin_api_manager:ApiManager, movie_data_genres):
        response_create_genre = admin_api_manager.genres_api.create_genres_movie(movie_data_genres)
        data = response_create_genre.json()
        assert "id" in data
        assert data['name'] == movie_data_genres['name']

    def test_create_genres_movie_duplicate(self, admin_api_manager:ApiManager, movie_data_genres_duplicate):
        response_create_genre = admin_api_manager.genres_api.create_genres_movie(movie_data_genres_duplicate, expected_status=409)
        data = response_create_genre.json()
        assert data["message"] ==  "Такой жанр уже существует"
        assert data["error"] ==  "Conflict"
        assert data["statusCode"] ==  409

    def test_delete_genre_movie(self, admin_api_manager:ApiManager, movie_data_genres):
        response_create_genre = admin_api_manager.genres_api.create_genres_movie(movie_data_genres)
        response_create_genre_data = response_create_genre.json()
        genre_id = response_create_genre_data['id']

        response_delete_genre = admin_api_manager.genres_api.delete_genres_movie(genre_id)
        response_delete_genre_data = response_delete_genre.json()
        assert response_delete_genre_data["id"] ==  genre_id
        assert response_delete_genre_data["name"] == movie_data_genres['name']

        response_get_genre = admin_api_manager.genres_api.get_genre_movie(genre_id, expected_status=404)
        data = response_get_genre.json()
        assert data["message"] == "Жанр не найден"
        assert data["error"] == "Not Found"
        assert data["statusCode"] == 404

