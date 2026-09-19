# API REST de Gestión de Usuarios - device_systems

## GA1-220501096-01-AA1-EV09

### FastAPI con SQLAlchemy: Persistencia de Datos y CRUD sobre Base de Datos

---

## Información del proyecto

**Programa:** Tecnólogo en Análisis y Desarrollo de Software (ADSO)

**Entidad:** Servicio Nacional de Aprendizaje - SENA

**Proyecto:** `device_systems`

**Actividad:** GA1-220501096-01-AA1-EV09

**Tecnología principal:** FastAPI + SQLAlchemy

**Lenguaje:** Python 3.13

**Base de datos:** SQLite

**Autor:** Kelly Lopera

---

# Descripción

`device_systems` es una API REST desarrollada con **FastAPI** para la gestión de usuarios de un sistema.

Esta versión corresponde a la evolución del proyecto desarrollado en las actividades anteriores. En esta etapa se reemplaza el almacenamiento de usuarios en memoria por una **base de datos relacional SQLite**, utilizando **SQLAlchemy como ORM**.

La API permite realizar un CRUD completo de usuarios mediante:

- Consulta de usuarios.
- Consulta de un usuario por ID.
- Creación de usuarios.
- Actualización completa mediante `PUT`.
- Actualización parcial mediante `PATCH`.
- Eliminación de usuarios mediante `DELETE`.
- Persistencia de datos mediante SQLite.
- Modelado de datos mediante SQLAlchemy.
- Validación de datos utilizando Pydantic.
- Validación de correos electrónicos.
- Validación de roles.
- Prevención de correos electrónicos duplicados.
- Manejo de errores HTTP.
- Dependency Injection mediante `Depends()`.
- Filtros por rol y estado de actividad.
- Ordenamiento de usuarios por nombre.
- Documentación automática mediante Swagger/OpenAPI.
- Documentación alternativa mediante ReDoc.

La información de los usuarios se almacena en el archivo:

```text
device_systems.db
```

Este archivo es generado automáticamente por SQLite al ejecutar la aplicación y contiene los datos persistidos de los usuarios.

El archivo de base de datos no forma parte de los archivos que se deben versionar en GitHub.

Esto permite que los datos permanezcan almacenados aunque se reinicie el servidor.

---

# Objetivos

## Objetivo general

Desarrollar una API REST utilizando FastAPI y SQLAlchemy que permita gestionar usuarios mediante operaciones CRUD sobre una base de datos SQLite, aplicando validaciones, restricciones, manejo de errores, Dependency Injection y documentación automática con Swagger/OpenAPI.

## Objetivos específicos

- Implementar una conexión entre FastAPI y una base de datos SQLite.
- Utilizar SQLAlchemy como ORM para el manejo de los datos.
- Crear un modelo relacional para los usuarios.
- Implementar operaciones `GET`, `POST`, `PUT`, `PATCH` y `DELETE`.
- Aplicar validaciones mediante Pydantic.
- Validar correos electrónicos.
- Validar los roles permitidos.
- Evitar registros con correos electrónicos duplicados.
- Implementar restricciones de integridad mediante SQLAlchemy.
- Utilizar Dependency Injection para administrar las sesiones de base de datos.
- Implementar filtros por rol y estado de actividad.
- Ordenar los usuarios por nombre.
- Manejar errores mediante `HTTPException` e `IntegrityError`.
- Documentar la API mediante Swagger/OpenAPI.
- Comprobar la persistencia de los datos después de reiniciar la aplicación.

---

# Tecnologías utilizadas

- **Python 3.13**
- **FastAPI**
- **Uvicorn**
- **SQLAlchemy**
- **Pydantic**
- **Email-validator**
- **SQLite**
- **Swagger/OpenAPI**
- **ReDoc**
- **Git**
- **GitHub**
- **uv** para la gestión del entorno y dependencias

---

# Estructura del proyecto

