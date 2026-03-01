from api.auth_api import AuthAPI
from api.genres_movies_api import GenresMoviesAPI
from api.movies_api import MoviesAPI
from api.reviews_api import ReviewsAPI
from api.user_api import UserAPI

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesAPI(session)
        self.reviews_api = ReviewsAPI(session)
        self.genres_api = GenresMoviesAPI(session)

