from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        description="Nombre del usuario"
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        description="Contraseña segura"
    )

    role: Literal["admin", "support", "user"] = "user"

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if any(char.isspace() for char in value):
            raise ValueError(
                "La contraseña no puede contener espacios"
            )

        if not any(char.isupper() for char in value):
            raise ValueError(
                "La contraseña debe contener al menos una mayúscula"
            )

        if not any(char.islower() for char in value):
            raise ValueError(
                "La contraseña debe contener al menos una minúscula"
            )

        if not any(char.isdigit() for char in value):
            raise ValueError(
                "La contraseña debe contener al menos un número"
            )

        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        description="Contraseña del usuario"
    )


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None


class AuthUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)