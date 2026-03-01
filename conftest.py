import os
import pytest
import requests
import json
from api.api_manager import ApiManager
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def user_admin_creds():
    """
    Генерация админа.
    """
    return {
        "email": "api1@gmail.com",
        # "fullName": random_name,
        "password": "asdqwe123Q",
        "passwordRepeat": "asdqwe123Q",
        "roles": ["SUPER_ADMIN"]
    }

@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user


@pytest.fixture(scope="function")
def auth_session(test_user):
    """
    Фикстура для создания авторизованной сессии.
    """
    # Регистрируем нового пользователя
    register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(register_url, json=test_user, headers=headers)
    assert response.status_code == 201, "Ошибка регистрации пользователя"

    # Логинимся для получения токена
    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = requests.post(login_url, json=login_data, headers=headers)
    assert response.status_code == 200, "Ошибка авторизации"

    # Получаем токен и создаём сессию
    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(headers)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture(scope="session")
def auth_session_admin(user_admin_creds):
    """
    Фикстура для создания авторизованной сессии.
    """
    # Логинимся для получения токена
    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_data = {
        "email": user_admin_creds["email"],
        "password": user_admin_creds["password"]
    }
    response = requests.post(login_url, json=login_data)
    assert response.status_code == 201, "Ошибка авторизации"

    # Получаем токен и создаём сессию
    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture
def admin_api_manager(auth_session_admin):
    """
    Фикстура, возвращающая ApiManager с авторизованной сессией ADMIN.
    """
    return ApiManager(auth_session_admin)

@pytest.fixture(scope="function")
def movie_data_random():
    return {
        "name": f"{DataGenerator.generate_random_string(5)}",
        "description": DataGenerator.generate_random_sentence(10),
        "price": DataGenerator.generate_random_int(100, 1000),
        "location": DataGenerator.random_choice(["MSK", "SPB"]),
        "genreId": DataGenerator.generate_random_int(1, 10),
        "imageUrl": "https://example.com/image.jpg",
        "published": True
    }

@pytest.fixture(scope="session")
def movie_data_duplicate():
    description = (
        f"1967 год, Ньюарк в штате Нью-Джерси. Маленький Тони Сопрано восхищается "
        f"деловым партнёром отца — Ричардом Молтисанти по прозвищу Дики. Тот "
        f"ответственно ведёт доверенную ему отцом, местным криминальным авторитетом, "
        f"часть бизнеса и, в отличие от остальных мафиози, не гнушается иметь дело "
        f"с чернокожими. Когда в городе вспыхивают беспорядки, спровоцированные "
        f"жестоким обращением полиции с чёрным таксистом, Дики совершает импульсивный "
        f"поступок и использует окружающий хаос в качестве прикрытия."
    )
    return {
        "name": "The Many Saints of Newark",
        "description": description,
        "price": DataGenerator.generate_random_int(100, 1000),
        "location": DataGenerator.random_choice(["MSK", "SPB"]),
        "genreId": DataGenerator.generate_random_int(1, 10),
        "imageUrl": "https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/6429e089-cd97-4f46-a101-b7d0a0adca93/1920x",
        "published": True
    }

@pytest.fixture(scope="function")
def movie_data_empty():
    return {}

@pytest.fixture(scope="function")
def movie_data_update():
    return {
        "name": f"{DataGenerator.generate_random_string(5)}",
        "description": DataGenerator.generate_random_sentence(10),
        "price": DataGenerator.generate_random_int(100, 1000),
        "location": DataGenerator.random_choice(["MSK", "SPB"]),
        "genreId": DataGenerator.generate_random_int(1, 10),
        "imageUrl": "https://kg-portal.ru/img/134224/main.webp",
        "published": False
    }

@pytest.fixture(scope="session")
def movie_data_review():
    return {
        "rating": DataGenerator.generate_random_int(1, 5),
        "text": "Сюжет немножко затянут. Однако, концовка максимально непредсказуемая"
    }

@pytest.fixture(scope="function")
def movie_data_review_update():
    return {
        "rating": DataGenerator.generate_random_int(1, 5),
        "text": f"{DataGenerator.generate_random_string(5)}"
    }

@pytest.fixture(scope="function")
def movie_data_genres():
    return {
        "name": f"Тестовый жанр: байопик/{DataGenerator.generate_random_int(1, 1999)}"
    }

@pytest.fixture(scope="function")
def movie_data_genres_duplicate():
    return {
        "name": "Драма"
    }

@pytest.fixture(scope="function")
def params_get_movies_with_filters():
    return {
        "pageSize": DataGenerator.generate_random_int(1, 5),
        "page": DataGenerator.generate_random_int(1, 5),
        "minPrice": DataGenerator.generate_random_int(100, 100),
        "maxPrice": DataGenerator.generate_random_int(500, 500),
        "locations": DataGenerator.random_choice(["MSK", "SPB"]),
        "published": True,
        "genreId": DataGenerator.generate_random_int(1, 10),
        "createdAt": "desc"
    }

@pytest.fixture(scope="function")
def movie_invalid_data():
    return {
        "pageSize": DataGenerator.generate_random_int(-10, 0),
        "page": DataGenerator.generate_random_int(1, 5),
        "minPrice": DataGenerator.generate_random_int(100, 100),
        "maxPrice": DataGenerator.generate_random_int(500, 500),
        "locations": DataGenerator.random_choice(["MSK", "SPB"]),
        "published": True,
        "genreId": DataGenerator.generate_random_int(1, 10),
        "createdAt": "desc"
    }

@pytest.fixture(scope="function")
def movie_data_invalid():
    return {
        "name": 211,
        "description": DataGenerator.generate_random_sentence(10),
        "price": DataGenerator.generate_random_int(100, 1000),
        "location": DataGenerator.random_choice(["MSK", "SPB"]),
        "genreId": DataGenerator.generate_random_int(1, 10),
        "imageUrl": "https://kg-portal.ru/img/134224/main.webp",
        "published": False
    }

@pytest.fixture(scope="session")
def movie_id_invalid():
    return f"{DataGenerator.generate_random_string(5)}"

@pytest.fixture(scope="function")
def movie_id():
    return f"{DataGenerator.generate_random_int(600, 900)}"
