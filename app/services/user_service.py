from sqlalchemy.orm import Session

from app.models.user_model import User


def get_all_users(
    db: Session,
    role: str | None = None,
    is_active: bool | None = None
):
    """Obtiene los usuarios aplicando filtros y orden por nombre."""

    query = db.query(User)

    if role is not None:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.order_by(User.name.asc()).all()


def get_user_by_id(db: Session, user_id: int):
    """Busca un usuario por su ID."""

    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Busca un usuario por su correo."""

    return db.query(User).filter(User.email == email).first()

def email_exists(
    db: Session,
    email: str,
    exclude_user_id: int | None = None,
):
    """Comprueba si un correo ya está registrado."""

    query = db.query(User).filter(User.email == email)

    if exclude_user_id is not None:
        query = query.filter(User.id != exclude_user_id)

    return query.first() is not None

def create_user(db: Session, user_data):
    """Crea un nuevo usuario en la base de datos."""

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        is_active=user_data.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def update_user(
    db: Session,
    user: User,
    user_data,
):
    """Actualiza completamente un usuario."""

    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return user


def update_user_partial(
    db: Session,
    user: User,
    update_data,
):
    """Actualiza parcialmente un usuario."""

    data = update_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User,
):
    """Elimina un usuario de la base de datos."""

    db.delete(user)
    db.commit()

    return user