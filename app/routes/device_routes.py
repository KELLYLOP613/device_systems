from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.device_model import Device
from app.schemas.device_schema import (
    DeviceCreate,
    DeviceResponse,
    DeviceUpdate,
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
    query = select(Device)

    if device_type:
        query = query.where(Device.device_type == device_type)

    if is_available is not None:
        query = query.where(Device.is_available == is_available)

    if brand:
        query = query.where(Device.brand == brand)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Device.name.ilike(search_term),
                Device.serial_number.ilike(search_term),
                Device.device_type.ilike(search_term),
                Device.brand.ilike(search_term)
            )
        )

    return db.scalars(query).all()

@router.get(
    "/{device_id}/loans",
    summary="Consultar historial de un dispositivo",
    description="Obtiene todos los préstamos históricos de un dispositivo.",
    response_description="Historial de préstamos del dispositivo."
)
def get_device_loans(
    device_id: int,
    db: Session = Depends(get_db)
):
    device = db.get(Device, device_id)

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )

    return device.loans

@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Consultar dispositivo",
    description="Obtiene un dispositivo mediante su ID.",
    response_description="Información del dispositivo."
)
def get_device(
    device_id: int,
    db: Session = Depends(get_db)
):
    device = db.get(Device, device_id)

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )

    return device


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo.",
    response_description="Dispositivo creado correctamente."
)
def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db)
):
    existing_device = db.scalar(
        select(Device).where(
            Device.serial_number == device_data.serial_number
        )
    )

    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un dispositivo con ese número de serie"
        )

    device = Device(
        name=device_data.name,
        serial_number=device_data.serial_number,
        device_type=device_data.device_type,
        brand=device_data.brand,
        is_available=True
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return device


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo",
    description="Actualiza completamente los datos de un dispositivo."
)
def update_device(
    device_id: int,
    device_data: DeviceCreate,
    db: Session = Depends(get_db)
):
    device = db.get(Device, device_id)

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )

    duplicate = db.scalar(
        select(Device).where(
            Device.serial_number == device_data.serial_number,
            Device.id != device_id
        )
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe otro dispositivo con ese número de serie"
        )

    device.name = device_data.name
    device.serial_number = device_data.serial_number
    device.device_type = device_data.device_type
    device.brand = device_data.brand

    db.commit()
    db.refresh(device)

    return device


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar parcialmente dispositivo",
    description="Actualiza uno o varios campos del dispositivo."
)
def patch_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db)
):
    device = db.get(Device, device_id)

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )

    update_data = device_data.model_dump(exclude_unset=True)

    if "serial_number" in update_data:
        duplicate = db.scalar(
            select(Device).where(
                Device.serial_number == update_data["serial_number"],
                Device.id != device_id
            )
        )

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro dispositivo con ese número de serie"
            )

    for field, value in update_data.items():
        setattr(device, field, value)

    db.commit()
    db.refresh(device)

    return device


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo registrado."
)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db)
):
    device = db.get(Device, device_id)

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )

    db.delete(device)
    db.commit()

    return None
