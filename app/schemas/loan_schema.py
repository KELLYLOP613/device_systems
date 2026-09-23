from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LoanCreate(BaseModel):
    user_id: int
    device_id: int


class LoanUpdate(BaseModel):
    status: str | None = None
    return_date: datetime | None = None


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: datetime | None
    status: str

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(BaseModel):
    id: int
    loan_date: datetime
    return_date: datetime | None
    status: str

    user_id: int
    user_name: str
    user_email: str

    device_id: int
    device_name: str
    serial_number: str
    device_type: str
    brand: str | None

    model_config = ConfigDict(from_attributes=True)