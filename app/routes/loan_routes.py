from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.loan_dependencies import get_loan_or_404
from app.schemas.loan_schema import (
    LoanCreate,
    LoanDetailResponse,
    LoanResponse,
)
from app.services.device_service import get_device_by_id
from app.services.loan_service import (
    create_loan,
    device_has_active_loan,
    get_all_loans,
    get_loan_details,
    return_loan,
)
from app.services.user_service import get_user_by_id

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
def list_loan_details(
    db: Session = Depends(get_db)
):
    return get_loan_details(db)


# GET /loans
@router.get(
    "/",
    response_model=list[LoanResponse],
    summary="Listar préstamos",
    description="Obtiene todos los préstamos y permite aplicar filtros.",
    response_description="Lista de préstamos registrados."
)
def list_loans(
    status_filter: str | None = Query(
        default=None,
        alias="status"
    ),
    user_email: str | None = Query(default=None),
    device_type: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return get_all_loans(
        db,
        status_filter=status_filter,
        user_email=user_email,
        device_type=device_type,
    )


# GET /loans/{loan_id}
@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Consultar préstamo",
    description="Obtiene un préstamo mediante su ID.",
    response_description="Información del préstamo."
)
def get_loan(
    loan=Depends(get_loan_or_404),
):
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
def create_new_loan(
    loan_data: LoanCreate,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db, loan_data.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    device = get_device_by_id(db, loan_data.device_id)

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

    if device_has_active_loan(db, loan_data.device_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El dispositivo ya tiene un préstamo activo"
        )

    return create_loan(db, loan_data, device)


# PATCH /loans/{loan_id}/return
@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Registra la devolución y vuelve a habilitar el dispositivo.",
    response_description="Préstamo devuelto correctamente."
)
def return_existing_loan(
    loan=Depends(get_loan_or_404),
    db: Session = Depends(get_db)
):
    if loan.status != "active":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El préstamo ya fue devuelto"
        )

    device = get_device_by_id(db, loan.device_id)

    return return_loan(db, loan, device)
