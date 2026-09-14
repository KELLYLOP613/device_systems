from fastapi import FastAPI
from app.routes.user_routes import router as user_router


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