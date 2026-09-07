from fastapi import APIRouter, HTTPException, Query
from app.schemas.user_schema import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Base de datos temporal en memoria
users_db = [
    {
        "id": 1,
        "name": "Kelly",
        "email": "kelly@example.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Carlos",
        "email": "carlos@example.com",
        "role": "support",
        "is_active": True
    },
    {
        "id": 3,
        "name": "Ana",
        "email": "ana@example.com",
        "role": "user",
        "is_active": False
    }
]


@router.get("/", response_model=list[UserResponse])
def get_users(
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None)
):
    """Obtiene todos los usuarios y permite filtrarlos."""

    users = users_db

    if role is not None:
        users = [
            user for user in users
            if user["role"] == role
        ]

    if is_active is not None:
        users = [
            user for user in users
            if user["is_active"] == is_active
        ]

    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Obtiene un usuario mediante su ID."""

    for user in users_db:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    """Registra un nuevo usuario."""

    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    new_user = {
        "id": len(users_db) + 1,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

    users_db.append(new_user)

    return new_user