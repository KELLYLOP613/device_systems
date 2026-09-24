# API REST de Gestión de Usuarios, Dispositivos y Préstamos - device_systems

## GA1-220501096-01-AA1-EV11

### FastAPI Seguridad: Autenticación, Middleware, CORS, Rate Limiting y Validación Avanzada

---

# Información del proyecto

**Programa:** Tecnólogo en Análisis y Desarrollo de Software (ADSO)

**Entidad:** Servicio Nacional de Aprendizaje - SENA

**Proyecto:** `device_systems`

**Actividad:** GA1-220501096-01-AA1-EV11

**Tecnologías principales:** FastAPI + SQLAlchemy + Alembic + JWT

**Lenguaje:** Python 3.13

**Base de datos:** SQLite

**Autor:** Kelly Lopera

---

# Descripción

`device_systems` es una API REST desarrollada con **FastAPI** para la gestión de usuarios, dispositivos y préstamos de dispositivos.

Esta versión corresponde a la evolución del proyecto desarrollado en las actividades anteriores, incorporando funcionalidades de seguridad y autenticación.

En esta etapa se implementan:

* Autenticación mediante JWT.
* Registro de usuarios.
* Inicio de sesión mediante OAuth2.
* Protección de rutas mediante tokens.
* Control de acceso basado en roles.
* Validación avanzada de contraseñas mediante Pydantic.
* Hash seguro de contraseñas mediante bcrypt.
* Middleware personalizado.
* Identificación única de solicitudes.
* Medición del tiempo de procesamiento.
* CORS.
* Rate limiting.
* Protección de operaciones según el rol del usuario.
* Variables de entorno para la configuración de seguridad.
* Migraciones mediante Alembic.
* Gestión de usuarios, dispositivos y préstamos.
* Consultas relacionadas mediante `JOIN`.
* Manejo de errores HTTP.
* Documentación automática mediante Swagger/OpenAPI.

La aplicación utiliza una base de datos SQLite almacenada en:

```text
device_systems.db
```

La estructura de la base de datos se administra mediante **Alembic**.

El archivo `.env` se mantiene fuera del repositorio mediante `.gitignore` para evitar publicar información sensible.

---

# Objetivo general

Desarrollar una API REST segura con FastAPI que permita gestionar usuarios, dispositivos y préstamos, incorporando autenticación mediante JWT, control de acceso por roles, validación avanzada, middleware personalizado, CORS, rate limiting y migraciones con Alembic.

---

# Objetivos específicos

* Implementar autenticación mediante JWT.
* Implementar registro e inicio de sesión de usuarios.
* Utilizar OAuth2 para la autenticación.
* Proteger endpoints mediante dependencias de FastAPI.
* Implementar control de acceso basado en roles.
* Validar contraseñas mediante Pydantic.
* Almacenar contraseñas utilizando hashes bcrypt.
* Implementar middleware personalizado.
* Generar identificadores únicos para las solicitudes.
* Medir el tiempo de procesamiento de las peticiones.
* Configurar CORS.
* Implementar límites de solicitudes mediante rate limiting.
* Utilizar SQLAlchemy como ORM.
* Implementar migraciones mediante Alembic.
* Gestionar usuarios, dispositivos y préstamos.
* Utilizar relaciones entre modelos.
* Realizar consultas utilizando `JOIN`.
* Aplicar filtros mediante parámetros de consulta.
* Implementar reglas de negocio.
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
* **Pydantic v2**
* **Email-validator**
* **SQLite**
* **python-jose**
* **Passlib**
* **bcrypt**
* **SlowAPI**
* **python-multipart**
* **python-dotenv**
* **Swagger/OpenAPI**
* **ReDoc**
* **Git**
* **GitHub**
* **uv** para la gestión del entorno y dependencias

---

# Estructura del proyecto

