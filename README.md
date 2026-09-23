# API REST de Gestión de Usuarios, Dispositivos y Préstamos - device_systems

## GA1-220501096-01-AA1-EV10

### FastAPI Avanzado: Migraciones con Alembic, Asociaciones de Modelos y Consultas con Joins

---

# Información del proyecto

**Programa:** Tecnólogo en Análisis y Desarrollo de Software (ADSO)

**Entidad:** Servicio Nacional de Aprendizaje - SENA

**Proyecto:** `device_systems`

**Actividad:** GA1-220501096-01-AA1-EV10

**Tecnologías principales:** FastAPI + SQLAlchemy + Alembic

**Lenguaje:** Python 3.13

**Base de datos:** SQLite

**Autor:** Kelly Lopera

---

# Descripción

`device_systems` es una API REST desarrollada con **FastAPI** para la gestión de usuarios, dispositivos y préstamos de dispositivos.

Esta versión corresponde a la evolución del proyecto desarrollado en la actividad **GA1-220501096-01-AA1-EV09**.

En esta etapa se incorpora:

* Gestión de dispositivos.
* Gestión de préstamos.
* Relaciones entre modelos SQLAlchemy.
* Migraciones de base de datos mediante Alembic.
* Consultas utilizando `JOIN`.
* Filtros avanzados.
* Historial de préstamos.
* Control de disponibilidad de dispositivos.
* Validación de usuarios y dispositivos.
* Manejo de reglas de negocio.
* Manejo de errores HTTP.
* Documentación automática mediante Swagger/OpenAPI.

La aplicación utiliza una base de datos SQLite almacenada en:

```text
device_systems.db
```

La estructura de la base de datos es administrada mediante **Alembic**, por lo que las tablas no se crean directamente mediante `Base.metadata.create_all()`.

El archivo de base de datos se mantiene fuera del repositorio cuando está incluido en el `.gitignore`.

---

# Objetivo general

Desarrollar una API REST con FastAPI y SQLAlchemy que permita gestionar usuarios, dispositivos y préstamos, incorporando migraciones con Alembic, asociaciones entre modelos, consultas con joins, filtros avanzados, validaciones y manejo de reglas de negocio.

---

# Objetivos específicos

* Utilizar SQLAlchemy como ORM.
* Implementar migraciones mediante Alembic.
* Crear modelos relacionados para usuarios, dispositivos y préstamos.
* Establecer relaciones entre los modelos mediante `relationship()`.
* Utilizar claves foráneas mediante `ForeignKey`.
* Implementar CRUD para dispositivos.
* Registrar préstamos de dispositivos.
* Controlar la disponibilidad de los dispositivos.
* Registrar devoluciones.
* Consultar el historial de préstamos.
* Realizar consultas utilizando `JOIN`.
* Implementar filtros mediante parámetros de consulta.
* Filtrar préstamos por estado.
* Filtrar préstamos por correo electrónico del usuario.
* Filtrar préstamos por tipo de dispositivo.
* Validar la existencia de usuarios y dispositivos.
* Manejar errores HTTP.
* Documentar la API mediante Swagger/OpenAPI.
* Realizar pruebas funcionales mediante Swagger UI.
* Gestionar el proyecto mediante Git y GitHub.

---

# Tecnologías utilizadas

* **Python 3.13**
* **FastAPI**
* **Uvicorn**
* **SQLAlchemy**
* **Alembic**
* **Pydantic**
* **Email-validator**
* **SQLite**
* **Swagger/OpenAPI**
* **ReDoc**
* **Git**
* **GitHub**
* **uv** para la gestión del entorno y dependencias

---

# Estructura del proyecto

```text
device_systems/
│
├── alembic/
│   ├── versions/
│   │   └── e549a8fe9960_create_devices_and_loans_tables.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user_model.py
│   │   ├── device_model.py
│   │   └── loan_model.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   ├── device_schema.py
│   │   └── loan_schema.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   ├── device_routes.py
│   │   └── loan_routes.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── device_service.py
│   │   └── loan_service.py
│   │
│   └── dependencies/
│       ├── __init__.py
│       ├── database_dependency.py
│       ├── user_dependencies.py
│       ├── device_dependencies.py
│       └── loan_dependencies.py
│
├── evidencias/
├── src/
├── .gitignore
├── .python-version
├── alembic.ini
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

---

# Arquitectura de la aplicación

El proyecto mantiene una separación de responsabilidades:

```text
Cliente
   ↓