```text
device_systems/
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
│   │   └── user_model.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_routes.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   │
│   └── dependencies/
│       ├── __init__.py
│       ├── database_dependency.py
│       └── user_dependencies.py
│
├── evidencias/
├── src/
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

El archivo `device_systems.db` es generado automáticamente por SQLite al iniciar la aplicación. Contiene los datos persistidos de los usuarios y debe mantenerse fuera del repositorio si está incluido en el `.gitignore`.

---

# Descripción de los módulos

## `app/main.py`

Es el archivo principal de la aplicación.

Aquí se configura la instancia de FastAPI, la información de la API, los datos de contacto, las rutas y los encabezados personalizados.

También se inicializan las tablas de la base de datos mediante:

```python
Base.metadata.create_all(bind=engine)
```

El endpoint raíz es:

```text
GET /
```

---

## `app/database/connection.py`

Contiene la configuración de conexión con la base de datos SQLite.

La URL utilizada es:

```python
DATABASE_URL = "sqlite:///./device_systems.db"
```

También contiene:

- `engine`
- `SessionLocal`
- `Base`

Estos elementos permiten configurar SQLAlchemy y establecer la conexión con la base de datos.

---

## `app/models/user_model.py`

Contiene el modelo de SQLAlchemy correspondiente a la tabla `users`.

El modelo incluye los siguientes campos:

| Campo | Tipo | Restricción |
|---|---|---|
| `id` | Integer | Clave primaria |
| `name` | String | No nulo |
| `email` | String | Único y no nulo |
| `role` | String | No nulo |
| `is_active` | Boolean | Valor predeterminado `True` |
| `created_at` | DateTime | Fecha de creación |

La tabla utilizada en SQLite se denomina:

```text
users
```

---

# Modelo de usuario

El modelo SQLAlchemy se encuentra en:

```text
app/models/user_model.py
```

Su estructura representa los datos almacenados en la base de datos.

Ejemplo:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

La separación entre el modelo SQLAlchemy y los esquemas Pydantic permite diferenciar:

- La estructura utilizada para almacenar datos.
- La estructura utilizada para recibir y responder información mediante la API.

---

# Esquemas Pydantic

## `app/schemas/user_schema.py`

Contiene los esquemas utilizados para validar los datos enviados y devueltos por la API.

### `UserBase`

Modelo base de usuario.

Campos:

- `name`
- `email`
- `role`
- `is_active`

### `UserCreate`

Se utiliza para crear nuevos usuarios mediante `POST`.

### `UserUpdate`

Se utiliza para actualizar completamente un usuario mediante `PUT`.

Todos sus campos son obligatorios.

### `UserPatch`

Se utiliza para realizar actualizaciones parciales mediante `PATCH`.

Sus campos son opcionales.

### `UserResponse`

Define la estructura de los datos devueltos por la API.

Incluye:

- `id`
- `name`
- `email`
- `role`
- `is_active`
- `created_at`

También utiliza:

```python
ConfigDict(from_attributes=True)
```

para permitir la conversión de objetos SQLAlchemy a respuestas Pydantic.

---

# Servicios

## `app/services/user_service.py`

Contiene la lógica de acceso y modificación de los usuarios mediante SQLAlchemy.

Entre sus funciones se encuentran:

```text
get_all_users()

get_user_by_id()

get_user_by_email()

email_exists()

create_user()

update_user()

update_user_partial()

delete_user()
```

El servicio utiliza una sesión SQLAlchemy:

```python
db: Session
```

para realizar consultas y operaciones sobre la base de datos.

La separación de esta lógica permite mantener las rutas más organizadas.

---

# Dependency Injection

FastAPI permite utilizar **Dependency Injection** mediante `Depends()`.

## `app/dependencies/database_dependency.py`

Contiene la dependencia encargada de proporcionar una sesión de SQLAlchemy:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

De esta manera, los endpoints pueden recibir automáticamente una sesión de base de datos.

Ejemplo:

```python
def get_users(
    db: Session = Depends(get_db)
):
    ...
