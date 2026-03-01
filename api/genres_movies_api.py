from requests import Response

from constants import MOVIE_ENDPOINT, MOVIE_REVIEWS_ENDPOINT, MOVIE_GENRES_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class GenresMoviesAPI(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url="https://api.dev-cinescope.coconutqa.ru")

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