"""
routes/users.py — Endpoints para usuarios.

Permite consultar usuarios. No se permite crear nuevos usuarios.
Los usuarios deben ser creados manualmente en la base de datos.

Endpoints:
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