FastAPI / Routes
   ↓
Schemas Pydantic
   ↓
SQLAlchemy
   ↓
Models
   ↓
SQLite
```

Para las operaciones que requieren lógica adicional se utilizan servicios y dependencias.

La estructura general permite separar:

```text
routes
   ↓
services
   ↓
models
   ↓
database
```

Los esquemas Pydantic se utilizan para validar los datos de entrada y salida.

---

# Modelos de datos

En esta versión se trabajan tres modelos principales:

```text
User
  │
  │ 1
  │
  │ N
Loan
  │
  │ N
  │
  │ 1
Device
```

Un usuario puede tener múltiples préstamos.

Un dispositivo puede tener múltiples préstamos históricos.

Cada préstamo pertenece a un usuario y a un dispositivo.

---

# Modelo User

El modelo de usuarios se encuentra en:

```text
app/models/user_model.py
```

La tabla utilizada es:

```text
users
```

Campos principales:

| Campo        | Tipo     | Restricción                 |
| ------------ | -------- | --------------------------- |
| `id`         | Integer  | Clave primaria              |
| `name`       | String   | No nulo                     |
| `email`      | String   | Único y no nulo             |
| `role`       | String   | No nulo                     |
| `is_active`  | Boolean  | Valor predeterminado `True` |
| `created_at` | DateTime | Fecha de creación           |

El modelo también contiene la relación:

```python
loans = relationship(
    "Loan",
    back_populates="user"
)
```

Esta relación permite acceder a los préstamos asociados a un usuario.

---

# Modelo Device

El modelo de dispositivos se encuentra en:

```text
app/models/device_model.py
```

La tabla utilizada es:

```text
devices
```

Campos:

| Campo           | Tipo     | Restricción                 |
| --------------- | -------- | --------------------------- |
| `id`            | Integer  | Clave primaria              |
| `name`          | String   | No nulo                     |
| `serial_number` | String   | Único y no nulo             |
| `device_type`   | String   | No nulo                     |
| `brand`         | String   | Opcional                    |
| `is_available`  | Boolean  | Valor predeterminado `True` |
| `created_at`    | DateTime | Fecha de creación           |

El modelo contiene la relación:

```python
loans = relationship(
    "Loan",
    back_populates="device"
)
```

Esto permite consultar el historial de préstamos de un dispositivo.

---

# Modelo Loan

El modelo de préstamos se encuentra en:

```text
app/models/loan_model.py
```

La tabla utilizada es:

```text
loans
```

Campos:

| Campo         | Tipo     | Restricción         |
| ------------- | -------- | ------------------- |
| `id`          | Integer  | Clave primaria      |
| `user_id`     | Integer  | Clave foránea       |
| `device_id`   | Integer  | Clave foránea       |
| `loan_date`   | DateTime | Fecha del préstamo  |
| `return_date` | DateTime | Opcional            |
| `status`      | String   | Estado del préstamo |

Las claves foráneas son:

```text
user_id → users.id
device_id → devices.id
```

El modelo contiene las relaciones:

```python
user = relationship(
    "User",
    back_populates="loans"
)

device = relationship(
    "Device",
    back_populates="loans"
)
```

---

# Asociaciones entre modelos

Las relaciones implementadas son:

## User → Loan

Un usuario puede tener varios préstamos:

```text
User 1 ───────── N Loan
```

Se implementa mediante:

```python
loans = relationship(
    "Loan",
    back_populates="user"
)
```

---

## Device → Loan

Un dispositivo puede aparecer en múltiples préstamos históricos:

```text
Device 1 ───────── N Loan
```

Se implementa mediante:

```python
loans = relationship(
    "Loan",
    back_populates="device"
)
```

---

## Loan → User

Cada préstamo pertenece a un usuario:

```python
user = relationship(
    "User",
    back_populates="loans"
)
```

---

## Loan → Device

Cada préstamo pertenece a un dispositivo:

```python
device = relationship(
    "Device",
    back_populates="loans"
)
```

---

# Alembic

Alembic se utiliza para administrar las migraciones de la base de datos.

La configuración principal se encuentra en:

```text
alembic.ini
```

La configuración de los modelos y metadatos se encuentra en:

```text
alembic/env.py
```

En `env.py` se importa:

```python
from app.database.connection import Base

