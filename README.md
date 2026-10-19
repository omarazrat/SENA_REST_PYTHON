# API de Tareas (TODO List)

API REST desarrollada con **FastAPI** para gestionar tareas. La información se almacena en una base de datos **Derby** (de bolsillo).

## Estructura del proyecto

```
RestPython/
├── app/
│   ├── db/           # Configuración de conexión a Derby (JayDeBeApi)
│   ├── repositories/ # Lógica de acceso a datos
│   ├── routes/       # Rutas/endpoints
│   └── schemas/      # Esquemas Pydantic (validaciones)
├── lib/              # JARs de Apache Derby
├── tareas_db/        # Base de datos Derby embebida (creada al ejecutar)
├── main.py
├── requirements.txt
└── README.md
```

## Campos de Tarea

- `id`: Identificador único (autoincremental)
- `titulo`: Título de la tarea (requerido, 1-100 caracteres)
- `descripcion`: Descripción de la tarea (opcional, 500 caracteres máx.)
- `responsable`: Persona responsable (requerido, 1-50 caracteres)
- `estado`: `pendiente` o `completado` (por defecto `pendiente`)
- `fecha_creacion`: Fecha y hora de creación
- `fecha_actualizacion`: Fecha y hora de última actualización

## Endpoints

- `GET /tareas/` - Listar todas las tareas (soporta filtro `?estado=pendiente` o `?estado=completado`)
- `GET /tareas/{id}` - Obtener tarea por ID
- `POST /tareas/` - Crear nueva tarea
- `PUT /tareas/{id}` - Actualizar tarea completa
- `DELETE /tareas/{id}` - Eliminar tarea
- `GET /` - Verificación de estado de la API

## Instalación

1. Clonar o descargar el proyecto
2. Crear entorno virtual (recomendado)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> **Nota:** Los JARs de Derby ya se encuentran en la carpeta `lib/`. Java JRE/JDK es requerido.

## Ejecución

```bash
uvicorn main:app --reload
```

La documentación automática estará disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Notas

- Base de datos Derby embebida (`jdbc:derby:tareas_db;create=true`)
- Se crea automáticamente al iniciar la aplicación
- Las tablas se crean automáticamente si no existen
- Requiere Java Runtime Environment (JRE) para ejecutar Derby
- jpype1 + jaydebeapi para conectar Python con Derby
```