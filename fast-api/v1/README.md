# FastAPI v1 — Product CRUD API

## Rating: 4/10

A minimal FastAPI product management API using in-memory storage. Functional as a learning project but needs significant improvements for production readiness.

---

## ✅ What's Good

1. **Minimal & focused** — Small codebase, easy to understand, great for beginners learning FastAPI.
2. **Separation of concerns** — Models are in `models.py`, routes are in `main.py`. Good foundational structure.
3. **Correct FastAPI patterns** — Proper use of `HTTPException` for 404s, Pydantic models for request validation, typed path parameters.
4. **Clear CRUD naming** — Function names (`add_product`, `get_product`, `update_product`, `delete_product`) are self-documenting.
5. **Modern Python tooling** — Uses `uv` for dependency management, `pyproject.toml`, targets Python 3.14.
6. **All standard extras included** — `fastapi[standard]` brings in uvicorn, Jinja2, python-multipart, httpx, pydantic-settings, CORS support, and more — ready to use but not yet leveraged.

---

## ❌ What Can Be Improved

### Storage & Persistence
1. **No database** — Data lives in a Python list (`products = []`) and is wiped on every server restart. Add SQLite/PostgreSQL with SQLAlchemy or a simple file-based store.
2. **Client-supplied ID allows duplicates** — The `id` field is sent by the client in the POST body. A client can create multiple products with the same `id`, and update/delete only affect the first match. Auto-generate IDs server-side.

### Code Quality & Correctness
3. **No async handlers** — All route handlers use `def` instead of `async def`. FastAPI handles sync functions via a thread pool, but async is more efficient for I/O-bound operations.
4. **No field validation constraints** — The `Product` model accepts negative prices, negative quantities, and empty names. Use Pydantic's `Field(gt=0)`, `min_length`, etc.
5. **Wrong HTTP status codes** — `POST /add` should return `201 Created` (not 200). `DELETE /delete/{id}` should return `204 No Content` (not 200 with a body).
6. **No return type annotations** — Route handlers lack `-> dict`, `-> Product`, `-> list` return types, reducing IDE support and self-documentation.
7. **Typo & inconsistent messaging** — `"Its Empty"` (line 16) should be `"Empty"` or `"It's Empty"`. Error messages use `"Product not found"` (capitalized) on lines 34/45 but `"product not found"` (lowercase) on line 56.
8. **Non-RESTful URL design** — Paths like `/all`, `/add`, `/delete/{id}` don't follow REST conventions. Use resource-based paths: `GET /products`, `POST /products`, `GET /products/{id}`, `PUT /products/{id}`, `DELETE /products/{id}`.
9. **No service/repository layer** — CRUD logic is mixed directly into route handlers. Extract business logic into a service layer for testability and reusability.
10. **No dependency injection** — No use of FastAPI's `Depends()`. Dependencies like DB sessions or auth should be injected rather than hardcoded.

### Infrastructure & Configuration
11. **No CORS middleware** — Browsers from different origins cannot call this API. Add `CORSMiddleware` from `starlette.middleware.cors`.
12. **No authentication or security** — The API is completely open. No OAuth2, JWT, API keys, or basic auth. Every endpoint is publicly writable.
13. **No environment configuration** — No `.env` file, no `pydantic-settings` usage. Configuration like DB URLs, secrets, and API keys should be externalized.
14. **No logging** — No `logging` setup. Request/error logs are unavailable for debugging or monitoring.
15. **No global exception handlers** — No `@app.exception_handler` for standardized error responses across all endpoints.
16. **No startup/shutdown lifecycle** — No `@app.on_event("startup")` or lifespan context manager for initializing DB connections or cleanup.

### Testing & DevOps
17. **No tests** — No pytest tests, no test directory. The global `products` list makes testing especially tricky due to shared mutable state between tests.
18. **No `.gitignore`** — `__pycache__/`, `.venv/`, and `.env` should be excluded from version control.
19. **No CI/CD** — No GitHub Actions, Dockerfile, docker-compose, or Makefile. No automated testing or deployment pipeline.
20. **Python 3.14 requirement** — Python 3.14 is very cutting-edge and may not be available on all deployment platforms. Consider targeting 3.11+ for broader compatibility.