```text
device_systems/
├── alembic/
│   ├── versions/
│   │   ├── e549a8fe9960_create_devices_and_loans_tables.py
│   │   └── cea33c79f65d_add_authentication_fields_to_users.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── app/
│   ├── main.py
│   │
│   ├── auth/
│   │   ├── auth_routes.py
│   │   ├── auth_service.py
│   │   └── security.py
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
│   │   ├── loan_schema.py
│   │   └── auth_schema.py
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
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── database_dependency.py
│   │   ├── user_dependencies.py
│   │   ├── device_dependencies.py
│   │   ├── loan_dependencies.py
│   │   └── auth_dependency.py
│   │
│   ├── middlewares/
│   │   └── request_middleware.py
│   │
│   └── rate_limiter.py 
│
├── evidencias/
├── .env.example
├── .gitignore
├── .python-version
├── alembic.ini
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

> El archivo `.env` contiene configuración local y no debe publicarse en GitHub.

---

# Arquitectura de la aplicación

El proyecto mantiene una separación de responsabilidades:

```text
Cliente
   ↓
FastAPI / Routes
   ↓
Dependencies
   ↓
Schemas Pydantic
   ↓
Services
   ↓
SQLAlchemy
   ↓
Models
   ↓
SQLite
```

Para las operaciones protegidas se incorpora el flujo de autenticación:

```text
Cliente
   ↓
Login
   ↓
JWT
   ↓
Authorization: Bearer
   ↓
Auth Dependency
   ↓
Validación del usuario
   ↓
Validación del rol
   ↓
Endpoint protegido
```

---

# Modelos de datos

En el proyecto se trabajan tres modelos principales:

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

| Campo             | Tipo     | Restricción        |
| ----------------- | -------- | ------------------ |
| `id`              | Integer  | Clave primaria     |
| `name`            | String   | No nulo            |
| `email`           | String   | Único y no nulo    |
| `hashed_password` | String   | Hash de contraseña |
| `role`            | String   | Rol del usuario    |
| `is_active`       | Boolean  | Estado del usuario |
| `created_at`      | DateTime | Fecha de creación  |

La contraseña no se almacena en texto plano. Se almacena mediante un hash generado con bcrypt.

El modelo mantiene la relación:

```python
loans = relationship(
    "Loan",
    back_populates="user"
)
```

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

| Campo           | Tipo     | Restricción             |
| --------------- | -------- | ----------------------- |
| `id`            | Integer  | Clave primaria          |
| `name`          | String   | No nulo                 |
| `serial_number` | String   | Único y no nulo         |
| `device_type`   | String   | No nulo                 |
| `brand`         | String   | Opcional                |
| `is_available`  | Boolean  | Disponible inicialmente |
| `created_at`    | DateTime | Fecha de creación       |

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

Relaciones:

```text
user_id → users.id
device_id → devices.id
```

---

# Autenticación y seguridad

La autenticación se encuentra organizada en:

```text
app/auth/
```

Componentes principales:

```text
auth_routes.py
auth_service.py
security.py
```

La API utiliza:

* OAuth2.
* JWT.
* `python-jose`.
* Passlib.
* bcrypt.
* Dependencias de FastAPI.

---

# Registro de usuarios

Endpoint:

```text
POST /auth/register
```

Permite registrar un nuevo usuario.

Ejemplo:

```json
{
    "name": "Maria Test",
    "email": "maria.test@example.com",
    "password": "Maria1234",
    "role": "user"
}
```

La contraseña se valida antes de crear el usuario.

Después se genera un hash mediante bcrypt.

La respuesta no expone el campo `hashed_password`.

Respuesta exitosa:

```text
201 Created
```

---

# Validación de contraseñas

Las contraseñas utilizan validación avanzada mediante Pydantic.

La contraseña debe:

* Tener mínimo 8 caracteres.
* Contener al menos una letra mayúscula.
* Contener al menos una letra minúscula.
* Contener al menos un número.
* No contener espacios.

Ejemplo de contraseña válida:

```text
Maria1234
```

Una contraseña que no cumpla estas condiciones genera:

```text
422 Unprocessable Entity
```

---

# Inicio de sesión

Endpoint:

```text
POST /auth/login
```

El inicio de sesión utiliza OAuth2 Password Flow.

En Swagger se utilizan:

```text
username = correo electrónico
password = contraseña
```

Si las credenciales son correctas, la API genera un JWT.

Respuesta:

```json
{
    "access_token": "JWT_GENERADO",
    "token_type": "bearer"
}
```

---

# JWT

Los tokens JWT contienen información relacionada con el usuario autenticado.

El token incluye:

```text
sub
role
exp
```

Donde:

* `sub` identifica al usuario mediante su correo.
* `role` contiene el rol del usuario.
* `exp` establece la fecha de expiración del token.

El algoritmo utilizado es:

```text
HS256
```

La duración del token se configura mediante:

```text
ACCESS_TOKEN_EXPIRE_MINUTES
```

---

# Variables de entorno

La configuración de seguridad se administra mediante variables de entorno.

Archivo:

```text
.env
```

Ejemplo:

```text
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