from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan

target_metadata = Base.metadata
```

La importación de los modelos permite que Alembic conozca las tablas y relaciones existentes.

---

# Inicialización de Alembic

Alembic se inicializó mediante:

```bash
uv run alembic init alembic
```

Esto generó la estructura:

```text
alembic/
├── versions/
├── env.py
├── README
└── script.py.mako
```

También se generó:

```text
alembic.ini
```

---

# Creación de una migración

Para detectar los cambios realizados en los modelos se utilizó:

```bash
uv run alembic revision --autogenerate -m "create devices and loans tables"
```

Alembic generó la migración:

```text
e549a8fe9960_create_devices_and_loans_tables.py
```

La migración contiene la creación de las tablas:

```text
devices
loans
```

También contiene las claves foráneas correspondientes.

---

# Aplicación de la migración

La migración se aplicó mediante:

```bash
uv run alembic upgrade head
```

El resultado confirmó la ejecución de la migración:

```text
Running upgrade -> e549a8fe9960, create devices and loans tables
```

---

# Verificación de la migración

La versión actual de Alembic se puede consultar mediante:

```bash
uv run alembic current
```

También se verificó que los modelos y las migraciones estuvieran sincronizados mediante:

```bash
uv run alembic check
```

El resultado obtenido fue:

```text
No new upgrade operations detected.
```

Esto confirma que no existen cambios pendientes de migración respecto a los modelos actuales.

---

# Importante: creación de tablas

En la versión anterior se utilizaba:

```python
Base.metadata.create_all(bind=engine)
```

En EV10 este mecanismo ya no se utiliza para crear las tablas.

La estructura de la base de datos se administra mediante **Alembic**.

Esto permite controlar los cambios del esquema mediante versiones de migración.

---

# Esquemas Pydantic

## DeviceCreate

Se utiliza para crear dispositivos.

Campos principales:

```text
name
serial_number
device_type
brand
```

---

## DeviceUpdate

Permite modificar los datos del dispositivo.

Campos:

```text
name
serial_number
device_type
brand
is_available
```

Los campos son opcionales para permitir actualizaciones parciales.

---

## DeviceResponse

Define la estructura de respuesta de los dispositivos.

Incluye:

```text
id
name
serial_number
device_type
brand
is_available
created_at
```

---

# Esquemas de préstamos

## LoanCreate

Permite registrar un préstamo mediante:

```text
user_id
device_id
```

---

## LoanUpdate

Permite representar información actualizable de un préstamo:

```text
status
return_date
```

---

## LoanResponse

Representa la información básica de un préstamo:

```text
id
user_id
device_id
loan_date
return_date
status
```

---

## LoanDetailResponse

Se utiliza para devolver información combinada del préstamo, usuario y dispositivo.

Incluye:

```text
id
loan_date
return_date
status

user_id
user_name
user_email

