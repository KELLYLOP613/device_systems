# API REST de Gestión de Usuarios - device_systems

## GA1-220501096-01-AA1-EV08
### FastAPI Intermedio: CRUD Completo, Manejo de Errores, Swagger/OpenAPI y Dependency Injection

---

## 👩‍💻 Información del proyecto

**Programa:** Tecnólogo en Análisis y Desarrollo de Software (ADSO)  
**Entidad:** Servicio Nacional de Aprendizaje - SENA  
**Proyecto:** `device_systems`  
**Actividad:** GA1-220501096-01-AA1-EV08  
**Tecnología principal:** FastAPI  
**Lenguaje:** Python 3.13  
**Autor:** Kelly Lopera  

---

## 📌 Descripción

`device_systems` es una API REST desarrollada con **FastAPI** para la gestión de usuarios de un sistema.

Esta versión corresponde a la evolución del proyecto desarrollado en la actividad anterior y permite implementar un **CRUD completo de usuarios**, incluyendo:

- Consulta de usuarios.
- Consulta de un usuario por ID.
- Creación de usuarios.
- Actualización completa mediante `PUT`.
- Actualización parcial mediante `PATCH`.
- Eliminación de usuarios mediante `DELETE`.
- Validación de datos utilizando Pydantic.
- Manejo de errores HTTP.
- Validación de correos electrónicos.
- Validación de roles.
- Prevención de correos duplicados.
- Dependency Injection mediante `Depends()`.
- Documentación automática con Swagger/OpenAPI.
- Filtros por rol y estado de actividad.

La información se almacena temporalmente en una estructura de datos en memoria, simulando una base de datos.

---

# 🎯 Objetivos

## Objetivo general

Desarrollar una API REST utilizando FastAPI que permita gestionar usuarios mediante operaciones CRUD, aplicando validaciones, manejo de errores, códigos de estado HTTP, Dependency Injection y documentación automática con Swagger/OpenAPI.

## Objetivos específicos

- Implementar endpoints para gestionar usuarios.
- Aplicar validaciones mediante Pydantic.
- Implementar operaciones `GET`, `POST`, `PUT`, `PATCH` y `DELETE`.
- Utilizar códigos de estado HTTP adecuados.
- Implementar manejo de errores mediante `HTTPException`.
- Evitar registros con correos electrónicos duplicados.
- Implementar Dependency Injection mediante `Depends()`.
- Separar las responsabilidades de rutas, servicios, datos, esquemas y dependencias.
- Documentar la API utilizando Swagger/OpenAPI.
- Realizar pruebas de los diferentes endpoints y casos de error.

---

# 🛠️ Tecnologías utilizadas

- **Python 3.13**
- **FastAPI**
- **Uvicorn**
- **Pydantic**
- **Email-validator**
- **Swagger/OpenAPI**
- **ReDoc**
- **Git**
- **GitHub**
- **uv** para la gestión del entorno y dependencias

---

# 📂 Estructura del proyecto