También se incluye:

```text
.env.example
```

como plantilla para configurar el proyecto.

El archivo `.env` se encuentra incluido en `.gitignore` y no debe subirse al repositorio.

---

# Obtener usuario autenticado

Endpoint:

```text
GET /auth/me
```

Requiere un token JWT válido.

Con autenticación correcta devuelve la información del usuario actual.

Sin token:

```text
401 Unauthorized
```

Con token inválido:

```text
401 Unauthorized
```

Si el usuario está inactivo:

```text
403 Forbidden
```

---

# Roles y permisos

Los roles disponibles son:

```text
admin
support
user
```

Se implementaron dependencias para controlar el acceso:

```text
get_current_user
get_current_active_user
require_admin
require_admin_or_support
```

---

# Control de acceso

Las operaciones sensibles requieren autenticación y permisos específicos.

Por ejemplo:

```text
admin
   ↓
Operaciones administrativas

admin / support
   ↓
Operaciones de soporte

user
   ↓
Operaciones permitidas para usuarios autenticados
```

Una operación que requiere permisos administrativos y es solicitada por un usuario sin el rol correspondiente devuelve:

```text
403 Forbidden
```

Ejemplo comprobado:

```text
Usuario Maria (role=user)
        ↓
POST /devices/
        ↓
403 Forbidden
```

También se comprobó:

```text
Usuario Maria (role=user)
        ↓
GET /loans/details
        ↓
403 Forbidden
```

Mientras que un usuario administrador autenticado pudo acceder:

```text
Admin Test (role=admin)
        ↓
GET /loans/details
        ↓
200 OK
```

---

# Middleware personalizado

El middleware se encuentra en:

```text
app/middlewares/request_middleware.py
```

El middleware registra información de cada solicitud y agrega encabezados personalizados.

Los encabezados utilizados son:

```text
X-App-Name
X-Process-Time
X-Request-ID
```

Ejemplo:

```text
X-App-Name: device_systems
X-Process-Time: 0.0031
X-Request-ID: d55f8497-...
```

---

# X-Request-ID

Cada solicitud recibe un identificador único.

Si el cliente envía:

```text
X-Request-ID
```

se conserva el identificador.

Si no lo envía, el middleware genera automáticamente un UUID.

Esto facilita la identificación y seguimiento de solicitudes.

---

# Tiempo de procesamiento

El middleware mide el tiempo de procesamiento de cada solicitud utilizando:

```python
time.perf_counter()
```

El resultado se devuelve mediante:

```text
X-Process-Time
```

---

# CORS

La aplicación utiliza `CORSMiddleware` de FastAPI.

Los orígenes configurados para desarrollo son:

```text
http://localhost:5173
http://localhost:3000
```

Configuración principal:

