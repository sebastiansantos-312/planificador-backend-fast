"""
routes/subjects.py - Endpoints para materias predefinidas.

Permite consultar las materias estáticas predefinidas.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("/", response_model=list[schemas.Subject])
def get_subjects(db: Session = Depends(get_db)):
    """Lista todas las materias predefinidas."""
    return crud.get_subjects(db)


@router.get("/by-email", response_model=list[schemas.Subject])
def get_subjects_by_email(user_email: str, db: Session = Depends(get_db)):
    """Lista todas las materias predefinidas."""
    return crud.get_subjects_by_email(db, user_email)


@router.get("/{subject_id}", response_model=schemas.Subject)
def get_subject(subject_id: UUID, db: Session = Depends(get_db)):
    """Obtiene una materia por su UUID."""
    return crud.get_subject(db, subject_id)