```text
device_systems/
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_routes.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── user_dependencies.py
│   │
│   └── data/
│       ├── __init__.py
│       └── users_db.py
│
├── evidencias/
│
├── src/
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

---

# 📁 Descripción de los módulos

## `app/main.py`

Es el archivo principal de la aplicación.

Aquí se configura la instancia de FastAPI, la información de la API, los datos de contacto, las rutas y los encabezados personalizados.

También se encuentra el endpoint raíz:

```text
GET /
```

---

## `app/routes/user_routes.py`

Contiene los endpoints relacionados con la gestión de usuarios.

Aquí se definen las operaciones:

- GET
- POST
- PUT
- PATCH
- DELETE

Las rutas utilizan los servicios y las dependencias para mantener separada la lógica de negocio.

---

## `app/schemas/user_schema.py`

Contiene los modelos de Pydantic utilizados para validar los datos.

### `UserBase`

Modelo base de usuario.

Campos:

- `name`
- `email`
- `role`
- `is_active`

### `UserCreate`

Se utiliza para crear nuevos usuarios.

### `UserUpdate`

Se utiliza para actualizar completamente un usuario mediante `PUT`.

Todos sus campos son obligatorios.

### `UserPatch`

Se utiliza para realizar actualizaciones parciales mediante `PATCH`.

Sus campos son opcionales.

### `UserResponse`

Define la estructura de los datos que devuelve la API e incluye el campo `id`.

---

## `app/services/user_service.py`

Contiene la lógica de negocio relacionada con los usuarios.

Entre sus funciones se encuentran:

```text
get_all_users()
get_user_by_id()
email_exists()
create_user()
update_user()
update_user_partial()
delete_user()
```

Esta separación permite evitar que toda la lógica quede directamente dentro de las rutas.

---

## `app/dependencies/user_dependencies.py`

Contiene dependencias reutilizables de FastAPI.

Actualmente se utiliza:

```python
get_user_or_404()
```

Esta función busca un usuario por su ID.

Si el usuario existe, lo devuelve.

Si no existe, genera automáticamente un error:

```text
404 Usuario no encontrado
```

---

## `app/data/users_db.py`

Contiene la información de usuarios utilizada como una base de datos temporal en memoria.

Ejemplo:

```python
users_db = [
    {
        "id": 1,
        "name": "Kelly",
        "email": "kelly@example.com",
        "role": "admin",
        "is_active": True
    }
]
```

Los datos son temporales y se reinician cuando se reinicia la aplicación.

---

# ⚙️ Instalación

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

Con `uv`:

```bash
uv sync
```

También es posible instalar las dependencias utilizando:

```bash
uv pip install -r requirements.txt
```

---

# ▶️ Ejecución del proyecto

Para iniciar el servidor:

```bash
uvicorn app.main:app --reload
```

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

# 📚 Documentación de la API

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
- Consultar los modelos de Pydantic.

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

ReDoc presenta la documentación de la API en un formato alternativo.

---

# 🔗 Endpoints disponibles

| Método | Endpoint | Descripción | Código exitoso |
|---|---|---|---:|
| GET | `/` | Verificar funcionamiento de la API | 200 |
| GET | `/users/` | Obtener todos los usuarios | 200 |
| GET | `/users/{user_id}` | Obtener usuario por ID | 200 |
| POST | `/users/` | Crear usuario | 201 |
| PUT | `/users/{user_id}` | Actualizar usuario completo | 200 |
| PATCH | `/users/{user_id}` | Actualizar parcialmente un usuario | 200 |
| DELETE | `/users/{user_id}` | Eliminar usuario | 204 |

---

# 🔎 GET - Obtener usuarios

## Obtener todos los usuarios

Endpoint:

```text
GET /users/
```

Devuelve la lista de usuarios registrados.

Ejemplo de respuesta:

```json
[
    {
        "name": "Kelly",
        "email": "kelly@example.com",
        "role": "admin",
        "is_active": true,
        "id": 1
    },
    {
        "name": "Carlos",
        "email": "carlos@example.com",
        "role": "support",
        "is_active": true,
        "id": 2
    }
]
```

---

# 🔎 Filtros de usuarios

El endpoint permite filtrar los usuarios mediante parámetros de consulta.

## Filtrar por rol

```text
GET /users/?role=admin
```

Ejemplo:

```text
GET /users/?role=support
```

---

## Filtrar por estado

```text
GET /users/?is_active=true
```

También se puede utilizar:

```text
GET /users/?is_active=false
```

---

## Combinar filtros

Es posible utilizar ambos parámetros:

```text
GET /users/?role=admin&is_active=true
```

---

# 🔎 GET - Obtener usuario por ID

Endpoint:

```text
GET /users/{user_id}
```

Ejemplo:

```text
GET /users/1
```

Respuesta:

```json
{
    "name": "Kelly",
    "email": "kelly@example.com",
    "role": "admin",
    "is_active": true,
    "id": 1
}
```

Si el usuario no existe:

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

# ➕ POST - Crear usuario

Endpoint:

```text
POST /users/
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
    "id": 4
}
```

Código exitoso:

```text
201 Created
```

---

# ✏️ PUT - Actualizar usuario completo

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

Ejemplo de respuesta:

```json
{
    "detail": "El correo ya está registrado"
}
```

---

# 📝 PATCH - Actualizar usuario parcialmente

Endpoint:

```text
PATCH /users/{user_id}
```

A diferencia de `PUT`, `PATCH` permite modificar solamente los campos necesarios.

Por ejemplo, para cambiar únicamente el rol:

```json
{
    "role": "support"
}
```

También se puede modificar solamente el estado:

```json
{
    "is_active": false
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

# 🗑️ DELETE - Eliminar usuario

Endpoint:

```text
DELETE /users/{user_id}
```

Ejemplo:

```text
DELETE /users/2
```

Si el usuario existe, es eliminado correctamente.

Código:

```text
204 No Content
```

Si el usuario no existe:

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

# ⚠️ Manejo de errores

La API utiliza `HTTPException` de FastAPI para generar respuestas de error controladas.

## Usuario inexistente

```text
404 Not Found
```

Mensaje:

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

Mensaje:

```json
{
    "detail": "El correo ya está registrado"
}
```

Este error se controla en:

- POST
- PUT
- PATCH

---

## PATCH sin información

```text
400 Bad Request
```

Mensaje:

```json
{
    "detail": "Debe enviar al menos un campo para actualizar"
}
```

---

## Datos inválidos

FastAPI y Pydantic validan automáticamente los datos enviados.

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

# 📊 Códigos de estado HTTP

| Código | Significado | Uso |
|---:|---|---|
| 200 | OK | Solicitud procesada correctamente |
| 201 | Created | Usuario creado correctamente |
| 204 | No Content | Usuario eliminado correctamente |
| 400 | Bad Request | Datos no permitidos o correo duplicado |
| 404 | Not Found | Usuario inexistente |
| 422 | Unprocessable Entity | Error de validación de Pydantic |

---

# 🔐 Validación con Pydantic

La API utiliza Pydantic para validar los datos recibidos.

Por ejemplo:

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

Estas validaciones permiten controlar:

### Nombre

Debe tener como mínimo 3 caracteres.

### Correo

Debe tener un formato válido de correo electrónico.

### Rol

Solamente se permiten:

```text
admin
support
user
```

### Estado

El campo `is_active` utiliza un valor booleano:

```text
true
false
```

---

# 💉 Dependency Injection

FastAPI permite utilizar **Dependency Injection** mediante `Depends()`.

En este proyecto se creó la dependencia:

```python
get_user_or_404()
```

Su objetivo es buscar un usuario por ID antes de ejecutar determinadas operaciones.

Ejemplo:

```python
def get_user(
    user=Depends(get_user_or_404)
):
    return user
```

De esta manera, la ruta recibe directamente el usuario encontrado.

Si el usuario no existe, la dependencia genera automáticamente:

```text
404 Usuario no encontrado
```

Esto permite reutilizar la misma lógica en diferentes endpoints y evita repetir código.

---

# 🧩 Separación de responsabilidades

El proyecto utiliza una estructura organizada por responsabilidades.

```text
routes
   ↓
services
   ↓
data
```

Mientras que:

```text
schemas
```

se encarga de validar los datos.

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
- La escalabilidad de la aplicación.

---

# 📖 Swagger y OpenAPI

La aplicación configura información personalizada para la documentación:

```python
app = FastAPI(
    title="Device Systems API",
    description="API REST para la gestión de usuarios del sistema device_systems.",
    version="2.0.0",
    contact={
        "name": "Kelly Lopera",
        "email": "johalopera15@gmail.com"
    }
)
```

Cada endpoint también cuenta con información como:

- `summary`
- `description`
- `response_description`

Esto permite que Swagger presente una documentación más clara y organizada.

---

# 🧪 Pruebas realizadas

Las pruebas fueron realizadas utilizando Swagger UI.

Se verificaron diferentes escenarios:

## Consultas

- Obtener todos los usuarios.
- Obtener usuario por ID.
- Buscar usuario inexistente.
- Filtrar por rol.
- Filtrar por estado.

## Creación

- Crear usuario correctamente.
- Crear usuario con correo inválido.
- Crear usuario con nombre demasiado corto.
- Crear usuario con rol inválido.
- Crear usuario con correo duplicado.

## Actualización completa

- Actualizar usuario existente mediante PUT.
- Intentar actualizar con correo duplicado.
- Intentar actualizar un usuario inexistente.

## Actualización parcial

- Modificar un solo campo.
- Modificar varios campos.
- Intentar realizar PATCH sin campos.

## Eliminación

- Eliminar usuario existente.
- Intentar eliminar usuario inexistente.

## Documentación

- Verificar Swagger UI.
- Verificar información de OpenAPI.
- Verificar endpoints documentados.
- Verificar modelos y códigos de respuesta.

---

# 📸 Evidencias

Las evidencias de las pruebas realizadas se encuentran en la carpeta:

```text
evidencias/
```

Entre las evidencias se incluyen:

```text
01_get_users.jpeg
02_get_user_id.jpeg
03_query_role.jpeg
04_query_is_active.jpeg
05_post_user.jpeg
06_email_invalido.jpeg
07_nombre_corto.jpeg
08_role_invalido.jpeg
09_correo_duplicado.jpeg
10_cabeceras.jpeg
11_put_usuario.jpeg
12_put_correo_duplicado.jpeg
13_put_usuario_inexistente.jpeg
14_patch_usuario.jpeg
15_patch_vacio.jpeg
16_delete_usuario.jpeg
17_delete_usuario_inexistente.jpeg
18_swagger_openapi.jpeg
```

> Los nombres anteriores corresponden a la organización propuesta para las evidencias de la actividad.

---

# 🧠 Conceptos aplicados

Durante el desarrollo de esta actividad se aplicaron los siguientes conceptos:

- APIs REST.
- FastAPI.
- Pydantic.
- Modelos de datos.
- Validación de información.
- CRUD.
- Métodos HTTP.
- Parámetros de ruta.
- Parámetros de consulta.
- Códigos de estado HTTP.
- Manejo de excepciones.
- `HTTPException`.
- Dependency Injection.
- `Depends()`.
- Swagger UI.
- OpenAPI.
- ReDoc.
- Separación de responsabilidades.
- Servicios.
- Dependencias reutilizables.
- Simulación de persistencia en memoria.
- Git y GitHub.

---

# 🚀 Ventajas de FastAPI

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

---

# 💭 Reflexión

El desarrollo de esta actividad permitió profundizar en el funcionamiento de FastAPI y comprender cómo una API puede organizarse de manera más estructurada.

La implementación del CRUD permitió trabajar con las operaciones principales de una API REST, mientras que el manejo de errores permitió controlar diferentes situaciones que pueden ocurrir durante el uso de la aplicación.

También fue importante comprender el funcionamiento de `Depends()`, ya que permite reutilizar lógica y separar responsabilidades dentro del proyecto.

La utilización de Swagger facilitó las pruebas de los endpoints y permitió visualizar de manera clara la estructura de la API.

---

# 📌 Conclusión

La actividad permitió evolucionar la API `device_systems` desde una implementación básica hacia una aplicación con una estructura más organizada y funcionalidades más completas.

Se implementó un CRUD completo de usuarios utilizando:

```text
GET
POST
PUT
PATCH
DELETE
```

Además, se incorporaron validaciones mediante Pydantic, manejo de errores HTTP, prevención de correos duplicados, Dependency Injection mediante `Depends()` y documentación automática mediante Swagger/OpenAPI.

La separación entre rutas, esquemas, servicios, dependencias y datos permite que el proyecto tenga una estructura más clara y facilita futuras mejoras, como la integración de una base de datos real y un sistema de autenticación.

---

# 👩‍💻 Autora

**Kelly Lopera**

Tecnólogo en Análisis y Desarrollo de Software  
SENA

Proyecto académico desarrollado como parte de la formación en ADSO.