```python
allow_origins=[
    "http://localhost:5173",
    "http://localhost:3000",
]

allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

Se comprobó mediante una solicitud HTTP que un origen permitido recibe:

```text
access-control-allow-origin
access-control-allow-credentials
```

---

# Rate Limiting

La aplicación utiliza **SlowAPI** para limitar la cantidad de solicitudes.

Configuraciones implementadas:

| Endpoint              |                Límite |
| --------------------- | --------------------: |
| `POST /auth/login`    |  5 solicitudes/minuto |
| `POST /auth/register` |  3 solicitudes/minuto |
| `GET /users`          | 30 solicitudes/minuto |
| `POST /loans/`        | 10 solicitudes/minuto |

Cuando se supera el límite configurado, la API responde:

```text
429 Too Many Requests
```

---

# Pruebas de Rate Limiting

Se realizaron pruebas sobre:

```text
POST /auth/login
```

Resultado:

```text
429 Too Many Requests
```

También se comprobó:

```text
POST /auth/register
```

Resultado:

```text
429 Too Many Requests
```

Y:

```text
GET /users
```

Resultado:

```text
429 Too Many Requests
```

Finalmente se comprobó el límite configurado para:

```text
POST /loans/
```

Resultado:

```text
429 Too Many Requests
```

---

# Asociaciones entre modelos

Las relaciones implementadas son:

```text
User 1 ───────── N Loan

Device 1 ─────── N Loan
```

Un usuario puede tener múltiples préstamos.

Un dispositivo puede aparecer en múltiples préstamos históricos.

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

Las migraciones existentes incluyen la creación de dispositivos y préstamos y la incorporación de los campos necesarios para autenticación.

---

# Migración de autenticación

Para incorporar el sistema de autenticación se creó una migración adicional:

```text
cea33c79f65d_add_authentication_fields_to_users.py
```

Esta migración agrega el campo:

```text
hashed_password
```

a la tabla:

```text
users
```

La migración fue aplicada mediante:

```bash
uv run alembic upgrade head
```

---

# Verificación de migraciones

Para consultar la versión actual:

```bash
uv run alembic current
```

Para comprobar si existen cambios pendientes:

```bash
uv run alembic check
```

El proyecto utiliza Alembic para administrar los cambios del esquema de base de datos.

---

# Endpoints principales

| Método | Endpoint                     | Descripción                                   |
| ------ | ---------------------------- | --------------------------------------------- |
| GET    | `/`                          | Verificar funcionamiento de la API            |
| POST   | `/auth/register`             | Registrar usuario                             |
| POST   | `/auth/login`                | Iniciar sesión                                |
| GET    | `/auth/me`                   | Obtener usuario autenticado                   |
| GET    | `/users`                     | Obtener usuarios                              |
| GET    | `/users/{user_id}`           | Obtener usuario                               |
| POST   | `/users`                     | Crear usuario                                 |
| PUT    | `/users/{user_id}`           | Actualizar usuario                            |
| PATCH  | `/users/{user_id}`           | Actualizar parcialmente                       |
| DELETE | `/users/{user_id}`           | Eliminar usuario                              |
| GET    | `/users/{user_id}/loans`     | Historial de préstamos                        |
| GET    | `/devices`                   | Obtener dispositivos                          |
| GET    | `/devices/{device_id}`       | Obtener dispositivo                           |
| POST   | `/devices`                   | Crear dispositivo                             |
| PUT    | `/devices/{device_id}`       | Actualizar dispositivo                        |
| PATCH  | `/devices/{device_id}`       | Actualizar parcialmente                       |
| DELETE | `/devices/{device_id}`       | Eliminar dispositivo                          |
| GET    | `/devices/{device_id}/loans` | Historial del dispositivo                     |
| GET    | `/loans`                     | Obtener préstamos                             |
| GET    | `/loans/{loan_id}`           | Obtener préstamo                              |
| POST   | `/loans/`                    | Crear préstamo                                |
| PATCH  | `/loans/{loan_id}/return`    | Registrar devolución                          |
| GET    | `/loans/details`             | Obtener préstamos con información relacionada |

---

# Gestión de dispositivos

## GET - Obtener dispositivos

Endpoint:

```text
GET /devices/
```

Permite consultar los dispositivos registrados.

También permite utilizar filtros.

---

# Filtros de dispositivos

## Filtrar por tipo

```text
GET /devices/?device_type=laptop
```

## Filtrar por disponibilidad

```text
GET /devices/?is_available=true
```

También:

```text
GET /devices/?is_available=false
```

## Filtrar por marca

```text
GET /devices/?brand=Lenovo
```

## Buscar dispositivos

```text
GET /devices/?search=Lenovo
```

## Combinar filtros

```text
GET /devices/?device_type=laptop&is_available=true
```

---

# Crear dispositivo

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

Esta operación requiere autenticación y permisos de administrador o soporte.

---

# Actualizar dispositivo

Endpoint:

```text
PUT /devices/{device_id}
```

Permite actualizar la información de un dispositivo.

Esta operación requiere permisos de administrador o soporte.

---

# Eliminar dispositivo

Endpoint:

```text
DELETE /devices/{device_id}
```

Esta operación requiere permisos de administrador.

Respuesta exitosa:

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

# Crear préstamo

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

La operación requiere un usuario autenticado.

Durante la creación se realizan las siguientes validaciones:

1. Se verifica que el usuario exista.
2. Se verifica que el dispositivo exista.
3. Se verifica que el dispositivo esté disponible.
4. Se verifica que no exista otro préstamo activo para el dispositivo.
5. Se crea el préstamo.
6. El estado se establece como `active`.
7. El dispositivo pasa a estar no disponible.

---

# Consultas con JOIN

El endpoint:

```text
GET /loans/details
```

combina información de:

```text
loans
users
devices
```

La consulta utiliza relaciones entre los modelos y `JOIN`.

Permite obtener información como:

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

Esta operación requiere permisos de administrador o soporte.

---

# Devolución de un dispositivo

Endpoint:

```text
PATCH /loans/{loan_id}/return
```

Al realizar la devolución:

1. Se verifica que el préstamo exista.
2. Se verifica que esté activo.
3. Se registra la fecha de devolución.
4. El estado cambia a `returned`.
5. El dispositivo vuelve a estar disponible.

Esta operación requiere permisos de administrador o soporte.

---

# Manejo de errores

La API utiliza códigos HTTP para representar diferentes situaciones.

| Código | Situación                               |
| ------ | --------------------------------------- |
| 200    | Operación exitosa                       |
| 201    | Registro creado                         |
| 204    | Eliminación exitosa                     |
| 400    | Solicitud inválida                      |
| 401    | No autenticado o credenciales inválidas |
| 403    | Sin permisos suficientes                |
| 404    | Recurso no encontrado                   |
| 409    | Conflicto con una regla de negocio      |
| 422    | Error de validación                     |
| 429    | Límite de solicitudes excedido          |

---

# Swagger y OpenAPI

FastAPI genera automáticamente documentación interactiva.

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

Desde Swagger se pueden probar:

* Auth.
* Users.
* Devices.
* Loans.
* Parámetros de ruta.
* Parámetros de consulta.
* Cuerpos JSON.
* Autenticación OAuth2.
* Tokens JWT.
* Filtros.
* Códigos de respuesta.

---

# ReDoc

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

## 2. Crear el entorno virtual

Utilizando `uv`:

```bash
uv venv
```

## 3. Activar el entorno virtual

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 4. Instalar dependencias

```bash
uv sync
```

También puede utilizarse:

```bash
uv pip install -r requirements.txt
```

---

# Configuración de variables de entorno

Crear un archivo:

```text
.env
```

Con valores similares a:

```text
SECRET_KEY=una-clave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

