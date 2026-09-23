from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.services.device_service import get_device_by_id


def get_device_or_404(
    device_id: int,
    db: Session = Depends(get_db),
):
    """Obtiene un dispositivo de la base de datos o genera un error 404."""

    device = get_device_by_id(db, device_id)

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado",
        )

    return device