```

La sesión se cierra automáticamente después de completar la solicitud.

---

## `app/dependencies/user_dependencies.py`

Contiene la dependencia:

```text
get_user_or_404()
```

Esta función busca un usuario por su ID.

Si el usuario existe, lo devuelve.

Si no existe, genera:

```text
404 Not Found
```

con el mensaje:

```json
{
    "detail": "Usuario no encontrado"
}
```

Esto permite reutilizar la misma lógica en diferentes endpoints.

---

# Endpoints disponibles

| Método | Endpoint | Descripción | Código exitoso |
|---|---|---|---:|
| GET | `/` | Verificar funcionamiento de la API | 200 |
| GET | `/users` | Obtener todos los usuarios | 200 |
| GET | `/users/{user_id}` | Obtener usuario por ID | 200 |
| POST | `/users` | Crear usuario | 201 |
| PUT | `/users/{user_id}` | Actualizar usuario completo | 200 |
| PATCH | `/users/{user_id}` | Actualizar parcialmente un usuario | 200 |
| DELETE | `/users/{user_id}` | Eliminar usuario | 204 |

---

# GET - Obtener usuarios

## Obtener todos los usuarios

Endpoint:

```text
GET /users
```

Devuelve los usuarios almacenados en SQLite.

Los resultados se ordenan por nombre.

Ejemplo:

```json
[
    {
        "name": "Kelly",
        "email": "kelly@example.com",
        "role": "admin",
        "is_active": true,
        "id": 1,
        "created_at": "2026-09-19T03:00:00"
    }
]
```

La fecha y hora de `created_at` dependen del momento en que se creó el registro.

---

# Filtros de usuarios

El endpoint permite filtrar los usuarios mediante parámetros de consulta.

## Filtrar por rol

```text
GET /users?role=admin
```

También:

```text
GET /users?role=support
```

o:

```text
GET /users?role=user
```

---

## Filtrar por estado

Para usuarios activos:

```text
GET /users?is_active=true
```

Para usuarios inactivos:

```text
GET /users?is_active=false
```

---

## Combinar filtros

Es posible utilizar ambos parámetros:

```text
GET /users?role=admin&is_active=true
```

---

# Ordenamiento

Los usuarios obtenidos mediante `GET /users` se ordenan por nombre de forma ascendente.

La consulta utilizada en el servicio es equivalente a:

```python
query.order_by(User.name.asc()).all()
```

Esto permite presentar los registros de manera organizada.

---

# GET - Obtener usuario por ID

Endpoint:

```text
GET /users/{user_id}
```

Ejemplo:

```text
GET /users/1
```

Si el usuario existe, la API devuelve su información.

Si no existe:

```json
{
    "detail": "Usuario no encontrado"
}
```

Código:

```text
404 Not Found
```

---

# POST - Crear usuario

Endpoint:

```text
POST /users
```

Ejemplo de solicitud:

```json
{
    "name": "Maria",
    "email": "maria@example.com",
    "role": "user",
    "is_active": true
}
```

Respuesta:

```json
{
    "name": "Maria",
    "email": "maria@example.com",
    "role": "user",
    "is_active": true,
    "id": 3,
    "created_at": "2026-09-19T03:00:00"
}
```

Código exitoso:

```text
201 Created
```

El `id` y `created_at` son generados al guardar el registro.

---

# PUT - Actualizar usuario completo

Endpoint:

```text
PUT /users/{user_id}
```

El método `PUT` reemplaza completamente la información del usuario.

Todos los campos son obligatorios.

Ejemplo:

```json
{
    "name": "Kelly Lopera",
    "email": "kelly.nuevo@example.com",
    "role": "admin",
    "is_active": true
}
```

Código exitoso:

```text
200 OK
```

Si el usuario no existe:

```text
404 Not Found
```

Si el correo ya pertenece a otro usuario:

```text
400 Bad Request
```

Respuesta:

```json
{
    "detail": "El correo ya está registrado"
}
```

---

# PATCH - Actualizar usuario parcialmente

Endpoint:

```text
PATCH /users/{user_id}
```

A diferencia de `PUT`, `PATCH` permite modificar solamente los campos necesarios.

Ejemplo:

```json
{
    "is_active": false
}
```

También se puede modificar el rol:

```json
{
    "role": "support"
}
```

Código exitoso:

```text
200 OK
```

Si no se envía ningún campo:

```json
{
    "detail": "Debe enviar al menos un campo para actualizar"
}
```

Código:

```text
400 Bad Request
```

---

# DELETE - Eliminar usuario

Endpoint:

```text
DELETE /users/{user_id}
```

Ejemplo:

```text
DELETE /users/2
```

Si el usuario existe, se elimina de la base de datos.

Código:

```text
204 No Content
```

El código `204` no devuelve un cuerpo de respuesta, por lo que Swagger puede mostrar únicamente el código de estado.

Para comprobar la eliminación se puede realizar posteriormente:

```text
GET /users/2
```

La API debe responder:

```text
404 Not Found
```

---

# Persistencia de datos

Una de las principales diferencias de esta versión respecto a la actividad anterior es el uso de una base de datos real.

La aplicación utiliza:

```text
SQLite
```

y almacena la información en:

```text
device_systems.db
```

La conexión se configura mediante:

```python
DATABASE_URL = "sqlite:///./device_systems.db"
```

Anteriormente los usuarios se almacenaban en una estructura en memoria.

En esta versión, los registros permanecen almacenados después de reiniciar el servidor.

Durante las pruebas se comprobó que:

1. Se creó un usuario mediante `POST`.
2. El usuario apareció mediante `GET`.
3. Se detuvo el servidor.
4. Se inició nuevamente la aplicación.
5. El usuario continuó disponible.
6. Después de eliminar un usuario, su consulta mediante `GET` devolvió `404`.

Esto permitió comprobar la persistencia de los datos en SQLite.

---

# Manejo de errores

La API utiliza `HTTPException` de FastAPI y manejo de `IntegrityError` de SQLAlchemy para controlar diferentes situaciones.

## Usuario inexistente

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

## Correo duplicado

```text
400 Bad Request
```

Respuesta:

```json
{
    "detail": "El correo ya está registrado"
}
```

Este control se aplica en:

- `POST`
- `PUT`
- `PATCH`

Además, la base de datos utiliza la restricción:

```python
unique=True
```

sobre el campo `email`.

---

## PATCH sin información

```text
400 Bad Request
```

Respuesta:

```json
{
    "detail": "Debe enviar al menos un campo para actualizar"
}
```

---

## Datos inválidos

FastAPI y Pydantic validan automáticamente los datos recibidos.

Cuando los datos no cumplen las reglas definidas, FastAPI responde:

```text
422 Unprocessable Entity
```

Ejemplos:

- Correo electrónico inválido.
- Nombre con menos de 3 caracteres.
- Rol diferente a `admin`, `support` o `user`.
- Tipo de dato incorrecto.

---

# Validación con Pydantic

La API utiliza Pydantic para validar los datos recibidos.

Ejemplo:

```python
class UserBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        description="Nombre del usuario"
    )
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool = True
```

## Nombre

Debe tener como mínimo 3 caracteres.

## Correo

Debe tener un formato válido de correo electrónico.

## Rol

Solamente se permiten:

```text
admin
support
user
```

## Estado

El campo `is_active` utiliza un valor booleano:

```text
true
false
```

---

# Restricciones de SQLAlchemy

El modelo SQLAlchemy utiliza restricciones para mantener la integridad de los datos.

## Clave primaria

El campo `id` se define como:

```python
primary_key=True
```

## Correo único

El campo `email` utiliza:

```python
unique=True
```

Esto evita que existan dos usuarios con el mismo correo.

## Campos obligatorios

Los campos principales utilizan:

```python
nullable=False
```

para evitar valores nulos en:

- `name`
- `email`
- `role`

El campo `is_active` utiliza `True` como valor predeterminado.

---

# Swagger y OpenAPI

FastAPI genera automáticamente documentación interactiva.

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

Desde Swagger es posible:

- Consultar endpoints.
- Enviar solicitudes.
- Probar parámetros.
- Probar cuerpos JSON.
- Ver respuestas.
- Revisar códigos HTTP.
- Consultar los modelos Pydantic.
- Realizar pruebas del CRUD.

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

ReDoc presenta la documentación de la API en un formato alternativo.

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

Utilizando `uv`:

```bash
uv sync
```

También es posible utilizar:

```bash
uv pip install -r requirements.txt
```

---

# Ejecución del proyecto

Para iniciar el servidor:

```bash
uv run uvicorn app.main:app --reload
```

También puede utilizarse:

```bash
uvicorn app.main:app --reload
```

si el entorno virtual se encuentra activado.

El parámetro:

```text
--reload
```

permite que el servidor se reinicie automáticamente cuando se realizan cambios en el código.

La API estará disponible en:

```text
http://127.0.0.1:8000
```

---

# Documentación de la API

Una vez iniciado el servidor se puede acceder a:

### Swagger

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# Pruebas realizadas

Las pruebas fueron realizadas utilizando Swagger UI.

Se verificaron los siguientes escenarios:

## Consultas

- Obtener todos los usuarios.
- Obtener usuario por ID.
- Buscar usuario inexistente.
- Filtrar por rol.
- Filtrar por estado.
- Verificar ordenamiento por nombre.

## Creación

- Crear usuario correctamente.
- Crear usuario con correo inválido.
- Crear usuario con nombre demasiado corto.
- Crear usuario con rol inválido.
- Crear usuario con correo duplicado.

## Actualización completa

- Actualizar usuario existente mediante `PUT`.
- Intentar actualizar con correo duplicado.
- Intentar actualizar un usuario inexistente.

## Actualización parcial

- Modificar un campo mediante `PATCH`.
- Modificar varios campos.
- Intentar realizar `PATCH` sin campos.

## Eliminación

- Eliminar usuario existente.
- Comprobar que el usuario eliminado ya no existe.
- Intentar consultar un usuario eliminado.
- Intentar eliminar un usuario inexistente.

## Persistencia

- Crear usuarios.
- Reiniciar el servidor.
- Consultar nuevamente los usuarios.
- Comprobar que los registros permanecen almacenados en SQLite.

## Documentación

- Verificar Swagger UI.
- Verificar OpenAPI.
- Verificar ReDoc.
- Verificar endpoints documentados.
- Verificar modelos y códigos de respuesta.

---

# Evidencias

Las evidencias de las pruebas realizadas se encuentran en la carpeta:

```text
evidencias/
```

Los archivos utilizados son:

```text
01_get_users.jpeg
02_get_user_id.jpeg
03_query_role.jpeg
04_query_is_active.jpeg
05_post_usuario.jpeg
06_email_invalido.jpeg
07_nombre_corto.jpeg
08_role_invalido.jpeg
09_correo_duplicado.jpeg
10_put_usuario.jpeg
11_put_correo_duplicado.jpeg
12_put_usuario_inexistente.jpeg
13_patch_usuario.jpeg
14_patch_vacio.jpeg
15_delete_usuario.jpeg
16_delete_usuario_inexistente.jpeg
17_persistencia_sqlite.jpeg
18_swagger_openapi.jpeg
```

---

# Conceptos aplicados

Durante el desarrollo de esta actividad se aplicaron los siguientes conceptos:

- APIs REST.
- FastAPI.
- Pydantic.
- SQLAlchemy.
- ORM.
- SQLite.
- Persistencia de datos.
- Modelos relacionales.
- Validación de información.
- CRUD.
- Métodos HTTP.
- Parámetros de ruta.
- Parámetros de consulta.
- Filtros.
- Ordenamiento.
- Códigos de estado HTTP.
- Manejo de excepciones.
- `HTTPException`.
- `IntegrityError`.
- Dependency Injection.
- `Depends()`.
- Sesiones de base de datos.
- Swagger UI.
- OpenAPI.
- ReDoc.
- Separación de responsabilidades.
- Servicios.
- Modelos SQLAlchemy.
- Esquemas Pydantic.
- Git y GitHub.
- Gestión de dependencias con `uv`.

---

# Separación de responsabilidades

El proyecto utiliza una estructura organizada por responsabilidades:

```text
routes
   ↓
