from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User


def get_loan_details(db: Session):
    """Obtiene los préstamos combinando información de usuario y dispositivo."""

    query = (
        select(
            Loan.id,
            Loan.loan_date,
            Loan.return_date,
            Loan.status,
            User.id.label("user_id"),
            User.name.label("user_name"),
            User.email.label("user_email"),
            Device.id.label("device_id"),
            Device.name.label("device_name"),
            Device.serial_number,
            Device.device_type,
            Device.brand,
        )
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
    )

    result = db.execute(query)

    return result.mappings().all()


def get_all_loans(
    db: Session,
    status_filter: str | None = None,
    user_email: str | None = None,
    device_type: str | None = None,
):
    """Obtiene los préstamos aplicando los filtros opcionales."""

    query = select(Loan).join(User).join(Device)

    if status_filter:
        query = query.where(Loan.status == status_filter)

    if user_email:
        query = query.where(User.email.ilike(f"%{user_email}%"))

    if device_type:
        query = query.where(Device.device_type.ilike(f"%{device_type}%"))

    return db.scalars(query).all()


def get_loan_by_id(db: Session, loan_id: int):
    """Busca un préstamo por su ID."""

    return db.get(Loan, loan_id)


def device_has_active_loan(db: Session, device_id: int):
    """Comprueba si el dispositivo ya tiene un préstamo activo."""

    query = select(Loan).where(
        Loan.device_id == device_id,
        Loan.status == "active",
    )

    return db.scalar(query) is not None


def create_loan(db: Session, loan_data, device: Device):
    """Crea un préstamo y marca el dispositivo como no disponible."""

    loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        loan_date=datetime.utcnow(),
        status="active",
    )

    device.is_available = False

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan


def return_loan(db: Session, loan: Loan, device: Device | None):
    """Registra la devolución de un préstamo y libera el dispositivo."""

    loan.return_date = datetime.utcnow()
    loan.status = "returned"

    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)

    return loan
