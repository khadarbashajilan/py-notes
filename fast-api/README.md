# FastAPI Learning Journey — v1 to v4

A progressive roadmap from **beginner → intermediate** FastAPI developer. Each version builds on the previous, adding real-world patterns one step at a time.

---

## v1 — Foundation (Score: 4/10)

### What I Learned
- Setting up a FastAPI project with `uv`
- Defining a Pydantic `BaseModel`
- Storing data in a Python list (in-memory)
- Path parameters like `{id}`
- Basic route handlers — `GET`, `POST`, `PUT`, `DELETE`

### What I Implemented
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Welcome message |
| GET | `/all` | List all products |
| POST | `/add` | Create product (client supplies ID) |
| GET | `/product/{id}` | Get product by ID |
| PUT | `/update/{id}` | Replace product entirely |
| DELETE | `/delete/{id}` | Delete product by ID |

### Project Structure
```
v1/
├── main.py         # Routes + app instance
├── models.py       # Product BaseModel
├── pyproject.toml  # Dependencies
└── uv.lock
```

### Key Terminology
| Term | Meaning |
|------|---------|
| **FastAPI** | Python web framework for building APIs with automatic docs |
| **Pydantic** | Library that validates data using Python type hints |
| **BaseModel** | Pydantic class that auto-validates fields on creation |
| **In-memory** | Data stored in RAM — fast but lost when server restarts |
| **CRUD** | Create, Read, Update, Delete — the four basic data operations |
| **Path parameter** | Dynamic part of a URL, like `{id}` in `/product/{id}` |
| **uv** | Fast Python package manager (alternative to pip/poetry) |
| **ASGI** | Asynchronous Server Gateway Interface — the standard FastAPI runs on |

### Limitations
- No database — data lost on every restart
- Client supplies IDs (can cause duplicates)
- No validation — negative prices, empty names all accepted
- Wrong HTTP status codes (POST returns 200 instead of 201)
- Non-RESTful paths (`/add`, `/all`, `/delete/{id}`)
- No async, no tests, no CORS, no auth, no logging

---

## v2 — REST & Validation (Score: 6/10)

### What I Learned
- RESTful API design conventions
- Pydantic v2 `@field_validator` with `@classmethod`
- Server-side UUID generation
- Correct HTTP status codes (201, 404, 409, 422)
- Separating code into multiple files (layered architecture)
- Partial updates with optional fields
- Case-insensitive lookups and input sanitization

### What I Implemented
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/products` | Create product (auto-generates UUID) → 201 |
| GET | `/products` | List all products |
| GET | `/products/{name}` | Get product by name (case-insensitive) |
| PUT | `/products/{name}` | Partially update product |
| DELETE | `/products/{name}` | Delete product by name |

### Project Structure
```
v2/
├── main.py         # Route handlers only
├── db.py           # In-memory storage + business logic
├── model.py        # Pydantic schemas (Create, Update, Response)
├── pyproject.toml
└── uv.lock
```

### Key Terminology
| Term | Meaning |
|------|---------|
| **REST** | API design style using standard HTTP methods + meaningful URLs |
| **HTTP status codes** | Standard response codes: 200 (OK), 201 (Created), 404 (Not Found), 409 (Conflict), 422 (Validation Error) |
| **`@field_validator`** | Pydantic decorator that runs custom validation on a specific field |
| **`@classmethod`** | Python decorator — method receives the class (`cls`), not an instance (`self`) |
| **UUID** | Universally Unique Identifier — a random string like `"a1b2c3d4-..."` |
| **Layered architecture** | Splitting code into separate layers (routes → logic → models) |
| **Partial update** | Updating only the fields the client sends (others stay unchanged) |
| **Sanitization** | Cleaning user input — trimming whitespace, lowercasing, etc. |

### New Validations in `model.py`
- **`check_empty`** — rejects blank names and descriptions
- **`lowercase_name`** — converts names to lowercase automatically
- **`check_price`** — rejects zero/negative prices

### What Improved from v1
- RESTful paths instead of `/add`, `/all`
- Correct HTTP codes (201 for create, 404/409 for errors)
- Auto-generated UUIDs (no duplicate ID bugs)
- Input validation → automatic 422 responses
- Three separate files instead of two
- Case-insensitive product lookups
- Whitespace trimming everywhere
- Partial updates via `ProductUpdate` (all fields optional)

### Limitations
- Still in-memory — data lost on restart
- No async handlers
- No dependency injection
- No tests
- No CORS, no auth, no logging, no error handlers

---

## v3 — Database & Async (Score: 8/10)

### What I Learned
- SQLAlchemy ORM — defining tables, querying, inserting
- SQLite — file-based database (persists between restarts)
- `async def` handlers — FastAPI's intended pattern
- `Depends()` — FastAPI dependency injection
- Database sessions — create, commit, rollback, close
- SQLAlchemy models vs Pydantic schemas (separation of concerns)

### What I Implemented
- **`database.py`** — SQLAlchemy engine, `SessionLocal`, `Base`
- **SQLAlchemy `Product` model** — maps to `products` table
- **`get_db()` dependency** — provides a session per request
- **Async `db.py`** — all CRUD functions use `async/await`
- **Async route handlers** — all `def` → `async def`
- **File-based SQLite** — data persists in `products.db`
- **`.gitignore`** — excludes `__pycache__/`, `.venv/`, `*.db`

### Project Structure
```
v3/
├── main.py         # Async routes with Depends(get_db)
├── db.py           # Async CRUD functions with SQLAlchemy queries
├── model.py        # Pydantic schemas + SQLAlchemy ORM model
├── database.py     # Engine, SessionLocal, Base, get_db()
├── pyproject.toml
├── .gitignore
└── uv.lock
```

### Key Terminology
| Term | Meaning |
|------|---------|
| **ORM** | Object-Relational Mapping — lets you write Python classes instead of SQL |
| **SQLAlchemy** | Popular Python ORM for working with databases |
| **SQLite** | Lightweight file-based database (no server needed) |
| **Engine** | SQLAlchemy object that connects to the database |
| **Session** | SQLAlchemy object that holds a database transaction |
| **`Depends()`** | FastAPI function that injects dependencies into route handlers |
| **Dependency Injection** | Pattern where a function receives its dependencies (like DB session) rather than creating them |
| **Async / Await** | Python syntax for non-blocking code — handles many requests concurrently |

### Database Flow
```
Request → Route Handler → Depends(get_db) → SQLAlchemy Session → SQLite File
                              │
                         yields session
                              │
                        closes on return
