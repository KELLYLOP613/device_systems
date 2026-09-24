from sqlalchemy.orm import Session

from app.auth.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.user_model import User


def get_user_by_email(
    db: Session,
    email: str
) -> User | None:
    """Busca un usuario por su correo electrónico."""
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def register_user(
    db: Session,
    name: str,
    email: str,
    password: str,
    role: str
) -> User:
    """Registra un nuevo usuario almacenando solo el hash."""

    hashed_password = get_password_hash(password)

    user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        role=role,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> User | None:
    """Valida las credenciales del usuario."""

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not user.hashed_password:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user


def create_user_token(user: User) -> str:
    """Genera un JWT para el usuario autenticado."""

    return create_access_token(
        data={
            "sub": user.email,
            "role": user.role,
        }
    )