from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from datetime import date
from uuid import UUID
from typing import Optional
from fastapi import HTTPException


# ─── USERS ──────────────────────────────────────────────────

def create_user(db: Session, user: schemas.UserCreate):
    # TODO Sprint 2: hashear password con bcrypt
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# ─── SUBJECTS ───────────────────────────────────────────────

def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def get_subjects(db: Session, user_id: UUID):
    return db.query(models.Subject).filter(models.Subject.user_id == user_id).all()


def delete_subject(db: Session, subject_id: UUID):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(db_subject)
    db.commit()
    return {"message": "subject deleted"}


# ─── TASKS ──────────────────────────────────────────────────

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, user_id: UUID):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()


def get_task(db: Session, task_id: UUID):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


def update_task(db: Session, task_id: UUID, task: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    # Solo actualiza los campos que vienen (no None)
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: UUID):
    db_task = get_task(db, task_id)
    db.delete(db_task)
    db.commit()
    return {"message": "task deleted"}


# ─── SUBTASKS ───────────────────────────────────────────────

def create_subtask(db: Session, subtask: schemas.SubtaskCreate):
    db_subtask = models.Subtask(**subtask.dict())
    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask


def get_subtasks_by_task(db: Session, task_id: UUID):
    return db.query(models.Subtask).filter(models.Subtask.task_id == task_id).all()


def get_subtask(db: Session, subtask_id: UUID):
    db_subtask = db.query(models.Subtask).filter(models.Subtask.id == subtask_id).first()
    if not db_subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return db_subtask


def update_subtask(db: Session, subtask_id: UUID, subtask: schemas.SubtaskUpdate):
    db_subtask = get_subtask(db, subtask_id)
    for key, value in subtask.dict(exclude_unset=True).items():
        setattr(db_subtask, key, value)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask


def delete_subtask(db: Session, subtask_id: UUID):
    db_subtask = get_subtask(db, subtask_id)
    db.delete(db_subtask)
    db.commit()
    return {"message": "subtask deleted"}


# ─── VISTA "HOY" — US-04 (T2) ───────────────────────────────
# Regla: Vencidas → Para hoy → Próximas
# Desempate: menor esfuerzo estimado primero

def get_today_view(db: Session, user_id: UUID):
    today = date.today()

    subtasks = (
        db.query(models.Subtask)
        .join(models.Task, models.Subtask.task_id == models.Task.id)
        .filter(models.Task.user_id == user_id)
        .filter(models.Subtask.status != "done")
        .filter(models.Subtask.target_date != None)
        .all()
    )

    overdue = []
    for_today = []
    upcoming = []

    for s in subtasks:
        if s.target_date < today:
            overdue.append(s)
        elif s.target_date == today:
            for_today.append(s)
        else:
            upcoming.append(s)

    overdue.sort(key=lambda s: (s.target_date, s.estimated_minutes or 9999))
    for_today.sort(key=lambda s: (s.estimated_minutes or 9999,))
    upcoming.sort(key=lambda s: (s.target_date, s.estimated_minutes or 9999))

    # Convertir a dict para que Pydantic pueda serializarlo
    def to_dict(s):
        return {
            "id": str(s.id),
            "task_id": str(s.task_id),
            "title": s.title,
            "description": s.description,
            "target_date": s.target_date.isoformat() if s.target_date else None,
            "estimated_minutes": s.estimated_minutes,
            "status": s.status,
            "created_at": s.created_at.isoformat() if s.created_at else None,
        }

    return {
        "date": today.isoformat(),
        "overdue": [to_dict(s) for s in overdue],
        "for_today": [to_dict(s) for s in for_today],
        "upcoming": [to_dict(s) for s in upcoming],
    }


# ─── CONFLICTO DE SOBRECARGA — US-07 (T3) ───────────────────
# Límite por defecto: 6 horas (360 min) si el usuario no configura

DEFAULT_DAILY_LIMIT_MINUTES = 360  # 6 horas