No publicar el archivo `.env` en GitHub.

Para facilitar la configuración se incluye:

```text
.env.example
```

---

# Migraciones después de clonar el proyecto

Después de instalar las dependencias:

```bash
uv run alembic upgrade head
```

Para verificar la versión:

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

Las pruebas funcionales fueron realizadas mediante Swagger UI y solicitudes HTTP.

## Autenticación

Se verificó:

* Registro de usuario.
* Hash de contraseña.
* Login mediante OAuth2.
* Generación de JWT.
* Acceso a `/auth/me`.
* Acceso sin token.
* Token inválido.
* Control de usuario activo.
* Protección de rutas.

## Validación Pydantic

Se verificó:

* Email válido.
* Longitud mínima de contraseña.
* Mayúsculas.
* Minúsculas.
* Números.
* Restricción de espacios.
* Roles permitidos.
* Respuesta `422` para datos inválidos.

## Roles

Se verificó:

* Usuario con rol `user` rechazado en operaciones administrativas.
* Usuario administrador autorizado.
* Respuestas `403 Forbidden`.
* Acceso exitoso con rol administrativo.

## Middleware

Se verificó la generación de:

```text
X-App-Name
X-Process-Time
X-Request-ID
```

## CORS

Se verificó el acceso desde un origen permitido:

