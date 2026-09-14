from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        description="Nombre del usuario"
    )
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool = True


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        description="Nombre del usuario"
    )
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool


class UserPatch(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        description="Nombre del usuario"
    )
    email: EmailStr | None = None
    role: Literal["admin", "support", "user"] | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int