from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union
import datetime
import re
from typing import List
from pydantic import BaseModel, Field, field_validator
from constants.roles import Roles


class TestUser(BaseModel):
    id: Optional[str] = Field(default=None, exclude=True)
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен полностью совпадать с полем password")
    roles: Optional[List[Roles]] = Field(default=[Roles.USER], exclude=True)
    verified: Optional[bool] = Field(default=None, exclude=True)
    banned: Optional[bool] = Field(default=None, exclude=True)

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    class Config:
        use_enum_values = True
        json_encoders = {
            Roles: lambda v: v.value
        }

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: Optional[bool] = None
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value

    class Config:
        use_enum_values = True
        json_encoders = {
            Roles: lambda v: v.value
        }


class CreateUserResponse(BaseModel):
    """Модель ответа при создании пользователя"""
    id: Optional[str] = None
    email: str
    fullName: str
    verified: bool
    roles: List[str]  # или List[Roles] если используете Enum
    createdAt: str

    class Config:
        use_enum_values = True

class LoginUserResponse(BaseModel):
    """Модель для ответа от логина"""
    user: dict
    accessToken: str
    refreshToken: str
    expiresIn: int

class ErrorResponse(BaseModel):
    """Модель для ответа с ошибкой"""
    message: Union[str, List[str]]
    error: Optional[str] = None
    statusCode: int

class RefreshTokenResponse(BaseModel):
    """Модель для ответа с обновлением логина"""
    accessToken: str
    refreshToken: str
    expiresIn: int


class UpdateUserResponse(BaseModel):
    """Модель ответа при обновлении пользователя"""
    email: str
    fullName: str
    verified: bool
    banned: bool
    roles: List[str]
    createdAt: str

    class Config:
        use_enum_values = True