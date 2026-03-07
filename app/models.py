"""
models.py — Modelos ORM que representan las tablas de la base de datos.

Cada clase corresponde a una tabla en PostgreSQL (Supabase).
SQLAlchemy mapea automáticamente los atributos de clase a columnas de la BD.

Tablas:
  - users:    Usuarios registrados en el sistema.
  - subjects: Materias o asignaturas del usuario.
  - tasks:    Tareas o actividades académicas.
  - subtasks: Pasos o subtareas dentro de una tarea.

Relaciones:
  subjects.user_id  → users.id
  tasks.user_id     → users.id
  tasks.subject_id  → subjects.id
  subtasks.task_id  → tasks.id
"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
import uuid

from .database import Base


class User(Base):
    """
    Tabla 'users' — Representa un usuario registrado en el sistema.

    Columns:
        id (UUID): Identificador único generado automáticamente.
        first_name (str): Nombre del usuario.
        last_name (str): Apellido del usuario.
        email (str): Correo electrónico único. Usado para login y consultas.
        password (str): Contraseña en texto plano (Sprint 1). 
                        TODO Sprint 2: hashear con bcrypt.
        birth_date (date): Fecha de nacimiento (opcional).
        created_at (timestamp): Fecha de registro, asignada por la BD.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    birth_date = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Subject(Base):
    """
    Tabla 'subjects' — Representa una materia o asignatura del usuario.

    Columns:
        id (UUID): Identificador único generado automáticamente.
        name (str): Nombre de la materia (ej: 'Cálculo', 'Bases de Datos').
        color (str): Color hex para identificar visualmente la materia en el frontend.
        user_id (UUID): FK → users.id. Propietario de la materia.
        created_at (timestamp): Fecha de creación.
    """
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    color = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())


class Task(Base):
    """
    Tabla 'tasks' — Representa una actividad o tarea académica.

    Columns:
        id (UUID): Identificador único generado automáticamente.
        title (str): Título descriptivo de la tarea.
        subject_id (UUID): FK → subjects.id. Materia a la que pertenece.
        user_id (UUID): FK → users.id. Propietario de la tarea.
        due_date (date): Fecha límite de entrega.
        duration_minutes (int): Tiempo estimado total en minutos.
        priority (str): Nivel de prioridad — 'alta' | 'media' | 'baja'.
        status (str): Estado actual — 'pending' | 'in_progress' | 'done'.
        created_at (timestamp): Fecha de creación.
    """
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    due_date = Column(Date)
    duration_minutes = Column(Integer)
    priority = Column(String)
    status = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Subtask(Base):
    """
    Tabla 'subtasks' — Representa un paso o subtarea dentro de una tarea.

    Las subtareas son la unidad mínima de planificación diaria. La vista 'Hoy'
    del frontend muestra subtareas agrupadas por fecha objetivo.

    Columns:
        id (UUID): Identificador único generado automáticamente.
        task_id (UUID): FK → tasks.id. Tarea padre a la que pertenece.
        title (str): Título del paso (ej: 'Leer capítulo 3').
        description (str): Descripción detallada opcional.
        target_date (date): Fecha objetivo en que se planea completar el paso.
        estimated_minutes (int): Tiempo estimado para completar el paso.
        status (str): Estado — 'pending' | 'done'.
        created_at (timestamp): Fecha de creación.
    """
    __tablename__ = "subtasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    title = Column(String)
    description = Column(Text)
    target_date = Column(Date)
    estimated_minutes = Column(Integer)
    status = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())