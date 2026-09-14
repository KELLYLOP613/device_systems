from app.data.users_db import users_db


def get_all_users():
    """Obtiene todos los usuarios."""
    return users_db


def get_user_by_id(user_id: int):
    """Busca un usuario por su ID."""
    for user in users_db:
        if user["id"] == user_id:
            return user

    return None


def email_exists(email: str, exclude_user_id: int | None = None):
    """Comprueba si un correo ya está registrado."""
    for user in users_db:
        if user["email"] == email:
            if exclude_user_id is None or user["id"] != exclude_user_id:
                return True

    return False


def create_user(user_data):
    """Crea un nuevo usuario."""

    new_id = max((user["id"] for user in users_db), default=0) + 1

    new_user = {
        "id": new_id,
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "is_active": user_data.is_active
    }

    users_db.append(new_user)

    return new_user

def update_user(user_id: int, user_data):
    """Actualiza completamente un usuario."""
    user = get_user_by_id(user_id)

    if user is None:
        return None

    user["name"] = user_data.name
    user["email"] = user_data.email
    user["role"] = user_data.role
    user["is_active"] = user_data.is_active

    return user


def update_user_partial(user_id: int, update_data):
    """Actualiza parcialmente un usuario."""
    user = get_user_by_id(user_id)

    if user is None:
        return None

    data = update_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        user[field] = value

    return user


def delete_user(user_id: int):
    """Elimina un usuario."""
    user = get_user_by_id(user_id)

    if user is None:
        return None

    users_db.remove(user)

    return user