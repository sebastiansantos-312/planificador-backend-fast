"""
models.py — Modelos ORM que representan las tablas de la base de datos.
"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
import uuid

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    birth_date = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    color = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())


class Task(Base):
    """
    Tabla 'tasks' — Actividad académica.

    Columns:
        task_type (str): Tipo de actividad — 'examen' | 'quiz' | 'taller' |
                         'proyecto' | 'exposición' | 'otro'. Requerido por US-01.
    """
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    task_type = Column(String)                                    # ← NUEVO (US-01)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    due_date = Column(Date)
    duration_minutes = Column(Integer)
    priority = Column(String)
    status = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Subtask(Base):
    __tablename__ = "subtasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    title = Column(String)
    description = Column(Text)
    target_date = Column(Date)
    estimated_minutes = Column(Integer)
    status = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())