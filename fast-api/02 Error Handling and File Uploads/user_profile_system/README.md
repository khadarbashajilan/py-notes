# User Profile System

A simple REST API built with **FastAPI** for managing user profiles with avatar uploads, backed by an in-memory store. Designed as a learning project to demonstrate layered architecture, custom exception handling, file uploads with real type validation, and static file serving.

## Tech Stack

- **FastAPI** (modern, high-performance web framework)
- **Pydantic** v2 (data validation, `EmailStr`)
- **Uvicorn** (ASGI server)
- **filetype** (magic-byte file-type detection)
- **uv** (dependency + virtualenv management)
- Python 3.14+

## Setup & Run

```bash
# Move into the project
cd "fast-api/02 Error Handling and File Uploads/user_profile_system"

# Sync dependencies (creates .venv and installs fastapi[standard] + filetype)
uv sync

# Start the server
uv run fastapi dev app/main.py
# or: uv run uvicorn app.main:app --reload
```

Visit **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

## API Endpoints

| Method | Endpoint                    | Description                  | Status Code |
|--------|-----------------------------|------------------------------|-------------|
| GET    | `/`                         | Welcome message              | 200         |
| POST   | `/users/`                   | Create a new user            | 201         |
| POST   | `/users/{username}/avatar`  | Upload / replace user avatar | 200         |
| GET    | `/users/user/{username}`    | Get user profile by username | 200         |

Uploaded avatars are stored under `/uploads/` and served statically, so the returned `avatar_url` is a fully qualified URL (e.g. `http://127.0.0.1:8000/uploads/<uuid>.png`).

### Error Response Shape

All custom errors follow a consistent JSON envelope:

```json
{
  "error": true,
  "error_code": "INVALID_FILETYPE",
  "message": "Unsupported file type. Allowed types are: JPEG, PNG, WEBP.",
  "path": "/users/<username>/avatar"
}
```

## Request Examples

### Create a User

```json
POST /users/
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secret123"
}
```

### Upload an Avatar

```bash
curl -F "file=@avatar.png" http://127.0.0.1:8000/users/alice/avatar
```

Response:

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "avatar_url": "http://127.0.0.1:8000/uploads/939e00ff1e8742cfbef42b04260ca61c.png"
}
```

### Get a User

```json
GET /users/user/alice
{
  "username": "alice",
  "email": "alice@example.com",
  "avatar_url": "http://127.0.0.1:8000/uploads/939e00ff1e8742cfbef42b04260ca61c.png"
}
```

## Project Structure

```
02 Error Handling and File Uploads/user_profile_system/
├── app/
│   ├── api/routes/
│   │   └── users.py          # Route definitions
│   ├── core/
│   │   ├── config.py         # Settings (upload dir, max size, allowed types)
│   │   ├── exceptions.py     # Custom AppException hierarchy + handler
│   │   └── middleware.py     # Request logging middleware
│   ├── schemas/
│   │   └── user.py           # Pydantic schemas (UserCreate, UserResponse)
│   ├── services/
│   │   ├── file_service.py   # Avatar upload / validation logic
│   │   └── user_service.py   # User CRUD (in-memory store)
│   └── main.py               # FastAPI app entry point
├── uploads/                  # Stored avatar files (served statically)
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Features

- Layered architecture (routes → services → schemas / core)
- Custom exception hierarchy with a consistent error envelope
- Avatar upload with **real** file-type validation via `filetype` (magic bytes, not just `content_type`)
- File-size limit enforcement (1 MB)
- Static serving of uploaded files via `StaticFiles`
- Request logging middleware
- Fully qualified avatar URLs in responses
- Interactive API docs at `/docs`
