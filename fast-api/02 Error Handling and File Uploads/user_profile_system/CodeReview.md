# Code Review: User Profile System

## Overview

A FastAPI-based REST API for managing user profiles with avatar uploads, backed by an in-memory store. Builds on the layered patterns of the Product API project and focuses on error handling, file uploads with real type validation, and static file serving.

**Tech Stack:** FastAPI, Pydantic v2 (`EmailStr`), Uvicorn, filetype, uv, Python 3.14+

---

## 1. Architecture (Rating: 9/10)

Clean layered separation with single responsibility per module:

```
Routes (users.py)        →  HTTP concerns, request/response shaping
Services (user/file)     →  Business logic
Schemas (user.py)        →  Data schemas + validation
Core (config/exceptions) →  Settings + cross-cutting error handling
```

FastAPI patterns are used correctly: `APIRouter(prefix="/users")`, proper `response_model` typing, status codes, custom exception handler, and `StaticFiles` mount for uploads.

**Strengths:**
- Clear dependency direction (routes → services → schemas/core)
- `main.py` is minimal and clean (app creation, middleware, handler, router, mount)
- `core/` cleanly isolates reusable infrastructure (config, exceptions, middleware)

**Issues:**
- 🟢 In-memory store lives *inside* `user_service.py` rather than a dedicated `db/` module (the Product API used `db/memory.py`). Minor, but inconsistent with the project's own convention.

---

## 2. Models & Validation (Rating: 6/10)

### `UserCreate`
- Good use of `EmailStr` for email validation
- ❌ **No `Field()` constraints on `username`** — accepts empty string, whitespace, or arbitrarily long values
- ❌ **No constraints on `password`** — accepts empty / weak passwords

### `UserResponse`
- `avatar_url: str | None = None` correctly models an optional avatar
- After the recent fix it returns a fully qualified URL — good for clients

**Issues:**
- 🔴 `password` is stored as **plaintext** in the in-memory dict (`user_service.py`). Even for a learning project, a profile system should at minimum hash (e.g. `bcrypt`/`passlib`). The code even carries a `# demo only` comment acknowledging this — it should be fixed or the field removed from the demo.
- 🟡 `UserCreate` lacks the `Field(min_length=..., max_length=...)` validation that `ProductCreate` had in the sibling project.

---

## 3. Services & Business Logic (Rating: 8/10)

- `user_service` exposes clean `create_new_user` / `get_user_by_username` / `update_avatar` with the right custom exceptions (404 / 409)
- `file_service.upload_avatar` correctly re-checks user existence, validates type via **magic bytes** (`filetype.guess`), enforces size, and persists the file
- Returns a fully qualified `avatar_url` built from `request.base_url`

**Issues:**
- 🟡 `filetype.guess(contents)` is called **twice** — once in `_validate()` and again to derive the extension. Cache the `kind` once.
- 🟡 **Orphaned files on re-upload** — uploading a new avatar does not delete the old file, so `uploads/` accumulates stale avatars.
- 🟡 **Disk / memory inconsistency on restart** — the in-memory user store resets on restart (all users gone), but previously uploaded avatar files remain in `uploads/` and stay publicly reachable at their old URLs.
- 🟢 `upload_avatar` is typed `async` but does only blocking `open(...).write(...)`; for 1 MB this is fine, but large writes should move to a threadpool (`await run_in_threadpool`).

---

## 4. Code Quality & Style (Rating: 7/10)

| Aspect | Rating | Notes |
|--------|--------|-------|
| Readability | 9/10 | Clear names, easy to follow |
| Consistency | 7/10 | Mostly consistent imports now use `app.` prefix throughout |
| Python idioms | 8/10 | Good use of `uuid`, `os.path.join` |
| Error handling | 8/10 | Consistent `AppException` envelope |

**Issues:**
- 🟢 A code comment (`# demo only: never store plaintext in real apps`) was left in `user_service.py` — acceptable as a warning, but the underlying behavior should still be addressed.
- 🟢 `core/middleware.py` uses `print()` for logging instead of the `logging` module.

---

## 5. Config & Dev Experience (Rating: 4/10)

- ❌ **`requirements.txt` is empty** — `pip install -r requirements.txt` does nothing (deps live in `pyproject.toml` + `uv.lock`, which is fine, but the empty file is misleading)
- ❌ **`pyproject.toml`** still has the placeholder `description = "Add your description here"`
- ❌ **No tests** — no `tests/` directory and no `pytest` in dependencies
- ❌ **`.gitignore` is empty** — `.venv/`, `__pycache__/`, and `uploads/` (binary files) are not ignored and risk being committed
- ✅ Modern tooling: `uv.lock` present, `filetype` correctly added as a dependency

---

## 6. Security (Rating: 3/10)

- 🔴 **Plaintext passwords** in the in-memory store
- 🟡 `/uploads` is mounted as fully public `StaticFiles` — fine for avatars, but any uploaded file is world-readable by URL
- 🟡 No authentication / authorization on any endpoint (anyone can fetch or overwrite any user's avatar)
- Appropriate to flag rather than block for a learning project, but these must be addressed before any real use

---

## 7. Overall Score: 7/10

### What's Good
- Clean, well-organized structure with proper separation of concerns
- Excellent FastAPI conventions (response models, custom exception handler, router tags, static mount)
- Real file-type validation via magic bytes — more robust than trusting `content_type`
- Fully qualified avatar URLs in responses
- Request logging middleware demonstrates cross-cutting concerns

### What Needs Fixing

| Priority | Issue | File | Line |
|----------|-------|------|------|
| 🔴 High | Passwords stored as plaintext | `services/user_service.py` | 19-24 |
| 🟡 Medium | `UserCreate` missing `Field` constraints (username/password) | `schemas/user.py` | 4-7 |
| 🟡 Medium | Orphaned files on avatar re-upload | `services/file_service.py` | 31-35 |
| 🟡 Medium | Disk/memory inconsistency on restart | `services/*` + `uploads/` | — |
| 🟢 Low | `filetype.guess` called twice | `services/file_service.py` | 12, 31 |
| 🟢 Low | Empty `requirements.txt` | `requirements.txt` | — |
| 🟢 Low | Placeholder description in `pyproject.toml` | `pyproject.toml` | 4 |
| 🟢 Low | Empty `.gitignore` (venv/cache/uploads not ignored) | `.gitignore` | — |
| 🟢 Low | `print()` used instead of `logging` | `core/middleware.py` | 7, 11 |
| 🟢 Low | In-memory store embedded in service vs dedicated `db/` module | `services/user_service.py` | 5 |

### Recommendations
1. Hash passwords (e.g. `passlib[bcrypt]`) or drop the password field from the demo
2. Add `Field(min_length=3, max_length=30)` to `username` and a minimum length to `password`
3. Delete the previous avatar file when a new one is uploaded
4. Add basic auth (or at least ownership checks) before exposing avatar overwrite
5. Populate `.gitignore` (`.venv/`, `__pycache__/`, `uploads/`) and `pyproject.toml` description
6. Cache the `filetype.guess` result instead of calling it twice
7. Add `pytest` + `httpx` tests covering create, 404, duplicate, bad file type, and oversize
8. Switch middleware `print` calls to the `logging` module
