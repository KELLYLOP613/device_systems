from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies.auth_dependency import get_current_active_user
from app.rate_limiter import limiter

from app.auth.auth_service import (
    authenticate_user,
    create_user_token,
    get_user_by_email,
    register_user,
)
from app.dependencies.database_dependency import get_db
from app.schemas.auth_schema import (
    AuthUserResponse,
    Token,
    UserRegister,
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=AuthUserResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("3/minute")
def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Registra un nuevo usuario."""

    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )

    return register_user(
        db=db,
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        role=user_data.role,
    )


@router.post(
    "/login",
    response_model=Token
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Autentica un usuario y genera un JWT."""

    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está inactivo"
        )

    access_token = create_user_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get(
    "/me",
    response_model=AuthUserResponse
)
def get_me(
    current_user=Depends(get_current_active_user)
):
    """Obtiene los datos del usuario autenticado."""

    return current_user