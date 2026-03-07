"""
routes/subtasks.py — Endpoints CRUD para subtareas y verificación de sobrecarga.

Gestiona los pasos/subtareas dentro de una tarea. Incluye el endpoint especial
de verificación de conflicto de sobrecarga diaria (US-07).

Endpoints:
  POST   /subtasks/                    — Crea una subtarea.
  GET    /subtasks/task/{task_id}      — Lista subtareas de una tarea.
  PATCH  /subtasks/{id}                — Actualiza una subtarea (fechas, estado).
  PATCH  /subtasks/{id}/status         — Actualiza solo el estado.
  DELETE /subtasks/{id}                — Elimina una subtarea.
  POST   /subtasks/{id}/check-conflict — Verifica sobrecarga diaria (US-07).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/subtasks", tags=["Subtasks"])


@router.post("/", response_model=schemas.Subtask)
def create_subtask(subtask: schemas.SubtaskCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva subtarea asociada a una tarea (T1).

    El frontend la llama al crear una actividad con pasos desde CrearPage.

    Args:
        subtask (SubtaskCreate): Datos del paso (task_id, título, fecha, minutos).
        db (Session): Sesión de BD inyectada.

    Returns:
        Subtask: Subtarea creada.
    """
    return crud.create_subtask(db, subtask)


@router.get("/task/{task_id}", response_model=list[schemas.Subtask])
def get_subtasks(task_id: UUID, db: Session = Depends(get_db)):
    """
    Lista todas las subtareas de una tarea específica.

    Usado por ActividadPage al cargar el detalle de una tarea.

    Args:
        task_id (UUID): UUID de la tarea padre en la ruta.
        db (Session): Sesión de BD inyectada.

    Returns:
        list[Subtask]: Subtareas de la tarea.
    """
    return crud.get_subtasks_by_task(db, task_id)


@router.patch("/{subtask_id}", response_model=schemas.Subtask)
def update_subtask(subtask_id: UUID, subtask: schemas.SubtaskUpdate, db: Session = Depends(get_db)):
    """
    Actualiza una subtarea parcialmente (T3 — reprogramar fechas).

    Permite modificar título, descripción, fecha objetivo, minutos estimados
    o estado. Solo se actualizan los campos enviados en el request.

    Args:
        subtask_id (UUID): UUID de la subtarea a actualizar.
        subtask (SubtaskUpdate): Campos a modificar.
        db (Session): Sesión de BD inyectada.

    Returns:
        Subtask: Subtarea actualizada.
    """
    return crud.update_subtask(db, subtask_id, subtask)


@router.patch("/{subtask_id}/status")
def update_status(subtask_id: UUID, status: str, db: Session = Depends(get_db)):
    """
    Actualiza únicamente el estado de una subtarea (T4 — registrar avance).

    Shortcut para marcar una subtarea como hecha o pendiente sin enviar
    todos los campos del objeto.

    Args:
        subtask_id (UUID): UUID de la subtarea.
        status (str): Nuevo estado — 'pending' | 'done'.
        db (Session): Sesión de BD inyectada.

    Returns:
        Subtask: Subtarea actualizada.
    """
    return crud.update_subtask(db, subtask_id, schemas.SubtaskUpdate(status=status))


@router.delete("/{subtask_id}")
def delete_subtask(subtask_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina una subtarea por su UUID.

    Args:
        subtask_id (UUID): UUID de la subtarea a eliminar.
        db (Session): Sesión de BD inyectada.

    Returns:
        dict: Mensaje de confirmación.
    """
    return crud.delete_subtask(db, subtask_id)


@router.post("/{subtask_id}/check-conflict")
def check_conflict(
    subtask_id: UUID,
    target_date: str,
    estimated_minutes: int,
    user_id: UUID,
    daily_limit_minutes: int = 360,
    db: Session = Depends(get_db),
):
    """
    Verifica si agregar/reprogramar una subtarea genera sobrecarga diaria (US-07, T3).

    Suma los minutos estimados de todas las subtareas pendientes del usuario
    para el día indicado y evalúa si superar el límite diario (default 6h).
    Excluye la subtarea actual del conteo para evitar contarla dos veces.

    El frontend llama este endpoint desde ActividadPage al pulsar ⚡ en una subtarea.

    Args:
        subtask_id (UUID): UUID de la subtarea que se está evaluando.
        target_date (str): Fecha objetivo en formato ISO (YYYY-MM-DD).
        estimated_minutes (int): Minutos estimados de la subtarea.
        user_id (UUID): UUID del usuario propietario.
        daily_limit_minutes (int): Límite diario en minutos. Default: 360 (6h).
        db (Session): Sesión de BD inyectada.

    Returns:
        dict: Resultado con has_conflict, totales en minutos y horas, y mensaje.
    """
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