device_id
device_name
serial_number
device_type
brand
```

---

# Endpoints disponibles

| Método | Endpoint                     | Descripción                                   |
| ------ | ---------------------------- | --------------------------------------------- |
| GET    | `/`                          | Verificar funcionamiento de la API            |
| GET    | `/users`                     | Obtener usuarios                              |
| GET    | `/users/{user_id}`           | Obtener usuario                               |
| POST   | `/users`                     | Crear usuario                                 |
| PUT    | `/users/{user_id}`           | Actualizar usuario                            |
| PATCH  | `/users/{user_id}`           | Actualizar parcialmente                       |
| DELETE | `/users/{user_id}`           | Eliminar usuario                              |
| GET    | `/users/{user_id}/loans`     | Historial de préstamos del usuario            |
| GET    | `/devices`                   | Obtener dispositivos                          |
| GET    | `/devices/{device_id}`       | Obtener dispositivo                           |
| POST   | `/devices`                   | Crear dispositivo                             |
| PUT    | `/devices/{device_id}`       | Actualizar dispositivo                        |
| PATCH  | `/devices/{device_id}`       | Actualizar parcialmente                       |
| DELETE | `/devices/{device_id}`       | Eliminar dispositivo                          |
| GET    | `/devices/{device_id}/loans` | Historial del dispositivo                     |
| GET    | `/loans`                     | Obtener préstamos                             |
| GET    | `/loans/{loan_id}`           | Obtener préstamo                              |
| POST   | `/loans`                     | Crear préstamo                                |
| PATCH  | `/loans/{loan_id}/return`    | Registrar devolución                          |
| GET    | `/loans/details`             | Obtener préstamos con información relacionada |

---

# Gestión de dispositivos

## GET - Obtener dispositivos

Endpoint:

```text
GET /devices/
```

Permite consultar todos los dispositivos registrados.

También permite utilizar filtros.

---

# Filtros de dispositivos

## Filtrar por tipo

```text
GET /devices/?device_type=laptop
```

---

## Filtrar por disponibilidad

```text
GET /devices/?is_available=true
```

También:

```text
GET /devices/?is_available=false
```

---

## Filtrar por marca

```text
GET /devices/?brand=Lenovo
```

---

## Buscar dispositivos

El parámetro `search` permite realizar una búsqueda sobre los datos del dispositivo.

Ejemplo:

```text
GET /devices/?search=Lenovo
```

---

## Combinar filtros

Los filtros pueden combinarse.

Ejemplo:

```text
GET /devices/?device_type=laptop&is_available=true
```

---

# POST - Crear dispositivo

Endpoint:

```text
POST /devices/
```

Ejemplo:

```json
{
    "name": "Laptop Lenovo",
    "serial_number": "LEN-001",
    "device_type": "laptop",
    "brand": "Lenovo"
}
```

Al crear un dispositivo:

```text
is_available = true
```

se establece como valor inicial.

El número de serie debe ser único.

---

# PUT - Actualizar dispositivo

Endpoint:

```text
PUT /devices/{device_id}
```

Permite actualizar completamente la información del dispositivo.

---

# PATCH - Actualizar dispositivo parcialmente

Endpoint:

```text
PATCH /devices/{device_id}
```

Permite modificar solamente los campos enviados.

---

# DELETE - Eliminar dispositivo

Endpoint:

```text
DELETE /devices/{device_id}
```

Si el dispositivo existe, se elimina.

Código exitoso:

```text
204 No Content
```

---

# Gestión de préstamos

Los préstamos relacionan:

```text
Usuario
   ↓
Préstamo
   ↓
Dispositivo
```

Para crear un préstamo deben existir tanto el usuario como el dispositivo.

Además, el dispositivo debe estar disponible.

---

# POST - Crear préstamo

Endpoint:

```text
POST /loans/
```

Ejemplo:

```json
{
    "user_id": 1,
    "device_id": 1
}
```

Durante la creación se realizan las siguientes validaciones:

1. Se verifica que el usuario exista.
2. Se verifica que el dispositivo exista.
3. Se verifica que el dispositivo esté disponible.
4. Se verifica que no exista otro préstamo activo para el dispositivo.
5. Se crea el préstamo.
6. El estado se establece como `active`.
7. El dispositivo pasa a estar no disponible.

Ejemplo de estado del dispositivo después del préstamo:

```text
is_available = false
```

---

# Dispositivo no disponible

Si se intenta prestar un dispositivo que ya está ocupado, la API responde:

```text
409 Conflict
```

Ejemplo:

```json
{
    "detail": "El dispositivo no está disponible"
}
```

Esto permite aplicar una regla de negocio para evitar préstamos simultáneos del mismo dispositivo.

---

# GET - Obtener préstamos

Endpoint:

```text
GET /loans/
```

Permite consultar los préstamos registrados.

---

# Filtro por estado

Para consultar préstamos activos:

```text
GET /loans/?status=active
```

Para consultar préstamos devueltos:

```text
GET /loans/?status=returned
```

---

# Filtro por correo del usuario

Se puede buscar un préstamo utilizando el correo electrónico del usuario:

```text
GET /loans/?user_email=kelly@example.com
```

La consulta utiliza el modelo `User` relacionado con `Loan`.

---

# Filtro por tipo de dispositivo

También es posible filtrar préstamos por tipo de dispositivo:

```text
GET /loans/?device_type=laptop
```

La consulta utiliza la relación entre `Loan` y `Device`.

---

# Consultas con JOIN

Una de las principales incorporaciones de EV10 es la utilización de consultas con `JOIN`.

El endpoint:

```text
GET /loans/details
```

combina información de las tablas:

```text
loans
users
devices
```

La consulta utiliza:

```python
select(...)
    .join(User, Loan.user_id == User.id)
    .join(Device, Loan.device_id == Device.id)
