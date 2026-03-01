import pytest
from api import movies_api
from api.movies_api import MoviesAPI
from conftest import test_user, api_manager
from api.api_manager import ApiManager


class TestReviewsApi:

    def test_get_reviews_movie(self, api_manager:ApiManager):
        response_get_movie = api_manager.movies_api.get_movie(movie_id="711")
        response_get_movie_data = response_get_movie.json()
        movie_id = response_get_movie_data['id']
        response_get_reviews_movie = api_manager.reviews_api.get_reviews_movie(movie_id)
        response_get_reviews_movie_data = response_get_reviews_movie.json()
        assert isinstance(response_get_reviews_movie_data, list)
        assert len(response_get_reviews_movie_data) > 0
        if response_get_reviews_movie_data:
            first_review = response_get_reviews_movie_data[0]
            expected_fields = ["userId", "text", "rating", "createdAt", "user"]
            for field in expected_fields:
                assert field in first_review, f"Поле '{field}' отсутствует в отзыве"

    def test_get_reviews_not_found_movie(self, api_manager:ApiManager):
        response_get_movie = api_manager.movies_api.get_movie(movie_id="1", expected_status=404)
        response_get_movie_data = response_get_movie.json()
        assert response_get_movie_data["message"] == "Фильм не найден"
        assert response_get_movie_data["error"] == "Not Found"
        assert response_get_movie_data["statusCode"] == 404

    def test_create_reviews_movie(self, admin_api_manager:ApiManager, movie_data_review):
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id="711")
        response_get_movie_data = response_get_movie.json()
        movie_id = response_get_movie_data['id']
        user_id = "a76b8bf9-af13-45bb-b200-b9db86db26d3"
        response_create_review = admin_api_manager.reviews_api.create_reviews_movie(movie_id, movie_data_review,
                                                                                    expected_status=201)
        response_create_review_data = response_create_review.json()
        assert "userId" in response_create_review_data
        assert response_create_review_data["text"] == movie_data_review['text']
        assert response_create_review_data["rating"] == movie_data_review['rating']
        assert "createdAt" in response_create_review_data
        assert "user" in response_create_review_data
        assert response_create_review_data["user"]['fullName'] == "Админ Кокосовый Куа"

        response_delete_movie = admin_api_manager.reviews_api.delete_reviews_movie(movie_id, user_id)
        response_delete_movie_data = response_delete_movie.json()
        assert response_delete_movie_data['userId'] == user_id
        assert response_delete_movie_data['text'] == movie_data_review['text']
        assert response_delete_movie_data['rating'] == movie_data_review['rating']
        assert 'createdAt' in response_delete_movie_data
        assert 'user' in response_delete_movie_data

    def test_create_reviews_duplicate(self, admin_api_manager:ApiManager, movie_data_review):
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id="895")
        response_get_movie_data = response_get_movie.json()
        movie_id = response_get_movie_data['id']
        user_id = "a76b8bf9-af13-45bb-b200-b9db86db26d3"
        admin_api_manager.reviews_api.create_reviews_movie(movie_id, movie_data_review, expected_status=201)
        response_create_review_second = admin_api_manager.reviews_api.create_reviews_movie(movie_id, movie_data_review,
                                                                                    expected_status=409)
        response_create_review_second_data = response_create_review_second.json()
        assert response_create_review_second_data['message'] == "Вы уже оставляли отзыв к этому фильму"
        assert response_create_review_second_data['error'] == "Conflict"
        assert response_create_review_second_data['statusCode'] == 409

        admin_api_manager.reviews_api.delete_reviews_movie(movie_id, user_id)

    def test_delete_reviews_not_found_movie(self, admin_api_manager:ApiManager):
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id="1044")
        response_get_movie_data = response_get_movie.json()
        movie_id = response_get_movie_data['id']
        user_id = "a76b8bf9-af13-45bb-b200-b9db86db26d3"
        response_delete_movie = admin_api_manager.reviews_api.delete_reviews_movie(movie_id, user_id, expected_status=404)
        response_delete_movie_data = response_delete_movie.json()
        assert response_delete_movie_data['message'] == "Отзыв не найден"
        assert response_delete_movie_data['error'] == "Not Found"
        assert response_delete_movie_data['statusCode'] == 404

    def test_update_reviews_movie(self, admin_api_manager:ApiManager, movie_data_review, movie_data_review_update):
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id="917")
        response_get_movie_data = response_get_movie.json()
        movie_id = response_get_movie_data['id']
        user_id = "a76b8bf9-af13-45bb-b200-b9db86db26d3"

        response_update_movie = admin_api_manager.reviews_api.update_reviews_movie(movie_id, movie_data_review_update, expected_status=200)
        response_update_movie_data = response_update_movie.json()
        assert response_update_movie_data['userId'] == user_id
        assert response_update_movie_data['text'] == movie_data_review_update['text']
        assert response_update_movie_data['rating'] == movie_data_review_update['rating']
        assert response_update_movie_data['movieId'] == movie_id
        assert "hidden" in response_update_movie_data
        assert "createdAt" in response_update_movie_data

    def test_update_not_found_reviews(self, admin_api_manager:ApiManager, movie_data_review_update):
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id="1044")
        response_get_movie_data = response_get_movie.json()
        movie_id = response_get_movie_data['id']
        user_id = "a76b8bf9-af13-45bb-b200-b9db86db26d3"
        response_update_movie = admin_api_manager.reviews_api.update_reviews_movie(movie_id, movie_data_review_update, expected_status=404)
        response_update_movie_data = response_update_movie.json()
        assert response_update_movie_data['message'] == "Отзыв не найден"
        assert response_update_movie_data['error'] == "Not Found"
        assert response_update_movie_data['statusCode'] == 404

    def test_hidden_reviews_movie(self, admin_api_manager:ApiManager, movie_data_review):
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id="899")
        response_get_movie_data = response_get_movie.json()
        movie_id = response_get_movie_data['id']
        user_id = "a76b8bf9-af13-45bb-b200-b9db86db26d3"

        response_hidden_movie_reviews = admin_api_manager.reviews_api.hidden_reviews_movie(movie_id, user_id)
        response_hidden_movie_reviews_data = response_hidden_movie_reviews.json()
        assert response_hidden_movie_reviews_data['userId'] == user_id
        assert response_hidden_movie_reviews_data['text'] == movie_data_review['text']
        assert response_hidden_movie_reviews_data['rating'] == 3
        assert "createdAt" in response_hidden_movie_reviews_data
        assert response_hidden_movie_reviews_data['user']['fullName'] == "Админ Кокосовый Куа"

    def test_hidden_not_found_reviews(self, admin_api_manager:ApiManager, movie_data_review):
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id="1044")
        response_get_movie_data = response_get_movie.json()
        movie_id = response_get_movie_data['id']
        user_id = "a76b8bf9-af13-45bb-b200-b9db86db26d3"
        response_hidden_movie_reviews = admin_api_manager.reviews_api.hidden_reviews_movie(movie_id, user_id, expected_status=404)
        response_hidden_movie_reviews_data = response_hidden_movie_reviews.json()
        assert response_hidden_movie_reviews_data['message'] == "Отзыв не найден"
        assert response_hidden_movie_reviews_data['error'] == "Not Found"
        assert response_hidden_movie_reviews_data['statusCode'] == 404

    def test_show_reviews_movie(self, admin_api_manager:ApiManager, movie_data_review):
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id="899")
        response_get_movie_data = response_get_movie.json()
        movie_id = response_get_movie_data['id']
        user_id = "a76b8bf9-af13-45bb-b200-b9db86db26d3"

        response_hidden_movie_reviews = admin_api_manager.reviews_api.show_reviews_movie(movie_id, user_id)
        response_hidden_movie_reviews_data = response_hidden_movie_reviews.json()
        assert response_hidden_movie_reviews_data['userId'] == user_id
        assert response_hidden_movie_reviews_data['text'] == movie_data_review['text']
        assert response_hidden_movie_reviews_data['rating'] == 3
        assert "createdAt" in response_hidden_movie_reviews_data
        assert response_hidden_movie_reviews_data['user']['fullName'] == "Админ Кокосовый Куа"

    def test_show_not_found_reviews(self, admin_api_manager:ApiManager, movie_data_review):
        response_get_movie = admin_api_manager.movies_api.get_movie(movie_id="1044")
        response_get_movie_data = response_get_movie.json()
        movie_id = response_get_movie_data['id']
        user_id = "a76b8bf9-af13-45bb-b200-b9db86db26d3"
        response_show_movie_reviews = admin_api_manager.reviews_api.show_reviews_movie(movie_id, user_id, expected_status=404)
        response_show_movie_reviews_data = response_show_movie_reviews.json()
        assert response_show_movie_reviews_data['message'] == "Отзыв не найден"
        assert response_show_movie_reviews_data['error'] == "Not Found"
        assert response_show_movie_reviews_data['statusCode'] == 404