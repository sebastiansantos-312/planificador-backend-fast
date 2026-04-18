"""
schemas.py — Esquemas Pydantic para validación y serialización de datos.

Pydantic valida automáticamente los datos de entrada (request body) y salida
(response) de cada endpoint. Si los datos no cumplen el esquema, FastAPI
retorna un error 422 automáticamente.

Convención de nomenclatura:
  - XxxCreate:        Datos requeridos para crear un recurso (entrada).
  - XxxUpdate:        Campos opcionales para actualizar un recurso (entrada PATCH).
  - Xxx:              Representación completa del recurso (salida/response).
  - XxxCreateByEmail: Variante que acepta email en lugar de UUID (más amigable).
"""

from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID
from typing import Optional


# ─── USER ────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    """Datos requeridos para registrar un nuevo usuario."""
    first_name: str
    last_name: str
    email: str
    password: str
    birth_date: Optional[date] = None


class UserUpdate(BaseModel):
    """Campos opcionales para actualizar el perfil de un usuario (PATCH)."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    birth_date: Optional[date] = None


class User(BaseModel):
    """
    Representación de un usuario en las respuestas de la API.
    No incluye la contraseña por seguridad.
    """
    id: UUID
    first_name: str
    last_name: str
    email: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permite convertir objetos ORM a este esquema


# ─── SUBJECT ─────────────────────────────────────────────────────────────────

class Subject(BaseModel):
    """Representación completa de una materia en las respuestas de la API."""
    id: UUID
    name: str
    color: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── TASK ────────────────────────────────────────────────────────────────────

class TaskCreate(BaseModel):
    """Datos requeridos para crear una tarea usando IDs directamente."""
    title: str
    subject_id: Optional[UUID] = None
    user_id: UUID
    due_date: Optional[date] = None
    duration_minutes: Optional[int] = None
    priority: Optional[str] = None    # Valores: 'alta' | 'media' | 'baja'
    status: Optional[str] = "pending" # Valores: 'pending' | 'in_progress' | 'done'


class TaskUpdate(BaseModel):
    """Campos opcionales para actualizar una tarea (PATCH)."""
    title: Optional[str] = None
    subject_id: Optional[UUID] = None
    due_date: Optional[date] = None
    duration_minutes: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class Task(BaseModel):
    """Representación completa de una tarea en las respuestas de la API."""
    id: UUID
    title: str
    subject_id: Optional[UUID] = None
    user_id: UUID
    due_date: Optional[date] = None
    duration_minutes: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── SUBTASK ─────────────────────────────────────────────────────────────────

class SubtaskCreate(BaseModel):
    """Datos requeridos para crear una subtarea (paso de una tarea)."""
    task_id: UUID
    title: str
    description: Optional[str] = None
    target_date: Optional[date] = None
    estimated_minutes: Optional[int] = None
    status: Optional[str] = "pending"  # Valores: 'pending' | 'done'


class SubtaskUpdate(BaseModel):
    """Campos opcionales para actualizar una subtarea (PATCH)."""
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    estimated_minutes: Optional[int] = None
    status: Optional[str] = None


class Subtask(BaseModel):
    """Representación completa de una subtarea en las respuestas de la API."""
    id: UUID
    task_id: UUID
    title: str
    description: Optional[str] = None
    target_date: Optional[date] = None
    estimated_minutes: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── VARIANTES POR EMAIL ─────────────────────────────────────────────────────
# Estas variantes permiten usar el email del usuario en lugar de su UUID.
# Son más amigables para el frontend, que almacena el email en localStorage.


class TaskCreateByEmail(BaseModel):
    """
    Alternativa a TaskCreate que acepta email y nombre de materia
    en lugar de UUIDs. El backend resuelve los IDs internamente.
    """
    title: str
    subject_name: str   # Nombre de la materia en lugar de subject_id
    user_email: str     # Email del usuario en lugar de user_id
    due_date: Optional[date] = None
    duration_minutes: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = "pending"