from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


# ✅ Crear tarea con email + nombre de materia
@router.post("/by-email", response_model=schemas.Task)
def create_task_by_email(task: schemas.TaskCreateByEmail, db: Session = Depends(get_db)):
    return crud.create_task_by_email(db, task)


@router.get("/", response_model=list[schemas.Task])
def get_tasks(user_id: UUID, db: Session = Depends(get_db)):
    return crud.get_tasks(db, user_id)


# ✅ Obtener tareas con email
@router.get("/by-email", response_model=list[schemas.Task])
def get_tasks_by_email(user_email: str, db: Session = Depends(get_db)):
    return crud.get_tasks_by_email(db, user_email)


@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    return crud.get_task(db, task_id)


@router.patch("/{task_id}", response_model=schemas.Task)
def update_task(task_id: UUID, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task(db, task_id, task)


@router.delete("/{task_id}")
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_task(db, task_id)


# ✅ Vista Hoy con email
@router.get("/hoy/prioridades")
def get_today(user_email: str = None, user_id: UUID = None, db: Session = Depends(get_db)):
    if user_email:
        return crud.get_today_view_by_email(db, user_email)
    if user_id:
        return crud.get_today_view(db, user_id)
    from fastapi import HTTPException
    raise HTTPException(status_code=400, detail="Debes enviar user_email o user_id")
