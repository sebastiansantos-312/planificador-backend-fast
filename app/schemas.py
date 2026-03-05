from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID
from typing import Optional


# ─── USER ───────────────────────────────────────────
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    birth_date: Optional[date] = None

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    birth_date: Optional[date] = None

class User(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── SUBJECT ────────────────────────────────────────
class SubjectCreate(BaseModel):
    name: str
    color: Optional[str] = None
    user_id: UUID

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

class Subject(BaseModel):
    id: UUID
    name: str
    color: Optional[str] = None
    user_id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── TASK ───────────────────────────────────────────
class TaskCreate(BaseModel):
    title: str
    subject_id: Optional[UUID] = None
    user_id: UUID
    due_date: Optional[date] = None
    duration_minutes: Optional[int] = None
    priority: Optional[str] = None   # "high" | "medium" | "low"
    status: Optional[str] = "pending"  # "pending" | "in_progress" | "done"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    subject_id: Optional[UUID] = None
    due_date: Optional[date] = None
    duration_minutes: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class Task(BaseModel):
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


# ─── SUBTASK ────────────────────────────────────────
class SubtaskCreate(BaseModel):
    task_id: UUID
    title: str
    description: Optional[str] = None
    target_date: Optional[date] = None
    estimated_minutes: Optional[int] = None
    status: Optional[str] = "pending"  # "pending" | "in_progress" | "done" | "postponed"


class SubtaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    estimated_minutes: Optional[int] = None
    status: Optional[str] = None


class Subtask(BaseModel):
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



class SubjectCreateByEmail(BaseModel):
    name: str
    color: Optional[str] = None
    user_email: str  # en vez de user_id


class TaskCreateByEmail(BaseModel):
    title: str
    subject_name: str  # nombre de la materia en vez de subject_id
    user_email: str    # en vez de user_id
    due_date: Optional[date] = None
    duration_minutes: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = "pending"