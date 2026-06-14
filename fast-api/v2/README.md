# FastAPI v2 — Product CRUD API (by Name)

## Rating: 6/10

A refactored product management API using in-memory storage with improved validation, proper error handling, and RESTful routing. A solid step forward from v1 but still lacks persistence and testing.

---

## ✅ What's Good

1. **Layered architecture** — `model.py` (schemas) → `db.py` (storage) → `main.py` (routes). Better separation than v1.
2. **Pydantic field validators** — `@field_validator` catches empty names, empty descriptions, negative/zero prices automatically → 422.
3. **Server-side ID generation** — UUIDs are auto-generated, avoiding the v1 bug where clients could supply duplicate IDs.
4. **RESTful endpoints** — `POST/GET /products`, `GET/PUT/PATCH/DELETE /products/{name}` follow REST conventions (not `/add`, `/all`, `/delete/{id}`).
5. **Correct HTTP status codes** — 201 for creation, 404 for not found, 409 for duplicate conflict, 422 for validation errors.
6. **Case-insensitive lookups** — Names are lowercased at validation + lookup, so `"Laptop"`, `"laptop"`, `"LAPTOP"` all work.
7. **Whitespace trimming** — `.strip()` applied at both validation and lookup layers.
8. **Partial updates** — `PATCH /products/{name}` uses `ProductUpdate` with all-Optional fields so clients send only what they want to change. `PUT` does full replacement with `ProductCreate`.
9. **Proper error messages** — Clear, consistent `detail` strings in all `HTTPException` responses.
10. **Type annotations everywhere** — All functions and route handlers have return types, improving IDE support.

---

## ❌ What Can Be Improved

### Storage & Persistence
1. **No database** — Data lives in a Python list and is wiped on every server restart. Add SQLite/PostgreSQL with SQLAlchemy.
2. **No persistence** — Even file-based storage (json, shelve) would be better than a volatile list.

### Code Quality & Correctness
3. **No async handlers** — All routes use `def` instead of `async def`. Fine for this scale but not best practice.
4. **No service/repository layer** — `db.py` doubles as storage + business logic. A proper repository pattern would improve testability.
5. **No dependency injection** — No use of FastAPI's `Depends()`. The global `products` list makes testing harder.
6. **Name-in-URL design** — Using names (not IDs) in URL paths means special characters (slashes, spaces) in product names can cause issues. Consider adding a `GET /products?name=xxx` query param alternative.

### Infrastructure & Configuration
7. **No CORS middleware** — Browsers from different origins cannot call this API.
8. **No authentication** — The API is completely open with no auth.
9. **No environment configuration** — No `.env`, no `pydantic-settings`.
10. **No logging** — No `logging` setup for debugging or monitoring.
11. **No global exception handlers** — No `@app.exception_handler` for standardized error responses.
12. **No startup/shutdown lifecycle** — No lifespan context manager.

### Testing & DevOps
13. **No tests** — Zero automated tests. The global `products` list makes isolation difficult.
14. **No `.gitignore`** — `__pycache__/`, `.venv/` should be excluded.
15. **No CI/CD** — No GitHub Actions, Dockerfile, or deployment pipeline.
16. **Python 3.14 requirement** — Cutting-edge; consider 3.11+ for broader compatibility.
