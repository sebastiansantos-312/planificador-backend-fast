"""
routes/auth.py — Endpoints de autenticación.

Gestiona el inicio de sesión de usuarios. En Sprint 1 la autenticación
es simple (email + contraseña en texto plano). No se usa JWT todavía.

Endpoints:
  POST /auth/login — Inicia sesión y retorna los datos básicos del usuario.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from .. import crud

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    """Cuerpo del request de login."""
    email: str
    password: str


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica a un usuario con email y contraseña.

    Busca el usuario por email y compara la contraseña en texto plano.
    Si las credenciales son válidas, retorna los datos de sesión que el
    frontend almacenará en localStorage.

    Args:
        data (LoginRequest): Email y contraseña del usuario.
        db (Session): Sesión de BD inyectada por FastAPI.

    Returns:
        dict: {
            "user_id": str (UUID),
            "email": str,
            "first_name": str,
            "last_name": str
        }

    Raises:
        HTTPException 401: Si el email no existe o la contraseña es incorrecta.

    TODO Sprint 2: Reemplazar comparación directa por verificación bcrypt.
    """
    user = crud.get_user_by_email(db, data.email)

    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {
        "user_id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }