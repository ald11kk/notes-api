# Notes API

A persistent REST API for creating, reading, updating, and deleting notes, backed by PostgreSQL and built with async Python.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.13 | Language |
| uv | Dependency and environment management |
| FastAPI | Web framework and routing |
| Pydantic + pydantic-settings | Request/response validation and config |
| SQLAlchemy (async) | ORM and async database sessions |
| asyncpg | Async PostgreSQL driver |
| Alembic | Database schema migrations |
| Docker Compose | PostgreSQL service |
| uvicorn | ASGI server |

---

## Project Structure

```
notes-api/
├── app/
│   ├── __init__.py
│   ├── config.py        # Pydantic settings — loads DATABASE_URL from .env
│   ├── database.py      # Async engine, session factory, get_db dependency
│   ├── models.py        # SQLAlchemy Note model (notes table)
│   ├── main.py          # FastAPI app and all route handlers
│   └── schemas.py       # Pydantic schemas: NoteCreate, NoteUpdate, Note
├── migrations/
│   ├── env.py           # Alembic async config — reads DATABASE_URL from settings
│   ├── script.py.mako
│   └── versions/
│       └── e0022cc4238a_init_notes_table.py
├── alembic.ini
├── docker-compose.yaml  # PostgreSQL 17 service
├── pyproject.toml
└── .env                 # Local env vars (not committed)
```

---

## Database Schema

The `notes` table has these columns:

| Column | Type | Notes |
|--------|------|-------|
| `id` | integer | Primary key, auto-increment |
| `title` | varchar(255) | Required |
| `content` | text | Required |
| `created_at` | datetime | Set on insert via `func.now()` |
| `updated_at` | datetime | Set on insert, updated on change |

---

## API Endpoints

### `POST /notes/`

Create a new note.

**Request body:**
```json
{
  "title": "My first note",
  "content": "Hello, world."
}
```

**Response** (`201 Created`):
```json
{
  "id": 1,
  "title": "My first note",
  "content": "Hello, world.",
  "created_at": "2025-01-01T12:00:00"
}
```

---

### `GET /notes/`

Return all notes.

---

### `GET /notes/{id}`

Return a single note by ID. Returns `404` if not found.

---

### `PATCH /notes/{id}`

Partially update a note. Both fields are optional.

**Request body:**
```json
{
  "title": "Updated title"
}
```

---

### `DELETE /notes/{id}`

Delete a note. Returns `204 No Content`. Returns `404` if not found.

---

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/notes_db
```

The `config.py` file loads this automatically via `pydantic-settings`.

---

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- Docker

### 1. Start the database

```bash
docker compose up -d
```

This starts a PostgreSQL 17 container on port `5432` with:
- user: `user`
- password: `password`
- database: `notes_db`

### 2. Install dependencies

```bash
uv sync
```

### 3. Apply migrations

```bash
uv run alembic upgrade head
```

### 4. Run the server

```bash
uv run uvicorn app.main:app --reload
```

API available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## Running Tests

```bash
uv run pytest -v
```

---

## Learning Goals

This project introduces the core backend data layer pattern:

- **SQLAlchemy async ORM** — Python classes mapped to database tables, with `await` on every query
- **Alembic migrations** — schema changes tracked as versioned files, applied forward or rolled back safely
- **FastAPI dependency injection** — `Depends(get_db)` creates a session per request and closes it after
- **Pydantic settings** — environment variables loaded and validated at startup, never hardcoded
- **Docker Compose** — local PostgreSQL running in one command, no manual installation