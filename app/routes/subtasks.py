from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/subtasks", tags=["Subtasks"])


# Crear subtarea — T1
@router.post("/", response_model=schemas.Subtask)
def create_subtask(subtask: schemas.SubtaskCreate, db: Session = Depends(get_db)):
    return crud.create_subtask(db, subtask)


# Obtener subtareas de una tarea
@router.get("/task/{task_id}", response_model=list[schemas.Subtask])
def get_subtasks(task_id: UUID, db: Session = Depends(get_db)):
    return crud.get_subtasks_by_task(db, task_id)


# Actualizar subtarea (reprogramar fechas) — T3
@router.patch("/{subtask_id}", response_model=schemas.Subtask)
def update_subtask(subtask_id: UUID, subtask: schemas.SubtaskUpdate, db: Session = Depends(get_db)):
    return crud.update_subtask(db, subtask_id, subtask)


# Registrar avance — T4 (marcar hecho/pospuesto)
@router.patch("/{subtask_id}/status")
def update_status(subtask_id: UUID, status: str, db: Session = Depends(get_db)):
    return crud.update_subtask(db, subtask_id, schemas.SubtaskUpdate(status=status))


# Eliminar subtarea
@router.delete("/{subtask_id}")
def delete_subtask(subtask_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_subtask(db, subtask_id)


# Verificar conflicto de sobrecarga antes de reprogramar — US-07 (T3)
@router.post("/{subtask_id}/check-conflict")
def check_conflict(
    subtask_id: UUID,
    target_date: str,
    estimated_minutes: int,
    user_id: UUID,
    daily_limit_minutes: int = 360,
    db: Session = Depends(get_db),
):
    from datetime import date
    parsed_date = date.fromisoformat(target_date)
    return crud.check_overload_conflict(
        db=db,
        user_id=user_id,
        target_date=parsed_date,
        new_estimated_minutes=estimated_minutes,
        exclude_subtask_id=subtask_id,
        daily_limit_minutes=daily_limit_minutes,
    )