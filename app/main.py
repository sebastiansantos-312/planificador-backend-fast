# ============================================================

# ============================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import models
from .routes import tasks, users, subjects, subtasks, auth

# 1️ crear tablas
Base.metadata.create_all(bind=engine)

# 2 crear app
app = FastAPI(title="Study Planner API", version="1.0.0")

# 3️ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción: URL de Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4️⃣ Registrar routers (UNA sola vez cada uno)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(subjects.router)
app.include_router(tasks.router)
app.include_router(subtasks.router)

@app.get("/")
def root():
    return {"message": "Study Planner API running ✅"}

@app.get("/health")
def health():
    return {"status": "ok"}