def check_overload_conflict(
    db: Session,
    user_id: UUID,
    target_date: date,
    new_estimated_minutes: int,
    exclude_subtask_id: Optional[UUID] = None,
    daily_limit_minutes: int = DEFAULT_DAILY_LIMIT_MINUTES,
):
    """
    Suma las horas planificadas para target_date del usuario.
    Retorna dict con si hay conflicto y cuánto excede.
    """
    query = (
        db.query(func.sum(models.Subtask.estimated_minutes))
        .join(models.Task, models.Subtask.task_id == models.Task.id)
        .filter(models.Task.user_id == user_id)
        .filter(models.Subtask.target_date == target_date)
        .filter(models.Subtask.status != "done")
    )

    # Si es una actualización, excluir la subtarea que se está moviendo
    if exclude_subtask_id:
        query = query.filter(models.Subtask.id != exclude_subtask_id)

    current_total = query.scalar() or 0
    new_total = current_total + new_estimated_minutes

    has_conflict = new_total > daily_limit_minutes

    return {
        "has_conflict": has_conflict,
        "current_minutes": current_total,
        "new_total_minutes": new_total,
        "limit_minutes": daily_limit_minutes,
        "current_hours": round(current_total / 60, 1),
        "new_total_hours": round(new_total / 60, 1),
        "limit_hours": round(daily_limit_minutes / 60, 1),
        "message": (
            f"Quedarías con {round(new_total/60, 1)}h planificadas (límite {round(daily_limit_minutes/60, 1)}h)"
            if has_conflict else "Sin conflicto"
        ),
    }



# ─── USERS adicionales ──────────────────────────────────────

def get_user(db: Session, user_id: UUID):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def update_user(db: Session, user_id: UUID, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    return {"message": "user deleted"}


# ─── SUBJECTS adicionales ───────────────────────────────────

def get_subject(db: Session, subject_id: UUID):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject


def update_subject(db: Session, subject_id: UUID, subject: schemas.SubjectUpdate):
    db_subject = get_subject(db, subject_id)
    for key, value in subject.dict(exclude_unset=True).items():
        setattr(db_subject, key, value)
    db.commit()
    db.refresh(db_subject)
    return db_subject


# ─── CRUD POR EMAIL (más amigable para operar) ──────────────

def create_subject_by_email(db: Session, data: schemas.SubjectCreateByEmail):
    # Buscar usuario por email
    user = get_user_by_email(db, data.user_email)
    if not user:
        raise HTTPException(status_code=404, detail=f"No existe usuario con email: {data.user_email}")

    db_subject = models.Subject(
        name=data.name,
        color=data.color,
        user_id=user.id
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def get_subjects_by_email(db: Session, user_email: str):
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail=f"No existe usuario con email: {user_email}")
    return db.query(models.Subject).filter(models.Subject.user_id == user.id).all()


def create_task_by_email(db: Session, data: schemas.TaskCreateByEmail):
    # Buscar usuario por email
    user = get_user_by_email(db, data.user_email)
    if not user:
        raise HTTPException(status_code=404, detail=f"No existe usuario con email: {data.user_email}")

    # Buscar materia por nombre y usuario
    subject = (
        db.query(models.Subject)
        .filter(models.Subject.name == data.subject_name)
        .filter(models.Subject.user_id == user.id)
        .first()
    )
    if not subject:
        raise HTTPException(status_code=404, detail=f"No existe materia '{data.subject_name}' para ese usuario")

    db_task = models.Task(
        title=data.title,
        subject_id=subject.id,
        user_id=user.id,
        due_date=data.due_date,
        duration_minutes=data.duration_minutes,
        priority=data.priority,
        status=data.status
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks_by_email(db: Session, user_email: str):
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail=f"No existe usuario con email: {user_email}")
    return db.query(models.Task).filter(models.Task.user_id == user.id).all()


def get_today_view_by_email(db: Session, user_email: str):
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail=f"No existe usuario con email: {user_email}")
    return get_today_view(db, user.id)