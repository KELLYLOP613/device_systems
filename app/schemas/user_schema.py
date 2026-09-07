from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserBase(BaseModel):
    """Modelo base con los datos de un usuario."""

    name: str = Field(
        ...,
        min_length=3,
        description="Nombre del usuario"
    )

    email: EmailStr

    role: Literal["admin", "support", "user"]

    is_active: bool = True


class UserCreate(UserBase):
    """Modelo utilizado para registrar un nuevo usuario."""
    pass


class UserResponse(UserBase):
    """Modelo utilizado para las respuestas de la API."""

    id: int