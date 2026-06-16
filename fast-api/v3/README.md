# FastAPI v3 — Credential Manager API

## Rating: 7/10

An async password credential manager with SQLite persistence, SQLAlchemy ORM, input validation, and proper RESTful routing. A major leap from v2 — data now survives server restarts — but still lacks DI, CORS, tests, and security hardening.

---

## ✅ What's Good

1. **Persistent database** — SQLite via SQLAlchemy async engine. Data survives server restarts, unlike v1/v2 in-memory storage.
2. **Async everywhere** — All route handlers and database operations use `async def` / `await`. Proper FastAPI pattern.
3. **Four-layer architecture** — `main.py` (routes) → `repository.py` (CRUD) → `model.py` (schemas + ORM) → `database.py` (engine). Clear separation of concerns.
4. **Lifespan context manager** — Uses modern `@asynccontextmanager` lifespan pattern (not deprecated `on_event`).
5. **Duplicate prevention** — POST checks for existing `service_name` before creating, returns 409 on conflict.
6. **Pydantic field validators** — `@field_validator` rejects empty `service_name` and `password` with automatic 422 responses.
7. **Correct HTTP status codes** — 201 for creation, 404 for not found, 422 for validation errors.
8. **Partial updates** — `PATCH /credentials/{id}` uses `UpdateCred` with all-Optional fields and `exclude_unset=True`.
9. **Proper error messages** — Clear, consistent `detail` strings in all `HTTPException` responses.
10. **Type annotations everywhere** — All functions and route handlers have return types.

---

## ❌ What Can Be Improved

### Storage & Persistence
1. **No unique constraint at DB level** — Duplicate `service_name` check is application-only. A race condition could bypass it. Add `unique=True` to the column.
2. **No password encryption** — Passwords are stored in plaintext in `passwords.db`. Use `passlib` + `bcrypt` to hash before storage.

### Code Quality & Correctness
3. **No dependency injection** — Each `repository.py` function creates its own session with `async with AsyncSessionLocal()`. Hard to swap DB for testing. v4 will fix this with `Depends(get_db)`.
4. **No service layer** — `repository.py` mixes data access and business logic (validation, error handling). Extracting business rules would improve testability.
5. **No cascade delete** — No `DELETE` endpoint exists. Credentials can only be created and updated, never removed.
6. **Flat error messages** — `detail` strings are meaningful but unstructured. Consider standardised JSON error envelopes for machine consumers.

### Infrastructure & Configuration
7. **No CORS middleware** — Browsers from different origins cannot call this API. Add `CORSMiddleware` from `starlette.middleware.cors`.
8. **No authentication** — The API is completely open. No JWT, OAuth2, or API keys. Every endpoint is publicly writable.
9. **No environment configuration** — No `.env`, no `pydantic-settings`. `DATABASE_URL` is hardcoded in `database.py`.
10. **No logging** — No `logging` setup. The only output is a `print()` on startup/shutdown.
11. **No global exception handlers** — No `@app.exception_handler` for standardised error responses across all endpoints.

### Testing & DevOps
12. **No tests** — Zero automated tests. Each `repository.py` function creates its own session, making isolation slightly easier than v1/v2's global list, but still no test suite.
13. **No `.gitignore`** — `__pycache__/`, `.venv/`, and `passwords.db` should be excluded from version control.
14. **No CI/CD** — No GitHub Actions, Dockerfile, or deployment pipeline.