```

### What Improved from v2
- Data persists across server restarts (SQLite file)
- Async handlers (proper FastAPI pattern)
- Dependency injection (`Depends(get_db)`)
- No global mutable state
- `.gitignore` for cleaner repos

### Limitations
- No tests
- No CORS
- No exception handlers
- No logging
- No environment config
- No Docker/CI

---

## v4 — Testing & Polish (Score: 9/10)

### What I Learned
- pytest — writing and running automated tests
- `TestClient` — FastAPI's test utility (uses httpx internally)
- Testing with dependency overrides
- CORS middleware — allowing frontend apps to call the API
- `@app.exception_handler` — custom global error responses
- Python `logging` module — structured logs for debugging
- `pydantic-settings` — environment configuration via `.env`
- `Dockerfile` — containerizing the app for deployment
- CI/CD basics — GitHub Actions for automated testing

### What I Implemented
- **`test_main.py`** — tests for all 5 CRUD endpoints
- **CORS middleware** — allows cross-origin requests
- **Global exception handlers** — standardized 404, 422, 500 JSON responses
- **Logging** — request logging with timestamps
- **`settings.py`** — configuration via `pydantic-settings` + `.env`
- **`Dockerfile` + `.dockerignore`** — container image
- **`.github/workflows/ci.yml`** — run tests on every push
- **`lifespan` context manager** — startup/shutdown events

### Project Structure
```
v4/
├── main.py            # Routes + CORS + exception handlers + lifespan + logging
├── db.py              # Async CRUD functions
├── model.py           # Pydantic schemas + SQLAlchemy ORM model
├── database.py        # Engine, SessionLocal, get_db()
├── settings.py        # pydantic-settings config class
├── test_main.py       # pytest tests for all endpoints
├── Dockerfile         # Container build instructions
├── .dockerignore      # Files to exclude from Docker image
├── .env.example       # Template for environment variables
├── .gitignore
├── pyproject.toml
└── uv.lock
```

### Key Terminology
| Term | Meaning |
|------|---------|
| **pytest** | Python testing framework — finds and runs test functions |
| **TestClient** | FastAPI's test helper — simulates HTTP requests without a server |
| **Dependency override** | Replacing a dependency (like `get_db`) during tests |
| **CORS** | Cross-Origin Resource Sharing — browser security mechanism |
| **Middleware** | Code that runs on every request before/after your route handler |
| **Exception handler** | Catches unhandled exceptions and returns a proper JSON response |
| **Lifespan** | FastAPI context manager for startup/shutdown code |
| **`pydantic-settings`** | Reads config from `.env` files and environment variables |
| **Docker** | Container platform — packages your app + dependencies together |
| **Container** | Lightweight, portable environment for running applications |
| **CI/CD** | Continuous Integration / Continuous Deployment — automated testing + deployment |
| **GitHub Actions** | GitHub's CI/CD service — runs workflows on push/PR |

### Test Example
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_product():
    response = client.post("/products", json={
        "name": "laptop", "price": 999, "description": "gaming laptop"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "laptop"
```

