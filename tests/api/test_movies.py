import pytest
from api import movies_api
from api.movies_api import MoviesAPI
from conftest import api_manager
from api.api_manager import ApiManager
from constants import USER_ADMIN

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

    def test_get_movies_with_filters(self, api_manager:ApiManager, params_get_movies_with_filters):
        response = api_manager.movies_api.get_movies(params=params_get_movies_with_filters)
        response_data = response.json()
        for movie in response_data['movies']:
            assert movie['price'] >= params_get_movies_with_filters['minPrice'], f"Цена {movie['price']} меньше 100"
            assert movie['price'] <= params_get_movies_with_filters['maxPrice'], f"Цена {movie['price']} больше 100"
            assert movie['location'] == params_get_movies_with_filters['locations'], f"Локация {movie['location']} не соответствует MSK"
            assert movie['genreId'] == params_get_movies_with_filters['genreId'], f"Жанр {movie['genreId']} не соответствует 1"
            assert movie['published'] is True, "Фильм не опубликован"

    def test_get_movies_invalid_params(self, api_manager: ApiManager, movie_invalid_data):
        response = api_manager.movies_api.get_movies(params=movie_invalid_data, expected_status=400)
        response_data = response.json()
        assert response.status_code == 400
        assert "message" in response_data
        assert "error" in response_data
        assert "statusCode" in response_data

    def test_get_movie_by_id(self, admin_api_manager: ApiManager, movie_data_random):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        movie_id = response_create_movie_data['id']
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id)
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

    def test_delete_movie_by_id(self, admin_api_manager: ApiManager, movie_data_random):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        response_movie_id = response_create_movie_data['id']
        response_delete_movie = admin_api_manager.movies_api.delete_movie(response_movie_id)
        response_delete_movie_data = response_delete_movie.json()
        assert response_create_movie_data['id'] == response_delete_movie_data['id']
        assert response_create_movie_data['name'] == response_delete_movie_data['name']
        assert response_create_movie_data['description'] == response_delete_movie_data['description']
        assert response_create_movie_data['price'] == response_delete_movie_data['price']
        assert response_create_movie_data['location'] == response_delete_movie_data['location']
        assert response_create_movie_data['genreId'] == response_delete_movie_data['genreId']
        assert response_create_movie_data['imageUrl'] == response_delete_movie_data['imageUrl']
        assert response_create_movie_data['published'] == response_delete_movie_data['published']
        response_get_movie = admin_api_manager.movies_api.get_movie(response_movie_id, expected_status=404)
        response_get_movie_data = response_get_movie.json()
        assert response_get_movie_data['message'] == "Фильм не найден"
        assert response_get_movie_data['error'] == "Not Found"
        assert response_get_movie_data['statusCode'] == 404

    def test_delete_movie_empty(self, admin_api_manager: ApiManager, movie_data_random, movie_id_invalid):
        response_delete_movie = admin_api_manager.movies_api.delete_movie(movie_id_invalid, expected_status=404)
        response_delete_movie_data = response_delete_movie.json()
        assert response_delete_movie_data['message'] == "Фильм не найден"
        assert response_delete_movie_data['error'] == "Not Found"
        assert response_delete_movie_data['statusCode'] == 404

    def test_patch_movie(self, admin_api_manager:ApiManager, movie_data_random, movie_data_update):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        response_movie_id = response_create_movie_data['id']
        response_update_movie = admin_api_manager.movies_api.patch_movie(response_movie_id, movie_data_update)
        response_update_movie_data = response_update_movie.json()
        assert response_update_movie_data['id'] == response_movie_id
        expected_fields = ['id', 'name', 'price', 'description', 'imageUrl',
                           'location', 'published', 'rating', 'genreId', 'createdAt', 'genre']
        for field in expected_fields:
            assert field in response_update_movie_data, f"Поле {field} отсутствует в ответе"

    def test_patch_movie_invalid_param(self, admin_api_manager:ApiManager, movie_data_random, movie_data_invalid):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        response_movie_id = response_create_movie_data['id']
        response_update_movie = admin_api_manager.movies_api.patch_movie(response_movie_id, movie_data_invalid, expected_status=400)
        response_update_movie_data = response_update_movie.json()
        assert response_update_movie_data['message'][0] == "Поле name должно быть строкой"
        assert response_update_movie_data['error'] == "Bad Request"

    def test_patch_movie_notfound(self, admin_api_manager:ApiManager, movie_id_invalid, movie_data_update):
        response_update_movie = admin_api_manager.movies_api.patch_movie(movie_id_invalid, movie_data_update, expected_status=404)
        response_update_movie_data = response_update_movie.json()
        assert response_update_movie_data['message'] == "Фильм не найден"
        assert response_update_movie_data['error'] == "Not Found"

    def test_get_reviews_movie(self, admin_api_manager:ApiManager, movie_data_random, movie_data_review):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        response_movie_id = response_create_movie_data['id']
        admin_api_manager.movies_api.create_reviews_movie(response_movie_id, movie_data_review)
        response_get_reviews_movie = admin_api_manager.movies_api.get_reviews_movie(response_movie_id)
        response_get_reviews_movie_data = response_get_reviews_movie.json()
        assert isinstance(response_get_reviews_movie_data, list)
        assert len(response_get_reviews_movie_data) > 0
        if response_get_reviews_movie_data:
            first_review = response_get_reviews_movie_data[0]
            expected_fields = ["userId", "text", "rating", "createdAt", "user"]
            for field in expected_fields:
                assert field in first_review, f"Поле '{field}' отсутствует в отзыве"

    def test_get_reviews_not_found_movie(self, api_manager:ApiManager, movie_id):
        response_get_movie = api_manager.movies_api.get_movie(movie_id, expected_status=404)
        response_get_movie_data = response_get_movie.json()
        assert response_get_movie_data["message"] == "Фильм не найден"
        assert response_get_movie_data["error"] == "Not Found"
        assert response_get_movie_data["statusCode"] == 404

    def test_create_reviews_movie(self, admin_api_manager:ApiManager, movie_data_random, movie_data_review):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        response_movie_id = response_create_movie_data['id']
        response_create_review_movie = admin_api_manager.movies_api.create_reviews_movie(response_movie_id, movie_data_review)
        response_create_review_movie_data = response_create_review_movie.json()
        assert "userId" in response_create_review_movie_data
        assert response_create_review_movie_data["text"] == movie_data_review['text']
        assert response_create_review_movie_data["rating"] == movie_data_review['rating']
        assert "createdAt" in response_create_review_movie_data
        assert "user" in response_create_review_movie_data
        assert response_create_review_movie_data["user"]['fullName'] == "Админ Кокосовый Куа"
        response_delete_movie = admin_api_manager.movies_api.delete_reviews_movie(response_movie_id, USER_ADMIN)
        response_delete_movie_data = response_delete_movie.json()
        assert response_delete_movie_data['userId'] == USER_ADMIN
        assert response_delete_movie_data['text'] == movie_data_review['text']
        assert response_delete_movie_data['rating'] == movie_data_review['rating']
        assert 'createdAt' in response_delete_movie_data
        assert 'user' in response_delete_movie_data

    def test_create_reviews_duplicate(self, admin_api_manager:ApiManager, movie_data_random, movie_data_review):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        response_movie_id = response_create_movie_data['id']
        admin_api_manager.movies_api.create_reviews_movie(response_movie_id,movie_data_review)
        response_create_review_second = admin_api_manager.movies_api.create_reviews_movie(response_movie_id,
                                                                    movie_data_review, expected_status=409)
        response_create_review_second_data = response_create_review_second.json()
        assert response_create_review_second_data['message'] == "Вы уже оставляли отзыв к этому фильму"
        assert response_create_review_second_data['error'] == "Conflict"
        assert response_create_review_second_data['statusCode'] == 409

    def test_delete_reviews_not_found_movie(self, admin_api_manager:ApiManager, movie_id_invalid):
        response_delete_movie = admin_api_manager.movies_api.delete_reviews_movie(movie_id_invalid, USER_ADMIN,
                                                                                  expected_status=404)
        response_delete_movie_data = response_delete_movie.json()
        assert response_delete_movie_data['message'] == "Отзыв не найден"
        assert response_delete_movie_data['error'] == "Not Found"
        assert response_delete_movie_data['statusCode'] == 404

    def test_update_reviews_movie(self, admin_api_manager:ApiManager, movie_data_random, movie_data_review,
                                  movie_data_review_update):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        response_movie_id = response_create_movie_data['id']
        response_create_review_movie = admin_api_manager.movies_api.create_reviews_movie(response_movie_id,
                                                                                         movie_data_review)
        response_update_movie = admin_api_manager.movies_api.update_reviews_movie(response_movie_id,
                                                                                  movie_data_review_update)
        response_update_movie_data = response_update_movie.json()
        assert response_update_movie_data['userId'] == USER_ADMIN
        assert response_update_movie_data['text'] == movie_data_review_update['text']
        assert response_update_movie_data['rating'] == movie_data_review_update['rating']
        assert response_update_movie_data['movieId'] == response_movie_id
        assert "hidden" in response_update_movie_data
        assert "createdAt" in response_update_movie_data
        admin_api_manager.movies_api.delete_movie(response_movie_id)

    def test_update_not_found_reviews(self, admin_api_manager:ApiManager, movie_data_review_update, movie_id_invalid):
        response = admin_api_manager.movies_api.update_reviews_movie(movie_id_invalid, movie_data_review_update,
                                                                                  expected_status=404)
        response_data = response.json()
        assert response_data['message'] == "Отзыв не найден"
        assert response_data['error'] == "Not Found"
        assert response_data['statusCode'] == 404

    def test_hidden_reviews_movie(self, admin_api_manager:ApiManager, movie_data_random, movie_data_review):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        response_movie_id = response_create_movie_data['id']
        response_create_review_movie = admin_api_manager.movies_api.create_reviews_movie(response_movie_id,
                                                                                         movie_data_review)
        response_hidden_movie_reviews = admin_api_manager.movies_api.hidden_reviews_movie(response_movie_id, USER_ADMIN)
        response_hidden_movie_reviews_data = response_hidden_movie_reviews.json()
        assert response_hidden_movie_reviews_data['userId'] == USER_ADMIN
        assert response_hidden_movie_reviews_data['text'] == movie_data_review['text']
        assert response_hidden_movie_reviews_data['rating'] == movie_data_review['rating']
        assert "createdAt" in response_hidden_movie_reviews_data
        assert response_hidden_movie_reviews_data['user']['fullName'] == "Админ Кокосовый Куа"
        admin_api_manager.movies_api.delete_movie(response_movie_id)

    def test_hidden_not_found_reviews(self, admin_api_manager:ApiManager, movie_data_review, movie_id_invalid):
        response = admin_api_manager.movies_api.hidden_reviews_movie(movie_id_invalid, USER_ADMIN, expected_status=404)
        response_data = response.json()
        assert response_data['message'] == "Отзыв не найден"
        assert response_data['error'] == "Not Found"
        assert response_data['statusCode'] == 404

    def test_show_reviews_movie(self, admin_api_manager:ApiManager, movie_data_random, movie_data_review):
        response_create_movie = admin_api_manager.movies_api.create_movie(movie_data_random)
        response_create_movie_data = response_create_movie.json()
        response_movie_id = response_create_movie_data['id']
        response_create_review_movie = admin_api_manager.movies_api.create_reviews_movie(response_movie_id,
                                                                                         movie_data_review)
        response_hidden_movie_reviews = admin_api_manager.movies_api.show_reviews_movie(response_movie_id, USER_ADMIN)
        response_hidden_movie_reviews_data = response_hidden_movie_reviews.json()
        assert response_hidden_movie_reviews_data['userId'] == USER_ADMIN
        assert response_hidden_movie_reviews_data['text'] == movie_data_review['text']
        assert response_hidden_movie_reviews_data['rating'] == movie_data_review['rating']
        assert "createdAt" in response_hidden_movie_reviews_data
        assert response_hidden_movie_reviews_data['user']['fullName'] == "Админ Кокосовый Куа"

    def test_show_not_found_reviews(self, admin_api_manager:ApiManager, movie_data_review, movie_id_invalid):
        response = admin_api_manager.movies_api.show_reviews_movie(movie_id_invalid, USER_ADMIN, expected_status=404)
        response_data = response.json()
        assert response_data['message'] == "Отзыв не найден"
        assert response_data['error'] == "Not Found"
        assert response_data['statusCode'] == 404

    def test_get_genres_movie(self, api_manager:ApiManager):
        response = api_manager.movies_api.get_genres_movie()
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "id" in data[0]
        assert "name" in data[0]

    def test_get_genre_movie_by_id(self, api_manager:ApiManager):
        response_get_genre = api_manager.movies_api.get_genre_movie(1)
        data = response_get_genre.json()
        assert data["id"] ==  1
        assert data["name"] ==  "Драма"

    def test_get_not_found_genre(self, api_manager:ApiManager):
        response_get_genre = api_manager.movies_api.get_genre_movie(9999, expected_status=404)
        data = response_get_genre.json()
        assert data["message"] ==  "Жанр не найден"
        assert data["error"] ==  "Not Found"
        assert data["statusCode"] == 404

    def test_create_genres_movie(self, admin_api_manager:ApiManager, movie_data_genres):
        response_create_genre = admin_api_manager.movies_api.create_genres_movie(movie_data_genres)
        data = response_create_genre.json()
        assert "id" in data
        assert data['name'] == movie_data_genres['name']

    def test_create_genres_movie_duplicate(self, admin_api_manager:ApiManager, movie_data_genres_duplicate):
        response_create_genre = admin_api_manager.movies_api.create_genres_movie(movie_data_genres_duplicate, expected_status=409)
        data = response_create_genre.json()
        assert data["message"] ==  "Такой жанр уже существует"
        assert data["error"] ==  "Conflict"
        assert data["statusCode"] ==  409

    def test_delete_genre_movie(self, admin_api_manager:ApiManager, movie_data_genres):
        response_create_genre = admin_api_manager.movies_api.create_genres_movie(movie_data_genres)
        response_create_genre_data = response_create_genre.json()
        genre_id = response_create_genre_data['id']

        response_delete_genre = admin_api_manager.movies_api.delete_genres_movie(genre_id)
        response_delete_genre_data = response_delete_genre.json()
        assert response_delete_genre_data["id"] ==  genre_id
        assert response_delete_genre_data["name"] == movie_data_genres['name']

        response_get_genre = admin_api_manager.movies_api.get_genre_movie(genre_id, expected_status=404)
        data = response_get_genre.json()
        assert data["message"] == "Жанр не найден"
        assert data["error"] == "Not Found"
        assert data["statusCode"] == 404