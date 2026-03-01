from requests import Response
from custom_requester.custom_requester import CustomRequester
from constants import MOVIE_ENDPOINT

class MoviesAPI(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url="https://api.dev-cinescope.coconutqa.ru")

    def get_movies(self, params=None, expected_status=200) -> Response:
        return self.send_request(
            method="GET",
            endpoint=MOVIE_ENDPOINT,
            data=None,
            expected_status=expected_status,
            params=params
        )

    def get_movie(self, movie_id, expected_status=200) -> Response:
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