```text
http://localhost:5173
```

## Rate Limiting

Se verificó:

* Login: `429`.
* Registro: `429`.
* Usuarios: `429`.
* Préstamos: `429`.

## Alembic

Se verificó:

* Inicialización de Alembic.
* Generación de migraciones.
* Aplicación de `upgrade head`.
* Consulta de versión.
* Comprobación de migraciones.

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
* Control de permisos.

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
* Filtrar por rango de fechas.
* Consultar información mediante `JOIN`.
* Consultar historial de usuario.
* Consultar historial de dispositivo.
* Registrar devolución.
* Cambiar el estado del préstamo.
* Volver a habilitar el dispositivo después de la devolución.
* Control de permisos.

---

# Evidencias

A continuación se presentan las evidencias de las pruebas realizadas durante la implementación de seguridad, autenticación, autorización, middleware, CORS, rate limiting, validación avanzada y migraciones de la API `device_systems`.

## 1. Estructura del proyecto

Se evidencia la estructura del proyecto `device_systems`, incluyendo los módulos de autenticación, dependencias, middleware, modelos, rutas, esquemas, servicios, migraciones y archivos de configuración.

![Estructura del proyecto](evidencias/EV11-estructura-proyecto.jpeg)

## 2. Migración Alembic aplicada

Se evidencia la ejecución y aplicación de las migraciones de la base de datos mediante Alembic, verificando la revisión actual del proyecto.

![Migración Alembic aplicada](evidencias/EV11-alembic-migracion-aplicada.jpeg)

## 3. Registro de usuario exitoso

Se verifica el registro correcto de un nuevo usuario mediante `POST /auth/register`, utilizando validación de datos y almacenamiento seguro de la contraseña mediante hash.

![Registro de usuario exitoso](evidencias/EV11-registro-usuario-exitoso.jpeg)

## 4. Login y generación del token

Se verifica el inicio de sesión mediante `POST /auth/login` utilizando OAuth2 Password Flow y la generación correcta de un token JWT.

![Login y token generado](evidencias/EV11-login-token-generado.jpeg)

## 5. Swagger/OpenAPI con OAuth2

Se evidencia la configuración de OAuth2 en la documentación interactiva Swagger/OpenAPI, permitiendo autenticar las solicitudes protegidas mediante usuario y contraseña.

![Swagger OpenAPI con OAuth2](evidencias/EV11-swagger-oauth2.jpeg)

## 6. Usuario autenticado mediante `/auth/me`

Se verifica que un usuario autenticado pueda consultar su propia información mediante `GET /auth/me`.

![Usuario autenticado](evidencias/EV11-auth-me-usuario-autenticado.jpeg)

## 7. Acceso a `/auth/me` sin token

Se verifica que el endpoint protegido rechace una solicitud sin token de autenticación, devolviendo `401 Unauthorized`.

![Auth me sin token](evidencias/EV11-auth-me-sin-token-401.jpeg)

## 8. Token inválido

Se verifica el rechazo de un token JWT inválido mediante una respuesta `401 Unauthorized`.

![Token inválido](evidencias/EV11-token-invalido-401.jpeg)

## 9. Consulta de usuarios autenticada

Se verifica el acceso autorizado al endpoint `GET /users` utilizando un usuario autenticado.

![Usuarios autenticado](evidencias/EV11-users-autenticado-200.jpeg)

## 10. Restricción por rol de usuario

Se verifica que un usuario con rol `user` no pueda ejecutar operaciones que requieren permisos superiores, obteniendo `403 Forbidden`.

![Restricción de rol usuario](evidencias/EV11-role-user-forbidden-403.jpeg)

## 11. Restricción de acceso a detalles de préstamos

Se verifica que un usuario con rol `user` no pueda acceder a `GET /loans/details`, endpoint protegido para administradores y soporte.

