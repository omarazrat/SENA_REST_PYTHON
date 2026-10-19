from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.schemas.tareas import TareaCreate, TareaUpdate, TareaOut
from app.repositories.tareas import TareaRepo

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.get("/", response_model=List[TareaOut])
def listar_tareas(estado: Optional[str] = Query(None, pattern=r"^(pendiente|completado)$")):
    return TareaRepo.listar(estado)

@router.get("/{tarea_id}", response_model=TareaOut)
def obtener_tarea(tarea_id: int):
    tarea = TareaRepo.obtener(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@router.post("/", response_model=TareaOut, status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: TareaCreate):
    return TareaRepo.crear(
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        responsable=tarea.responsable,
        estado=tarea.estado
    )

@router.put("/{tarea_id}", response_model=TareaOut)
def actualizar_tarea(tarea_id: int, tarea: TareaUpdate):
    actualizada = TareaRepo.actualizar(
        tarea_id,
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        responsable=tarea.responsable,
        estado=tarea.estado
    )
    if not actualizada:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return actualizada

@router.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(tarea_id: int):
    if not TareaRepo.eliminar(tarea_id):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
