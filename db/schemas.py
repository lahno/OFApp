import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class DTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageDTO(DTO):
    message: str
    status: bool


class AccountDTO(DTO):
    email: EmailStr
    password: Optional[str] = None
    status: bool

    # Проверка пароля
    @classmethod
    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError("Пароль должен содержать как минимум 8 символов")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль должен содержать как минимум одну заглавную букву")
        if not re.search(r"[a-z]", value):
            raise ValueError("Пароль должен содержать как минимум одну строчную букву")
        if not re.search(r"[0-9]", value):
            raise ValueError("Пароль должен содержать как минимум одну цифру")
        if not re.search(r"[@$!%*?&]", value):
            raise ValueError(
                "Пароль должен содержать как минимум один специальный символ (@$!%*?&)"
            )
        return value


class UserDTO(DTO):
    username: str