```

Esto permite obtener en una misma respuesta información como:

```text
Usuario
Correo
Dispositivo
Número de serie
Tipo de dispositivo
Marca
Fecha del préstamo
Estado
Fecha de devolución
```

---

# Ejemplo de respuesta de préstamos detallados

```json
[
    {
        "id": 1,
        "loan_date": "2026-09-22T20:00:00",
        "return_date": null,
        "status": "active",
        "user_id": 1,
        "user_name": "Kelly",
        "user_email": "kelly@example.com",
        "device_id": 1,
        "device_name": "Laptop Lenovo",
        "serial_number": "LEN-001",
        "device_type": "laptop",
        "brand": "Lenovo"
    }
]
```

La fecha mostrada depende del momento en que se creó el préstamo.

---

# Historial de préstamos de un usuario

Endpoint:

```text
GET /users/{user_id}/loans
```

Ejemplo:

```text
GET /users/1/loans
```

Permite consultar todos los préstamos asociados a un usuario.

La consulta utiliza la relación:

```text
User → Loan
```

Si el usuario no existe, se devuelve:

```text
404 Not Found
```

---

# Historial de préstamos de un dispositivo

Endpoint:

```text
GET /devices/{device_id}/loans
```

Ejemplo:

```text
GET /devices/1/loans
```

Permite consultar el historial de préstamos asociados a un dispositivo.

La consulta utiliza la relación:

```text
Device → Loan
```

---

# Devolución de un dispositivo

Endpoint:

```text
PATCH /loans/{loan_id}/return
```

Ejemplo:

```text
PATCH /loans/1/return
```

Al realizar la devolución:

1. Se verifica que el préstamo exista.
2. Se verifica que el préstamo esté activo.
3. Se registra la fecha de devolución.
4. El estado cambia de `active` a `returned`.
5. El dispositivo vuelve a estar disponible.

El resultado esperado es:

```text
status = returned
```

y:

```text
is_available = true
```

---

# Manejo de errores

La API utiliza códigos HTTP para representar diferentes situaciones.

| Código | Situación                          |
| ------ | ---------------------------------- |
| 200    | Operación exitosa                  |
| 201    | Registro creado                    |
| 204    | Eliminación exitosa                |
| 400    | Solicitud inválida                 |
| 404    | Recurso no encontrado              |
| 409    | Conflicto con una regla de negocio |
| 422    | Error de validación                |

---

# Errores de usuarios

Si el usuario no existe:

```text
404 Not Found
```

Respuesta:

```json
{
    "detail": "Usuario no encontrado"
}
```

---

# Errores de dispositivos

Si el dispositivo no existe:

```text
404 Not Found
```

Si el número de serie ya está registrado:

```text
400 Bad Request
```

---

# Errores de préstamos

Si el usuario no existe:

```text
404 Not Found
```

Si el dispositivo no existe:

```text
404 Not Found
```

Si el dispositivo no está disponible:

```text
409 Conflict
```

Si el dispositivo ya tiene un préstamo activo:

```text
409 Conflict
```

Si se intenta devolver un préstamo que ya fue devuelto:

```text
409 Conflict
```

---

# Swagger y OpenAPI

FastAPI genera automáticamente documentación interactiva.

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

Desde Swagger se pueden probar:

* Users
* Devices
* Loans
* Parámetros de ruta
* Parámetros de consulta
* Cuerpos JSON
* Filtros
* Joins
* Devoluciones
* Códigos de respuesta

---

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

ReDoc proporciona una presentación alternativa de la documentación OpenAPI.

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

Ingresar a la carpeta:

```bash
cd device_systems
```

---

## 2. Crear el entorno virtual

Utilizando `uv`:

```bash
uv venv
```

---

## 3. Activar el entorno virtual

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 4. Instalar las dependencias

```bash
uv sync
```

También puede utilizarse:

```bash
uv pip install -r requirements.txt
```

---

# Migraciones después de clonar el proyecto

Después de instalar las dependencias, se deben aplicar las migraciones:

```bash
uv run alembic upgrade head
```

Esto crea o actualiza las tablas según las migraciones disponibles.

Para verificar la versión actual:

```bash
uv run alembic current
```

---

# Ejecución del proyecto

Para iniciar el servidor:

```bash
uv run uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Pruebas realizadas

