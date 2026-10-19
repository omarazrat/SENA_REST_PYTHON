from typing import List, Optional
from datetime import datetime
from app.db.derby import get_connection

class TareaRepo:
    @staticmethod
    def listar(estado: Optional[str] = None) -> List[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT id, titulo, descripcion, responsable, estado, fecha_creacion, fecha_actualizacion FROM tareas"
        params = []
        if estado:
            sql += " WHERE estado = ?"
            params.append(estado)
        sql += " ORDER BY id"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        return [TareaRepo._row_to_dict(r) for r in rows]

    @staticmethod
    def obtener(tarea_id: int) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, titulo, descripcion, responsable, estado, fecha_creacion, fecha_actualizacion FROM tareas WHERE id = ?",
            [tarea_id]
        )
        row = cursor.fetchone()
        cursor.close()
        return TareaRepo._row_to_dict(row) if row else None

    @staticmethod
    def crear(titulo: str, descripcion: Optional[str], responsable: str, estado: str) -> dict:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tareas (titulo, descripcion, responsable, estado) VALUES (?, ?, ?, ?)",
            [titulo, descripcion, responsable, estado]
        )
        conn.commit()
        cursor.execute("SELECT id FROM tareas WHERE titulo = ? AND responsable = ? ORDER BY id DESC", [titulo, responsable])
        new_id = cursor.fetchone()[0]
        cursor.close()
        return TareaRepo.obtener(new_id)

    @staticmethod
    def actualizar(tarea_id: int, titulo: str, descripcion: Optional[str], responsable: str, estado: str) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tareas SET titulo = ?, descripcion = ?, responsable = ?, estado = ?, fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = ?",
            [titulo, descripcion, responsable, estado, tarea_id]
        )
        updated = cursor.rowcount
        conn.commit()
        cursor.close()
        if not updated:
            return None
        return TareaRepo.obtener(tarea_id)

    @staticmethod
    def eliminar(tarea_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", [tarea_id])
        deleted = cursor.rowcount
        conn.commit()
        cursor.close()
        return bool(deleted)

    @staticmethod
    def _row_to_dict(row) -> dict:
        return {
            "id": row[0],
            "titulo": row[1],
            "descripcion": row[2],
            "responsable": row[3],
            "estado": row[4],
            "fecha_creacion": row[5],
            "fecha_actualizacion": row[6],
        }