![Restricción de loans details](evidencias/EV11-loans-details-role-user-403.jpeg)

## 12. Restricción para devolver préstamos

Se verifica que un usuario con rol `user` no pueda ejecutar la operación de devolución de un préstamo mediante `PATCH /loans/{loan_id}/return`.

![Restricción devolución de préstamo](evidencias/EV11-loan-return-role-user-403.jpeg)

## 13. Middleware personalizado

Se verifica el funcionamiento del middleware personalizado mediante los encabezados agregados a las respuestas:

* `X-App-Name`
* `X-Process-Time`
* `X-Request-ID`

![Middleware personalizado](evidencias/EV11-middleware-custom-headers.jpeg)

## 14. Rate limiting en login

Se verifica el límite de solicitudes configurado para `POST /auth/login`. Al superar el límite establecido, la API responde con `429 Too Many Requests`.

![Rate limiting login](evidencias/EV11-rate-limit-login-429.jpeg)

## 15. Rate limiting en consulta de usuarios

Se verifica el límite de solicitudes configurado para `GET /users`. Al superar el número permitido de solicitudes, se obtiene una respuesta `429 Too Many Requests`.

![Rate limiting usuarios](evidencias/EV11-rate-limit-users-429.jpeg)

## 16. Rate limiting en registro

Se verifica el límite de solicitudes configurado para `POST /auth/register`. Al superar el límite establecido, la API responde con `429 Too Many Requests`.

![Rate limiting registro](evidencias/EV11-rate-limit-register-429.jpeg)

## 17. Configuración de CORS

Se verifica que la API permita solicitudes provenientes del origen configurado `http://localhost:5173`, incluyendo las credenciales cuando corresponde.

![Configuración CORS](evidencias/EV11-cors-origen-permitido.jpeg)

## 18. Validación avanzada con Pydantic

Se verifica la validación avanzada de contraseñas mediante Pydantic v2. Una contraseña que no cumple las condiciones establecidas genera una respuesta `422 Unprocessable Entity`.

![Validación Pydantic de contraseña](evidencias/EV11-pydantic-password-validation-422.jpeg)

## 19. Acceso autorizado con rol administrador

Se verifica que un usuario con rol `admin` pueda acceder correctamente al endpoint protegido `GET /loans/details`, obteniendo una respuesta `200 OK`.

![Acceso administrador a loans details](evidencias/EV11-admin-loans-details-200.jpeg)

## Pruebas adicionales realizadas

Además de las evidencias mostradas anteriormente, durante las pruebas de la API también se verificó:

* Registro de usuarios con diferentes roles.
* Inicio de sesión mediante OAuth2 y generación de tokens JWT.
* Protección de endpoints mediante `Bearer Token`.
* Validación de usuarios activos.
* Restricción de operaciones según los roles `admin`, `support` y `user`.
* Rate limiting para `POST /loans/`.
* Validación de correo electrónico mediante `EmailStr`.
* Validación de longitud y complejidad de contraseñas.
* Exclusión del campo `hashed_password` de las respuestas de la API.
* Persistencia de los usuarios mediante SQLAlchemy y SQLite.
* Migración de la base de datos mediante Alembic.
* Configuración de variables sensibles mediante `.env`.
* Uso de `.env.example` como referencia para la configuración del proyecto.

---

# Flujo de autenticación

```text
POST /auth/register
        ↓
Validar datos con Pydantic
        ↓
Validar contraseña
        ↓
Generar hash bcrypt
        ↓
Guardar usuario
```

Para iniciar sesión:

```text
POST /auth/login
        ↓
Validar credenciales
        ↓
Generar JWT
        ↓
Cliente recibe access_token
        ↓
Authorization: Bearer <token>
        ↓
Ruta protegida
        ↓
Validar usuario
        ↓
Validar rol
        ↓
Ejecutar operación
```

---

# Flujo de seguridad

```text
Solicitud HTTP
      ↓
Middleware
      ↓
Request ID
      ↓
Medición de tiempo
      ↓
Rate Limiting
      ↓
CORS
      ↓
Autenticación JWT
      ↓
Validación del usuario
      ↓
Validación del rol
      ↓
Endpoint
```

