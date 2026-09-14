from fastapi import HTTPException

from app.services.user_service import get_user_by_id


def get_user_or_404(user_id: int):
    """Obtiene un usuario o genera un error 404 si no existe."""

    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user