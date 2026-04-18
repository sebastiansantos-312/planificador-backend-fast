"""
main.py — Punto de entrada de la API REST del Planificador de Estudio.

Este archivo inicializa la aplicación FastAPI, configura el middleware CORS
para permitir peticiones desde el frontend (Vercel), y registra todos los
routers de la aplicación.

Flujo de arranque:
  1. Se crean las tablas en la base de datos si no existen.
  2. Se inicializan las materias estáticas (Matemáticas, Ciencias Naturales, etc).
  3. Se instancia la aplicación FastAPI.
  4. Se configura CORS para aceptar peticiones de cualquier origen.
  5. Se registran los routers: auth, users, subjects, tasks, subtasks.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import models
from .routes import tasks, users, subjects, subtasks, auth

# 1. Crear tablas en la BD a partir de los modelos SQLAlchemy
Base.metadata.create_all(bind=engine)

# 2. Inicializar materias estáticas
try:
    from .database import SessionLocal
    from . import crud, models
    
    STATIC_SUBJECTS = [
        {"name": "Matemáticas", "color": "#FF0000"},
        {"name": "Ciencias Naturales", "color": "#40E0D0"},
        {"name": "Lenguas", "color": "#ADD8E6"},
        {"name": "Historia", "color": "#FFFF00"},
        {"name": "Geografía", "color": "#800080"},
        {"name": "Inglés", "color": "#E6E6FA"},
    ]
    
    db = SessionLocal()
    for subj_data in STATIC_SUBJECTS:
        existing = db.query(models.Subject).filter(models.Subject.name == subj_data["name"]).first()
        if not existing:
            db_subject = models.Subject(name=subj_data["name"], color=subj_data["color"])
            db.add(db_subject)
    db.commit()
    db.close()
except Exception as e:
    print(f"Advertencia: No se pudieron inicializar las materias estáticas: {e}")

# 3. Instanciar la aplicación
app = FastAPI(title="Study Planner API", version="1.0.0")

# 4. Configurar CORS
# allow_origins=["*"] permite peticiones desde cualquier dominio.
# En producción se debería restringir a la URL del frontend en Vercel.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Registrar routers — cada uno agrupa los endpoints de su dominio
app.include_router(auth.router)       # POST /auth/login
app.include_router(users.router)      # CRUD /users/
app.include_router(subjects.router)   # CRUD /subjects/
app.include_router(tasks.router)      # CRUD /tasks/ + vista /hoy
app.include_router(subtasks.router)   # CRUD /subtasks/ + check-conflict


@app.get("/")
def root():
    """Endpoint raíz. Confirma que la API está activa."""
    return {"message": "Study Planner API running ✅"}


@app.get("/health")
def health():
    """Health check. Usado por Render para verificar que el servicio responde."""
    return {"status": "ok"}


@app.get("/debug/subjects")
def debug_subjects():
    """Debug endpoint para verificar todas las materias en la BD."""
    from .database import SessionLocal
    from . import models
    db = SessionLocal()
    try:
        all_subjects = db.query(models.Subject).all()
        return {
            "total_subjects": len(all_subjects),
            "subjects": [{"id": str(s.id), "name": s.name, "color": s.color} for s in all_subjects]
        }
    finally:
        db.close()