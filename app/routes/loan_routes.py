from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User
from app.schemas.loan_schema import (
    LoanCreate,
    LoanDetailResponse,
    LoanResponse,
)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


# GET /loans/details
@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Listar préstamos con información relacionada",
    description="Obtiene los préstamos utilizando joins con usuarios y dispositivos.",
    response_description="Lista detallada de préstamos."
)
def get_loan_details(
    db: Session = Depends(get_db)
):
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
            Device.brand
        )
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
    )

    result = db.execute(query)

    return result.mappings().all()


# GET /loans
@router.get(
    "/",
    response_model=list[LoanResponse],
    summary="Listar préstamos",
    description="Obtiene todos los préstamos y permite aplicar filtros.",
    response_description="Lista de préstamos registrados."
)
def get_loans(
    status_filter: str | None = Query(
        default=None,
        alias="status"
    ),
    user_email: str | None = Query(default=None),
    device_type: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = (
        select(Loan)
        .join(User)
        .join(Device)
    )

    if status_filter:
        query = query.where(
            Loan.status == status_filter
        )

    if user_email:
        query = query.where(
            User.email.ilike(f"%{user_email}%")
        )

    if device_type:
        query = query.where(
            Device.device_type.ilike(f"%{device_type}%")
        )

    return db.scalars(query).all()


# GET /loans/{loan_id}
@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Consultar préstamo",
    description="Obtiene un préstamo mediante su ID.",
    response_description="Información del préstamo."
)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    loan = db.get(
        Loan,
        loan_id
    )

    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado"
        )

    return loan


# POST /loans
@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Registra un préstamo y cambia el dispositivo a no disponible.",
    response_description="Préstamo creado correctamente."
)
def create_loan(
    loan_data: LoanCreate,
    db: Session = Depends(get_db)
):
    user = db.get(
        User,
        loan_data.user_id
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    device = db.get(
        Device,
        loan_data.device_id
    )

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )

    if not device.is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El dispositivo no está disponible"
        )

    active_loan = db.scalar(
        select(Loan).where(
            Loan.device_id == loan_data.device_id,
            Loan.status == "active"
        )
    )

    if active_loan:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El dispositivo ya tiene un préstamo activo"
        )

    loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        loan_date=datetime.utcnow(),
        status="active"
    )

    device.is_available = False

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan


# PATCH /loans/{loan_id}/return
@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Registra la devolución y vuelve a habilitar el dispositivo.",
    response_description="Préstamo devuelto correctamente."
)
def return_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    loan = db.get(
        Loan,
        loan_id
    )

    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado"
        )

    if loan.status != "active":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El préstamo ya fue devuelto"
        )

    device = db.get(
        Device,
        loan.device_id
    )

    loan.return_date = datetime.utcnow()
    loan.status = "returned"

    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)

    return loan