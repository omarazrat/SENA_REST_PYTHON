# AGENTS.md

## What this is

FastAPI TODO API backed by embedded Apache Derby (JDBC via `jaydebeapi`/`jpype1`). Single package, not a monorepo. Entry point: `main.py` (`app`); DB schema is created in the FastAPI lifespan via `init_db()`.

Layer flow: `app/routes/tareas.py` (router) -> `app/schemas/tareas.py` (Pydantic) -> `app/repositories/tareas.py` (raw SQL, static `TareaRepo` methods) -> `app/db/derby.py` (connection + table creation).

## Commands

- Install: `pip install -r requirements.txt` (venv exists at `.venv`)
- Run: `uvicorn main:app --reload` — **must run from the repo root**
- No tests, linter, formatter, typecheck, or CI exist. Do not invent verification commands; smoke-test against `/docs` or `GET /` instead.

## Gotchas

- **Java JRE required on PATH.** jpype1 boots a JVM for Derby; app fails at startup without it. Derby JARs are checked in under `lib/`.
- **Working directory matters.** JDBC URL is relative (`jdbc:derby:tareas_db;create=true`), so starting uvicorn elsewhere creates a stray `tareas_db/` instead of using the real one.
- **One process at a time.** Derby embedded allows a single JVM per database. A running server (see `.uvicorn.pid`) or a stale lock makes the next startup fail with a "database already booted"/lock error — stop the old process first.
- **No migrations.** `init_db()` only creates the table if missing. Schema changes need manual DDL against the existing DB or deleting `tareas_db/` (destroys data).
- **Spanish naming is the convention.** Endpoints and fields are Spanish (`titulo`, `responsable`, `estado`: `pendiente`|`completado`). Keep new API surface consistent with that.
- Runtime/build artifacts (do not treat as source, do not hand-edit): `tareas_db/`, `__pycache__/`, `dist/`, `derby.log`, `.uvicorn.pid`.
- `dist/api-tareas.exe` is built with PyInstaller from `api-tareas.spec` (bundles `lib/` JARs); pyinstaller is not in `requirements.txt`.

## Docs

`README.md` is accurate for setup/endpoints (Spanish). If docs and code conflict, trust the code.
