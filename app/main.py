from fastapi import FastAPI
from app.database.connection import Base, engine
from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

app = FastAPI(
    title="Device Systems API",
    description=(
        "API REST para la gestión de usuarios del sistema "
        "device_systems. Incluye operaciones CRUD, validación "
        "de datos, manejo de errores y Dependency Injection."
    ),
    version="2.0.0",
    contact={
        "name": "Kelly Lopera",
        "email": "johalopera15@gmail.com"
    }
)


app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)
@app.get("/")
def root():
    return {
        "message": "Device Systems API funcionando",
        "version": "2.0.0"
    }


@app.middleware("http")
async def add_custom_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0.0"
    return response