Las pruebas funcionales fueron realizadas mediante Swagger UI.

## Alembic

Se verificó:

* Inicialización de Alembic.
* Generación de migración mediante `--autogenerate`.
* Aplicación de `upgrade head`.
* Consulta de la versión actual.
* Verificación mediante `alembic check`.

---

## Usuarios

Se verificó:

* Obtener usuarios.
* Obtener usuario por ID.
* Crear usuario.
* Actualizar usuario.
* Actualizar parcialmente.
* Eliminar usuario.
* Filtros por rol.
* Filtros por estado.
* Validación de datos.
* Manejo de errores.

---

## Dispositivos

Se verificó:

* Crear dispositivo.
* Obtener dispositivos.
* Obtener dispositivo por ID.
* Filtrar por tipo.
* Filtrar por disponibilidad.
* Filtrar por marca.
* Realizar búsquedas.
* Actualizar dispositivo.
* Eliminar dispositivo.

---

## Préstamos

Se verificó:

* Crear préstamo.
* Consultar préstamos.
* Consultar préstamo por ID.
* Validar existencia del usuario.
* Validar existencia del dispositivo.
* Validar disponibilidad.
* Evitar préstamos simultáneos.
* Filtrar préstamos activos.
* Filtrar por correo del usuario.
* Filtrar por tipo de dispositivo.
* Consultar información mediante joins.
* Consultar historial de usuario.
* Consultar historial de dispositivo.
* Registrar devolución.
* Cambiar el estado del préstamo.
* Volver a habilitar el dispositivo después de la devolución.

---

# Evidencias

Las evidencias de la actividad se encuentran en:

```text
evidencias/
```

Entre las principales evidencias se incluyen:

```text
EV10_actualizar_disponibilidad.jpeg
EV10_consultar_dispositivo_id.jpeg
EV10_crear_dispositivo.jpeg
EV10_crear_prestamo.jpeg
EV10_devolucion_prestamo.jpeg
EV10_dispositivo_disponible_devolucion.jpeg
EV10_dispositivo_no_disponible.jpeg
EV10_filtro_device_type.jpeg
EV10_filtro_search.jpeg
EV10_filtro_status_active.jpeg
EV10_filtro_user_email.jpeg
EV10_historial_dispositivo.jpeg
EV10_historial_usuario.jpeg
EV10_join_prestamos_usuarios_dispositivos.jpeg
EV10_listar_dispositivos.jpeg
EV10_listar_prestamos.jpeg
EV10_validacion_dispositivo_no_disponible.jpeg
```

Estas evidencias permiten demostrar el funcionamiento de las migraciones, relaciones, joins, filtros y reglas de negocio implementadas.

---

# Flujo de un préstamo

El flujo principal de un préstamo es:

```text
POST /loans
      ↓
Validar usuario
      ↓
Validar dispositivo
      ↓
Comprobar disponibilidad
      ↓
Crear préstamo
      ↓
status = active
      ↓
is_available = false
```

---

# Flujo de devolución

```text
PATCH /loans/{loan_id}/return
              ↓
       Buscar préstamo
              ↓
       Verificar estado
              ↓
     Registrar return_date
              ↓
       status = returned
              ↓
     is_available = true
```

---

# Flujo de consultas con relaciones

Para consultar información relacionada:

```text
Loan
 │
 ├── User
 │    ├── name
 │    └── email
 │
 └── Device
      ├── name
      ├── serial_number
      ├── device_type
      └── brand
```

Esto permite obtener información de diferentes tablas utilizando `JOIN`.

---

# Conceptos aplicados

Durante el desarrollo de esta actividad se aplicaron:

