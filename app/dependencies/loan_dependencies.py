from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.services.loan_service import get_loan_by_id


def get_loan_or_404(
    loan_id: int,
    db: Session = Depends(get_db),
):
    """Obtiene un préstamo de la base de datos o genera un error 404."""

    loan = get_loan_by_id(db, loan_id)

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Préstamo no encontrado",
        )

    return loan
