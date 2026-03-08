from custom_requester.custom_requester import CustomRequester
from constants.endpoints import MOVIE_ENDPOINT, MOVIE_REVIEWS_ENDPOINT, MOVIE_GENRES_ENDPOINT

class MoviesAPI(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url="https://api.dev-cinescope.coconutqa.ru")

    def get_movies(self, params=None, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=MOVIE_ENDPOINT,
            data=None,
            expected_status=expected_status,
            params=params
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            data=None,
            expected_status=expected_status,
        )

    def create_movie(self, data_films: dict, expected_status=201, need_logging=True):
        return self.send_request(
            method="POST",
            endpoint=MOVIE_ENDPOINT,
            data=data_films,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def patch_movie(self, movie_id, data_films: dict, expected_status=200, need_logging=True):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            data=data_films,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def delete_movie(self, movie_id, expected_status=200, need_logging=True):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            data=None,
            expected_status=expected_status,
            need_logging=need_logging
        )
    def get_reviews_movie(self, movie_id, expected_status=200, need_logging=True):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}{MOVIE_REVIEWS_ENDPOINT}",
            data=None,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def create_reviews_movie(self, movie_id, movie_data_review: dict, expected_status=201, need_logging=True):
        return self.send_request(
            method="POST",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}{MOVIE_REVIEWS_ENDPOINT}",
            data=movie_data_review,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def delete_reviews_movie(self, movie_id, user_id, expected_status=200, need_logging=True):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}{MOVIE_REVIEWS_ENDPOINT}",
            data=None,
            expected_status=expected_status,
            need_logging=need_logging
        )
    def update_reviews_movie(self, movie_id, movie_data_review_update: dict, expected_status=200, need_logging=True):
        return self.send_request(
            method="PUT",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}{MOVIE_REVIEWS_ENDPOINT}",
            data=movie_data_review_update,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def hidden_reviews_movie(self, movie_id, user_id, expected_status=200, need_logging=True):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}{MOVIE_REVIEWS_ENDPOINT}/hide/{user_id}",
            data=None,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def show_reviews_movie(self, movie_id, user_id, expected_status=200, need_logging=True):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}{MOVIE_REVIEWS_ENDPOINT}/show/{user_id}",
            data=None,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def get_genres_movie(self, expected_status=200, need_logging=True):
        return self.send_request(
            method="GET",
            endpoint=MOVIE_GENRES_ENDPOINT,
            data=None,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def get_genre_movie(self, genre_id, expected_status=200, need_logging=True):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_GENRES_ENDPOINT}/{genre_id}",
            data=None,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def create_genres_movie(self, genres: dict, expected_status=201, need_logging=True):
        return self.send_request(
            method="POST",
            endpoint=MOVIE_GENRES_ENDPOINT,
            data=genres,
            expected_status=expected_status,
            need_logging=need_logging
        )

    def delete_genres_movie(self, genre_id, expected_status=200, need_logging=True):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIE_GENRES_ENDPOINT}/{genre_id}",
            data=None,
            expected_status=expected_status,
            need_logging=need_logging
        )