* APIs REST.
* FastAPI.
* Pydantic.
* SQLAlchemy.
* ORM.
* SQLite.
* Alembic.
* Migraciones.
* Modelos relacionales.
* Claves primarias.
* Claves foráneas.
* `relationship()`.
* `back_populates`.
* CRUD.
* Métodos HTTP.
* Parámetros de ruta.
* Parámetros de consulta.
* Filtros.
* `select()`.
* `join()`.
* `where()`.
* `ilike()`.
* Consultas relacionadas.
* Joins entre tablas.
* Validación de datos.
* Reglas de negocio.
* Códigos de estado HTTP.
* Manejo de excepciones.
* Dependency Injection.
* `Depends()`.
* Sesiones de base de datos.
* Swagger UI.
* OpenAPI.
* ReDoc.
* Git.
* GitHub.
* Gestión de dependencias con `uv`.

---

# Ventajas de utilizar Alembic

La utilización de Alembic permite controlar los cambios realizados sobre la estructura de la base de datos.

Entre sus ventajas se encuentran:

* Versionar los cambios de la base de datos.
* Crear migraciones automáticamente.
* Aplicar migraciones de forma controlada.
* Actualizar la estructura de la base de datos.
* Mantener sincronizados los modelos y el esquema.
* Facilitar el trabajo colaborativo.
* Evitar depender de `create_all()` para modificar el esquema.

---

# Separación de responsabilidades

El proyecto utiliza diferentes componentes para organizar la aplicación:

```text
routes
   ↓
schemas
   ↓
SQLAlchemy
   ↓
models
   ↓
database
```

Las rutas manejan las solicitudes HTTP.

Los esquemas Pydantic validan la información.

Los modelos SQLAlchemy representan las tablas.

Alembic administra las migraciones.

La capa de base de datos administra las sesiones y conexión con SQLite.

---

# Git y control de versiones

El desarrollo de EV10 se realizó utilizando una rama independiente:

```text
device_systems_alembic_relaciones
```

Posteriormente los cambios fueron integrados mediante:

```text
device_systems_alembic_relaciones
              ↓
           develop
              ↓
             main
```

El commit principal de esta actividad es:

```text
d4131c4
```

Con el mensaje:

```text
Implementación de Alembic, relaciones y joins en FastAPI
```

Los cambios fueron publicados en GitHub en la rama `main`.

---

# Reflexión

El desarrollo de esta actividad permitió evolucionar el proyecto `device_systems` desde una API enfocada principalmente en la gestión de usuarios hacia una solución con diferentes entidades relacionadas.

La incorporación de **Alembic** permitió comprender cómo administrar los cambios de estructura de una base de datos mediante migraciones versionadas.

La creación de los modelos `Device` y `Loan` permitió aplicar relaciones entre entidades utilizando claves foráneas y `relationship()` de SQLAlchemy.

También fue posible comprender el uso de consultas con `JOIN`, las cuales permiten combinar información almacenada en diferentes tablas.

Los filtros implementados permitieron realizar consultas más específicas sobre los préstamos, utilizando información tanto del usuario como del dispositivo.

Finalmente, las pruebas mediante Swagger permitieron comprobar las reglas de negocio relacionadas con la disponibilidad de los dispositivos, la creación de préstamos y su posterior devolución.

---

# Conclusión

La actividad **GA1-220501096-01-AA1-EV10** permitió evolucionar la API `device_systems` mediante la incorporación de **Alembic, relaciones entre modelos, consultas con joins y filtros avanzados**.

Se implementaron:

* Migraciones con Alembic.
* Modelo `User`.
* Modelo `Device`.
* Modelo `Loan`.
* Relaciones entre usuarios y préstamos.
* Relaciones entre dispositivos y préstamos.
* Claves foráneas.
* CRUD de dispositivos.
* Registro de préstamos.
* Validación de disponibilidad.
* Devolución de dispositivos.
* Historial de préstamos.
* Consultas con `JOIN`.
* Filtros por estado.
* Filtros por correo del usuario.
* Filtros por tipo de dispositivo.
* Manejo de errores HTTP.
* Documentación mediante Swagger/OpenAPI.
* Pruebas funcionales de las principales operaciones.

La estructura resultante permite continuar ampliando el proyecto y facilita el mantenimiento de la API y de la base de datos.

---

# Autora

**Kelly Lopera**

Tecnólogo en Análisis y Desarrollo de Software

SENA

Proyecto académico desarrollado como parte de la formación en ADSO.
