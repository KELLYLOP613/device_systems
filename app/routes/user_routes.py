from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserPatch
)

from app.services.user_service import (
    get_all_users,
    create_user,
    email_exists,
    update_user,
    update_user_partial,
    delete_user
)

from app.dependencies.user_dependencies import get_user_or_404

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Obtener todos los usuarios",
    description="Obtiene la lista de usuarios y permite filtrarla por rol y estado.",
    response_description="Lista de usuarios registrados."
)
def get_users(
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None)
):
    users = get_all_users()

    if role is not None:
        users = [user for user in users if user["role"] == role]

    if is_active is not None:
        users = [user for user in users if user["is_active"] == is_active]

    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Busca un usuario específico utilizando su identificador.",
    response_description="Información del usuario encontrado."
)
def get_user(user=Depends(get_user_or_404)):
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Registra un nuevo usuario en el sistema.",
    response_description="Usuario creado correctamente."
)
def create_new_user(user: UserCreate):
    for existing_user in get_all_users():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    return create_user(user)

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza todos los datos de un usuario existente.",
    response_description="Usuario actualizado correctamente."
)
def update_existing_user(
    user_data: UserUpdate,
    user=Depends(get_user_or_404)
):
    if email_exists(user_data.email, exclude_user_id=user["id"]):
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    return update_user(user["id"], user_data)

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente",
    description="Actualiza únicamente los campos enviados del usuario.",
    response_description="Usuario actualizado correctamente."
)
def patch_existing_user(
    user_data: UserPatch,
    user=Depends(get_user_or_404)
):
    update_data = user_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar"
        )

    if "email" in update_data:
        if email_exists(
            update_data["email"],
            exclude_user_id=user["id"]
        ):
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    return update_user_partial(user["id"], user_data)

@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Eliminar usuario",
    description="Elimina un usuario existente.",
    response_description="Usuario eliminado correctamente."
)
def delete_existing_user(
    user=Depends(get_user_or_404)
):
    delete_user(user["id"])
    return Response(status_code=204)