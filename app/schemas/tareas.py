from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TareaBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    responsable: str = Field(..., min_length=1, max_length=50)
    estado: str = Field("pendiente", pattern=r"^(pendiente|completado)$")

class TareaCreate(TareaBase):
    pass

class TareaUpdate(TareaBase):
    pass

class TareaOut(TareaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True