### What Improved from v3
- Full test coverage (confidence to refactor)
- CORS enabled (frontend can call the API)
- Beautiful error responses (not raw tracebacks)
- Structured logging (debug production issues)
- Environment config (no hardcoded secrets)
- Containerized (runs anywhere)
- Automated tests on push (CI)

---

## Version Comparison

| Feature | v1 | v2 | v3 | v4 |
|---------|:--:|:--:|:--:|:--:|
| RESTful routes | ✗ | ✓ | ✓ | ✓ |
| Input validation | ✗ | ✓ | ✓ | ✓ |
| Correct HTTP codes | ✗ | ✓ | ✓ | ✓ |
| Persistence (DB) | ✗ | ✗ | ✓ | ✓ |
| Async handlers | ✗ | ✗ | ✓ | ✓ |
| Dependency Injection | ✗ | ✗ | ✓ | ✓ |
| Tests | ✗ | ✗ | ✗ | ✓ |
| CORS | ✗ | ✗ | ✗ | ✓ |
| Error handlers | ✗ | ✗ | ✗ | ✓ |
| Logging | ✗ | ✗ | ✗ | ✓ |
| Environment config | ✗ | ✗ | ✗ | ✓ |
| Docker | ✗ | ✗ | ✗ | ✓ |
| CI | ✗ | ✗ | ✗ | ✓ |
| **Score** | **4/10** | **6/10** | **8/10** | **9/10** |

---

## Full Glossary

| Term | Definition |
|------|------------|
| **API** | Application Programming Interface — lets apps talk to each other |
| **ASGI** | Async Server Gateway Interface — the standard FastAPI runs on |
| **CRUD** | Create, Read, Update, Delete |
| **Pydantic** | Python library for data validation using type hints |
| **SQLAlchemy** | Python ORM for working with relational databases |
| **ORM** | Object-Relational Mapping — maps Python classes to database tables |
| **SQLite** | File-based relational database (no server required) |
| **Session** | A single database transaction/connection |
| **Dependency Injection** | Pattern where dependencies are passed in, not created internally |
| **`Depends()`** | FastAPI's built-in DI mechanism |
| **Async/Await** | Python syntax for concurrent, non-blocking code |
| **`@field_validator`** | Pydantic decorator that validates/c transforms a specific field |
| **`@classmethod`** | Method that receives the class (`cls`) instead of an instance (`self`) |
| **Middleware** | Code that processes every request/response in the pipeline |
| **CORS** | Security mechanism that controls which websites can call your API |
| **TestClient** | FastAPI's HTTP test simulator (uses httpx) |
| **pytest** | Popular Python testing framework |
| **pydantic-settings** | Reads config from `.env` files with validation |
| **Docker** | Platform for packaging apps into portable containers |
| **GitHub Actions** | CI/CD service that runs automated workflows |
| **Lifespan** | FastAPI's startup/shutdown event system |

---

## Architecture Evolution

```
v1:                   v2:                       v3:                        v4:
┌──────────┐          ┌──────────┐              ┌──────────┐               ┌──────────┐
│  main.py │          │  main.py │              │  main.py │               │  main.py │
│ (routes) │          │ (routes) │              │ (routes) │               │ (routes) │
│ (models) │          │          │              │   async  │               │   async  │
│ (logic)  │          ├──────────┤              │ Depends  │               │ CORS     │
└──────────┘          │  db.py   │              ├──────────┤               │ logging  │
                      │ (logic)  │              │  db.py   │               │ handlers │
                      ├──────────┤              │  async   │               ├──────────┤
                      │ model.py │              ├──────────┤               │  db.py   │
                      │ (schemas)│              │ model.py │               │  async   │
                      └──────────┘              │ (schemas)│               ├──────────┤
                                                │ (ORM)    │               │ model.py │
                                                ├──────────┤               │ (schemas)│
                                                │database  │               │ (ORM)    │
                                                │ .py      │               ├──────────┤
                                                └──────────┘               │database  │
                                                                           │ .py      │
                                                                           ├──────────┤
                                                                           │settings  │
                                                                           │ .py      │
                                                                           ├──────────┤
                                                                           │test_main │
                                                                           │ .py      │
                                                                           └──────────┘
```

---

## Final Thoughts

This journey took me from writing a single-file prototype (v1) to a fully tested, containerized, production-ready API (v4). Each version taught a core skill:

1. **v1** — Getting something working
2. **v2** — Writing clean, validated APIs
3. **v3** — Using databases and async properly
4. **v4** — Testing, hardening, and deploying

The next steps beyond v4 would be: authentication (JWT), background tasks, WebSockets, GraphQL, and cloud deployment (AWS/GCP/Azure).
