from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.device_dependencies import get_device_or_404
from app.schemas.device_schema import (
    DeviceCreate,
    DeviceResponse,
    DeviceUpdate,
)
from app.services.device_service import (
    create_device,
    delete_device,
    get_all_devices,
    serial_number_exists,
    update_device,
    update_device_partial,
)

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.get(
    "/",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    description="Obtiene todos los dispositivos y permite aplicar filtros.",
    response_description="Lista de dispositivos registrados."
)
def get_devices(
    device_type: str | None = Query(default=None),
    is_available: bool | None = Query(default=None),
    brand: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return get_all_devices(
        db,
        device_type=device_type,
        is_available=is_available,
        brand=brand,
        search=search,
    )


@router.get(
    "/{device_id}/loans",
    summary="Consultar historial de un dispositivo",
    description="Obtiene todos los préstamos históricos de un dispositivo.",
    response_description="Historial de préstamos del dispositivo."
)
def get_device_loans(
    device=Depends(get_device_or_404),
):
    return device.loans


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Consultar dispositivo",
    description="Obtiene un dispositivo mediante su ID.",
    response_description="Información del dispositivo."
)
def get_device(
    device=Depends(get_device_or_404),
):
    return device


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo.",
    response_description="Dispositivo creado correctamente."
)
def create_new_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db)
):
    if serial_number_exists(db, device_data.serial_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un dispositivo con ese número de serie"
        )

    return create_device(db, device_data)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo",
    description="Actualiza completamente los datos de un dispositivo."
)
def update_existing_device(
    device_data: DeviceCreate,
    device=Depends(get_device_or_404),
    db: Session = Depends(get_db)
):
    if serial_number_exists(
        db,
        device_data.serial_number,
        exclude_device_id=device.id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe otro dispositivo con ese número de serie"
        )

    return update_device(db, device, device_data)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar parcialmente dispositivo",
    description="Actualiza uno o varios campos del dispositivo."
)
def patch_existing_device(
    device_data: DeviceUpdate,
    device=Depends(get_device_or_404),
    db: Session = Depends(get_db)
):
    update_data = device_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar"
        )

    if "serial_number" in update_data:
        if serial_number_exists(
            db,
            update_data["serial_number"],
            exclude_device_id=device.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro dispositivo con ese número de serie"
            )

    return update_device_partial(db, device, device_data)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo registrado."
)
def delete_existing_device(
    device=Depends(get_device_or_404),
    db: Session = Depends(get_db)
):
    delete_device(db, device)
    return None
