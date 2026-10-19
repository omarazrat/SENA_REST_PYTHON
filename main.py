from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.derby import init_db
from app.routes import tareas

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="API de Tareas (TODO List)",
    description="API REST para gestionar tareas con Derby",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(tareas.router)

@app.get("/")
def read_root():
    return {"message": "API de Tareas funcionando correctamente"}
