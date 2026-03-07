"""
routes/users.py — Endpoints CRUD para usuarios.

Gestiona el registro y administración de cuentas de usuario.
El registro (POST /) crea un nuevo usuario en la BD.
Los demás endpoints permiten consultar, actualizar y eliminar usuarios.

Endpoints:
  POST   /users/      — Registra un nuevo usuario.
  GET    /users/      — Lista todos los usuarios.
  GET    /users/{id}  — Obtiene un usuario por UUID.
  PATCH  /users/{id}  — Actualiza el perfil de un usuario.
  DELETE /users/{id}  — Elimina un usuario.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema.

    Llamado desde AuthPage (formulario de registro) en el frontend.
    La contraseña se almacena en texto plano en Sprint 1.

    Args:
        user (UserCreate): Datos del nuevo usuario (nombre, email, contraseña).
        db (Session): Sesión de BD inyectada.

    Returns:
        User: Usuario creado (sin contraseña).

    TODO Sprint 2: Validar email único antes de insertar, hashear contraseña.
    """
    return crud.create_user(db, user)


@router.get("/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    """
    Lista todos los usuarios registrados.

    Args:
        db (Session): Sesión de BD inyectada.

    Returns:
        list[User]: Todos los usuarios (sin contraseñas).
    """
    return crud.get_users(db)


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene un usuario por su UUID.

    Args:
        user_id (UUID): UUID del usuario en la ruta.
        db (Session): Sesión de BD inyectada.

    Returns:
        User: Usuario encontrado.
    """
    return crud.get_user(db, user_id)


@router.patch("/{user_id}", response_model=schemas.User)
def update_user(user_id: UUID, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza parcialmente el perfil de un usuario (PATCH).

    Solo modifica los campos enviados en el request.

    Args:
        user_id (UUID): UUID del usuario a actualizar.
        user (UserUpdate): Campos a modificar.
        db (Session): Sesión de BD inyectada.

    Returns:
        User: Usuario actualizado.
    """
    return crud.update_user(db, user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina un usuario de la base de datos.

    Args:
        user_id (UUID): UUID del usuario a eliminar.
        db (Session): Sesión de BD inyectada.

    Returns:
        dict: Mensaje de confirmación.
    """
    return crud.delete_user(db, user_id)