services
   ↓
models
   ↓
database
```

Mientras que:

```text
schemas
```

se encarga de validar la información recibida y enviada por la API.

Y:

```text
dependencies
```

contiene lógica reutilizable que puede ser inyectada mediante `Depends()`.

Esta organización facilita:

- El mantenimiento.
- La reutilización del código.
- Las pruebas.
- La lectura del proyecto.
- La separación de responsabilidades.
- La futura escalabilidad de la aplicación.

---

# Flujo de una solicitud

El funcionamiento general de una operación sobre usuarios puede representarse de la siguiente manera:

```text
Cliente
   ↓
FastAPI / Route
   ↓
Dependency Injection
   ↓
Service
   ↓
SQLAlchemy
   ↓
SQLite
   ↓
Respuesta
```

Por ejemplo, al crear un usuario:

```text
POST /users
      ↓
UserCreate
      ↓
Validación Pydantic
      ↓
user_service
      ↓
SQLAlchemy
      ↓
SQLite
      ↓
UserResponse
```

---

# Ventajas de FastAPI

FastAPI permite desarrollar APIs modernas de manera rápida y organizada.

Entre sus principales ventajas se encuentran:

- Alto rendimiento.
- Validación automática mediante Pydantic.
- Documentación automática.
- Integración con Swagger y ReDoc.
- Soporte para Dependency Injection.
- Uso de tipado de Python.
- Manejo sencillo de rutas y parámetros.
- Facilidad para construir APIs REST.
- Integración con SQLAlchemy.
- Manejo organizado de errores.

---

# Reflexión

El desarrollo de esta actividad permitió avanzar desde una implementación que almacenaba los usuarios temporalmente en memoria hacia una solución que utiliza persistencia de datos mediante SQLite y SQLAlchemy.

La incorporación de SQLAlchemy permitió comprender cómo una API puede trabajar con un modelo de datos y realizar operaciones CRUD directamente sobre una base de datos.

También fue importante separar los modelos de SQLAlchemy de los esquemas de Pydantic, ya que cada uno cumple una función diferente dentro de la aplicación.

La utilización de Dependency Injection permitió administrar las sesiones de base de datos y reutilizar lógica dentro de los endpoints.

Las pruebas realizadas mediante Swagger facilitaron la comprobación de los diferentes escenarios de éxito y error.

---

# Conclusión

La actividad permitió evolucionar la API `device_systems` hacia una arquitectura con persistencia de datos utilizando **FastAPI, SQLAlchemy y SQLite**.

Se implementó un CRUD completo de usuarios mediante:

```text
GET
POST
PUT
PATCH
DELETE
```

Además, se incorporaron:

- Modelos SQLAlchemy.
- Sesiones de base de datos.
- Persistencia mediante SQLite.
- Validaciones mediante Pydantic.
- Restricciones de integridad.
- Validación de correos.
- Validación de roles.
- Prevención de correos duplicados.
- Manejo de errores HTTP.
- Dependency Injection.
- Filtros por rol y estado.
- Ordenamiento por nombre.
- Documentación automática mediante Swagger/OpenAPI.
- Pruebas de persistencia después de reiniciar la aplicación.

La separación entre rutas, servicios, modelos, esquemas, dependencias y conexión de base de datos permite que el proyecto tenga una estructura clara y facilita futuras mejoras.

---

# Autora

**Kelly Lopera**

Tecnólogo en Análisis y Desarrollo de Software

SENA

Proyecto académico desarrollado como parte de la formación en ADSO.