---

# Conceptos aplicados

Durante el desarrollo de esta actividad se aplicaron:

* APIs REST.
* FastAPI.
* Pydantic v2.
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
* Reglas de negocio.
* Códigos de estado HTTP.
* Manejo de excepciones.
* Dependency Injection.
* `Depends()`.
* OAuth2.
* JWT.
* bcrypt.
* Hash de contraseñas.
* Control de acceso basado en roles.
* Middleware.
* CORS.
* Rate limiting.
* Variables de entorno.
* Swagger UI.
* OpenAPI.
* ReDoc.
* Git.
* GitHub.
* Gestión de dependencias con `uv`.

---

# Consideraciones de seguridad

El proyecto incorpora diferentes mecanismos para mejorar la seguridad de la API:

* Las contraseñas no se almacenan en texto plano.
* Las contraseñas se almacenan mediante hashes bcrypt.
* Las rutas protegidas requieren autenticación.
* Se implementan permisos según roles.
* Los tokens JWT tienen tiempo de expiración.
* La clave secreta se configura mediante variables de entorno.
* `.env` está excluido del repositorio.
* Se implementa CORS con orígenes específicos para desarrollo.
* Se implementa rate limiting para reducir solicitudes excesivas.
* Se generan identificadores de solicitud mediante middleware.
* Se validan los datos de entrada mediante Pydantic.
* Los errores se gestionan mediante códigos HTTP.

---

# Git y control de versiones

El desarrollo de EV11 se realiza mediante una rama independiente:

```text
device_systems_security
```

El flujo de trabajo previsto es:

```text
device_systems_security
          ↓
       develop
          ↓
         main
```

Antes de realizar el commit y el push se verifica:

* README actualizado.
* Evidencias incluidas.
* Código funcionando.
* `.env` excluido.
* `requirements.txt` actualizado.
* Estado de Git revisado.

---

# Reflexión

El desarrollo de esta actividad permitió incorporar mecanismos de seguridad a la API `device_systems`.

La implementación de **JWT y OAuth2** permitió comprender cómo autenticar usuarios y proteger endpoints mediante tokens.

La incorporación de **bcrypt** permitió almacenar las contraseñas utilizando hashes en lugar de texto plano.

El control de acceso mediante roles permitió diferenciar las operaciones disponibles para usuarios, soporte y administradores.

También se implementó un **middleware personalizado** para identificar las solicitudes, registrar información y medir el tiempo de procesamiento.

La configuración de **CORS** permitió controlar los orígenes autorizados para acceder a la API.

Finalmente, el uso de **rate limiting** permitió establecer límites de solicitudes y generar respuestas `429 Too Many Requests` cuando se supera el límite configurado.

Las pruebas realizadas mediante Swagger y solicitudes HTTP permitieron comprobar el funcionamiento de los mecanismos de autenticación, autorización, validación y protección implementados.

---

# Conclusión

La actividad **GA1-220501096-01-AA1-EV11** permitió evolucionar la API `device_systems` incorporando diferentes mecanismos de seguridad.

Se implementaron:

* Registro de usuarios.
* Autenticación OAuth2.
* Tokens JWT.
* Hash de contraseñas con bcrypt.
* Validación avanzada mediante Pydantic.
* Protección de rutas.
* Control de acceso basado en roles.
* Middleware personalizado.
* Identificación de solicitudes.
* Medición del tiempo de procesamiento.
* Configuración CORS.
* Rate limiting.
* Migraciones mediante Alembic.
* Gestión de usuarios.
* Gestión de dispositivos.
* Gestión de préstamos.
* Relaciones entre modelos.
* Consultas mediante `JOIN`.
* Filtros y reglas de negocio.
* Manejo de errores HTTP.
* Documentación mediante Swagger/OpenAPI.
* Pruebas funcionales de seguridad.

La versión resultante proporciona una base más segura para continuar ampliando el proyecto `device_systems`.

---

# Autora

**Kelly Lopera**

Tecnólogo en Análisis y Desarrollo de Software

SENA

Proyecto académico desarrollado como parte de la formación en ADSO.