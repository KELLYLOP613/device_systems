from fastapi import APIRouter, Depends, HTTPException, Query, Response, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.dependencies.auth_dependency import get_current_active_user
from app.dependencies.database_dependency import get_db
from app.dependencies.user_dependencies import get_user_or_404
from app.rate_limiter import limiter
from app.schemas.user_schema import (
    UserCreate,
    UserPatch,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import (
    create_user,
    delete_user,
    email_exists,
    get_all_users,
    get_user_by_email,
    update_user,
    update_user_partial,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=list[UserResponse],
    summary="Obtener todos los usuarios",
    description="Obtiene los usuarios y permite filtrarlos por rol y estado.",
    response_description="Lista de usuarios registrados.",
)
@limiter.limit("30/minute")
def get_users(
    request: Request,
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return get_all_users(
        db,
        role=role,
        is_active=is_active,
    )

@router.get(
    "/{user_id}/loans",
    summary="Consultar préstamos de un usuario",
    description="Obtiene todos los préstamos asociados a un usuario.",
    response_description="Lista de préstamos del usuario."
)
def get_user_loans(
    user=Depends(get_user_or_404),
):
    return user.loans

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Busca un usuario específico utilizando su identificador.",
    response_description="Información del usuario encontrado.",
)
def get_user(
    user=Depends(get_user_or_404),
    current_user=Depends(get_current_active_user),
):
    return user


@router.post(
    "",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Registra un nuevo usuario en la base de datos.",
    response_description="Usuario creado correctamente.",
)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado",
        )

    try:
        return create_user(db, user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado",
        )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza todos los datos de un usuario existente.",
    response_description="Usuario actualizado correctamente.",
)
def update_existing_user(
    user_data: UserUpdate,
    user=Depends(get_user_or_404),
    db: Session = Depends(get_db),
):
    if email_exists(
        db,
        user_data.email,
        exclude_user_id=user.id,
    ):
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado",
        )

    try:
        return update_user(db, user, user_data)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado",
        )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente",
    description="Actualiza únicamente los campos enviados.",
    response_description="Usuario actualizado correctamente.",
)
def patch_existing_user(
    user_data: UserPatch,
    user=Depends(get_user_or_404),
    db: Session = Depends(get_db),
):
    update_data = user_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar",
        )

    if "email" in update_data:
        if email_exists(
            db,
            update_data["email"],
            exclude_user_id=user.id,
        ):
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado",
            )

    try:
        return update_user_partial(
            db,
            user,
            user_data,
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado",
        )


@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Eliminar usuario",
    description="Elimina un usuario existente de la base de datos.",
)
def delete_existing_user(
    user=Depends(get_user_or_404),
    db: Session = Depends(get_db),
):
    delete_user(db, user)
    return Response(status_code=204)

