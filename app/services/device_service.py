from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.device_model import Device


def get_all_devices(
    db: Session,
    device_type: str | None = None,
    is_available: bool | None = None,
    brand: str | None = None,
    search: str | None = None,
):
    """Obtiene los dispositivos aplicando los filtros opcionales."""

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
                Device.brand.ilike(search_term),
            )
        )

    return db.scalars(query).all()


def get_device_by_id(db: Session, device_id: int):
    """Busca un dispositivo por su ID."""

    return db.get(Device, device_id)


def serial_number_exists(
    db: Session,
    serial_number: str,
    exclude_device_id: int | None = None,
):
    """Comprueba si un número de serie ya está registrado."""

    query = select(Device).where(Device.serial_number == serial_number)

    if exclude_device_id is not None:
        query = query.where(Device.id != exclude_device_id)

    return db.scalar(query) is not None


def create_device(db: Session, device_data):
    """Crea un nuevo dispositivo en la base de datos."""

    device = Device(
        name=device_data.name,
        serial_number=device_data.serial_number,
        device_type=device_data.device_type,
        brand=device_data.brand,
        is_available=True,
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return device


def update_device(db: Session, device: Device, device_data):
    """Actualiza completamente un dispositivo."""

    device.name = device_data.name
    device.serial_number = device_data.serial_number
    device.device_type = device_data.device_type
    device.brand = device_data.brand

    db.commit()
    db.refresh(device)

    return device


def update_device_partial(db: Session, device: Device, update_data):
    """Actualiza parcialmente un dispositivo."""

    data = update_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(device, field, value)

    db.commit()
    db.refresh(device)

    return device


def delete_device(db: Session, device: Device):
    """Elimina un dispositivo de la base de datos."""

    db.delete(device)
    db.commit()

    return device
