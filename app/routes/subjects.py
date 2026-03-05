from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/", response_model=schemas.Subject)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, subject)


# ✅ Crear materia con email
@router.post("/by-email", response_model=schemas.Subject)
def create_subject_by_email(subject: schemas.SubjectCreateByEmail, db: Session = Depends(get_db)):
    return crud.create_subject_by_email(db, subject)


@router.get("/", response_model=list[schemas.Subject])
def get_subjects(user_id: UUID, db: Session = Depends(get_db)):
    return crud.get_subjects(db, user_id)


# ✅ Obtener materias con email
@router.get("/by-email", response_model=list[schemas.Subject])
def get_subjects_by_email(user_email: str, db: Session = Depends(get_db)):
    return crud.get_subjects_by_email(db, user_email)


@router.get("/{subject_id}", response_model=schemas.Subject)
def get_subject(subject_id: UUID, db: Session = Depends(get_db)):
    return crud.get_subject(db, subject_id)


@router.patch("/{subject_id}", response_model=schemas.Subject)
def update_subject(subject_id: UUID, subject: schemas.SubjectUpdate, db: Session = Depends(get_db)):
    return crud.update_subject(db, subject_id, subject)


@router.delete("/{subject_id}")
def delete_subject(subject_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_subject(db, subject_id)