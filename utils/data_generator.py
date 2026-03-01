import random
import string
from faker import Faker

faker = Faker()

class DataGenerator:
    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"


    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"


    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_string(length: int) -> str:
        """Генерирует случайную строку из букв и цифр"""
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generate_random_sentence(word_count: int) -> str:
        """Генерирует случайное предложение из указанного количества слов"""
        words = []
        for _ in range(word_count):
            word_length = random.randint(3, 10)
            word = DataGenerator.generate_random_string(word_length)
            words.append(word)
        return ' '.join(words).capitalize() + '.'

    @staticmethod
    def generate_random_int(min_value: int, max_value: int) -> int:
        """Генерирует случайное целое число в диапазоне"""
        return random.randint(min_value, max_value)

    @staticmethod
    def random_choice(choices: list):
        """Выбирает случайный элемент из списка"""
        return random.choice(choices)
