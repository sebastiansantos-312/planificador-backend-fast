"""
routes/subjects.py — Endpoints para materias predefinidas.

Permite consultar las materias estáticas predefinidas.
No se permiten crear, actualizar o eliminar, ya que son fijas.

Endpoints:
  GET    /subjects/            — Lista todas las materias predefinidas.
  GET    /subjects/by-email    — Lista todas las materias predefinidas (por compatibilidad).
  GET    /subjects/{id}       — Obtiene una materia por UUID.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("/", response_model=list[schemas.Subject])
def get_subjects(db: Session = Depends(get_db)):
    """
    Lista todas las materias predefinidas.

    Args:
        db (Session): Sesión de BD inyectada.

    Returns:
        list[Subject]: Todas las materias estáticas.
    """
    return crud.get_subjects(db)


@router.get("/by-email", response_model=list[schemas.Subject])
def get_subjects_by_email(user_email: str, db: Session = Depends(get_db)):
    """
    Lista todas las materias predefinidas (por compatibilidad con frontend).

    Args:
        user_email (str): Query param con el email del usuario (ignorado).
        db (Session): Sesión de BD inyectada.

    Returns:
        list[Subject]: Todas las materias estáticas.
    """
    return crud.get_subjects_by_email(db, user_email)


@router.get("/{subject_id}", response_model=schemas.Subject)
def get_subject(subject_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene una materia por su UUID.

    Args:
        subject_id (UUID): UUID de la materia en la ruta.
        db (Session): Sesión de BD inyectada.

    Returns:
        Subject: Materia encontrada.
    """
    return crud.get_subject(db, subject_id)