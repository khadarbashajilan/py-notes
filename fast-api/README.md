# FastAPI Learning Journey — v1 to v6

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
| PUT | `/products/{name}` | Full replacement (all fields required) |
| PATCH | `/products/{name}` | Partial update (only changed fields) |
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
- Creating sessions inside each function (no dependency injection)
- `async with` context manager for safe session cleanup
- SQLAlchemy models vs Pydantic schemas (separation of concerns)
- Lifespan context manager for startup/shutdown events

### What I Implemented
- **`database.py`** — SQLAlchemy engine + `async_sessionmaker`
- **`init_db()`** — creates tables on startup via lifespan
- **SQLAlchemy `ProductORM` model** — maps to `products` table
- **Async `db.py`** — each function creates its own session with `async with AsyncSessionLocal() as session:`
- **Async route handlers** — all `def` → `async def`
- **File-based SQLite** — data persists in `products.db`
- **Lifespan** — `init_db()` runs on startup

### Project Structure
```
v3/
├── main.py         # Async routes + lifespan (no Depends)
├── db.py           # Async CRUD — each function creates its own session
├── model.py        # Pydantic schemas + SQLAlchemy ORM model
├── database.py     # Engine, AsyncSessionLocal, init_db()
├── pyproject.toml
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
| **Async / Await** | Python syntax for non-blocking code — handles many requests concurrently |
| **Context manager** | `async with` block that auto-closes resources when done |
| **Lifespan** | FastAPI context manager for startup/shutdown code |

### Database Flow (No DI)
```
Request → Route Handler → db.py function → opens its own session → SQLite File
                                               │
                                          does work
                                               │
                                          auto-closes with `async with`
```

### What Improved from v2
- Data persists across server restarts (SQLite file)
- Async handlers (proper FastAPI pattern)
- No global mutable state (each function gets a fresh session)
- Lifespan context manager for startup init

### Limitations
- No dependency injection — can't swap DB for testing easily
- No CORS
- No exception handlers
- No logging
- No environment config

---

## v4 — PostgreSQL + DI + Infra Polish (Score: 9/10)

### What I Learned
- PostgreSQL — production-grade database (replaces SQLite)
- `Depends(get_db)` — FastAPI dependency injection in action
- `get_db()` generator — yields a session per request, closes automatically
- CORS middleware — allowing frontend apps to call the API
- `@app.exception_handler` — custom global error responses
- Python `logging` module — structured logs for debugging
- `pydantic-settings` — environment configuration via `.env`
- `.gitignore` — excluding unnecessary files from version control
- Feeling the **difference** between no-DI (v3) and DI (v4)

### What I Implemented
- **PostgreSQL** — replaces SQLite with `postgresql+asyncpg://`
- **`get_db()` dependency** — session per request via `Depends()`
- **`Depends(get_db)` in routes** — session passed into `db.py` functions
- **CORS middleware** — allows cross-origin requests
- **Global exception handlers** — standardized 404, 500 JSON responses
- **Logging** — request logging with timestamps
- **`settings.py`** — configuration via `pydantic-settings` + `.env`
- **`.gitignore`** — excludes `__pycache__/`, `.venv/`, `.env`
- **Lifespan** — startup logging + `init_db()`

### Project Structure
```
v4/
├── main.py            # Routes + CORS + exception handlers + lifespan + logging
├── db.py              # Async CRUD — session passed as parameter (DI)
├── model.py           # Pydantic schemas + SQLAlchemy ORM model
├── database.py        # Engine, AsyncSessionLocal, get_db()
├── settings.py        # pydantic-settings config class
├── .env.example       # Template for environment variables
├── .gitignore
├── pyproject.toml
└── uv.lock
```

### Key Terminology
| Term | Meaning |
|------|---------|
| **PostgreSQL** | Advanced open-source relational database (production-grade) |
| **Asyncpg** | High-performance async driver for PostgreSQL |
| **`Depends()`** | FastAPI function that injects dependencies into route handlers |
| **Dependency Injection** | Pattern where a function receives its dependencies (like DB session) rather than creating them |
| **`get_db()`** | Generator function that yields a DB session and auto-closes it |
| **CORS** | Cross-Origin Resource Sharing — browser security mechanism |
| **Middleware** | Code that runs on every request before/after your route handler |
| **Exception handler** | Catches unhandled exceptions and returns a proper JSON response |
| **`pydantic-settings`** | Reads config from `.env` files and environment variables |

### Database Flow (With DI)
```
Request → Route Handler → Depends(get_db) → PostgreSQL
                              │
                         yields session
                              │
                        closes on return
```

### What Improved from v3
- Dependency injection — session is a parameter, not created inside each function
- PostgreSQL — production-grade database
- CORS enabled (frontend can call the API)
- Beautiful error responses (not raw tracebacks)
- Structured logging (debug production issues)
- Environment config (no hardcoded secrets)
- `.gitignore` for cleaner repos

---

## v5 — Auth with JWT + Alembic (Score: 7/10 — mid-level foundation)

### What I Learned
- Alembic — version control for database schema (migrations)
- Hashing passwords with `passlib` + `bcrypt`
- JWT (JSON Web Token) — creating and verifying tokens
- `python-jose` — JWT encoding/decoding library
- `Depends(get_current_user)` — protecting routes with auth
- Register / Login flow — email + password → JWT
- SQLAlchemy relationship between `User` and `Product`

### What I Implemented
- **Alembic setup** — `alembic init`, first migration for `users` table
- **`auth.py`** — register + login logic with password hashing
- **`jwt.py`** — `create_access_token()` and `verify_token()` utilities
- **`POST /auth/register`** — create user (email, password)
- **`POST /auth/login`** — verify credentials → return JWT
- **`get_current_user`** dependency — extracts user from JWT on protected routes
- **Protected product routes** — only authenticated users can create/update/delete
- **`UserORM` model** — `id`, `email`, `password_hash`, `created_at`
- **Relationship** — products optionally linked to a user

### Key Files Added
```
v5/
├── auth.py           # Register + login handlers
├── jwt.py            # JWT create/verify utilities
├── alembic/          # Migration directory
│   ├── env.py
│   └── versions/     # Auto-generated migration files
├── alembic.ini       # Alembic config
└── .env              # Added JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE
```

### Key Terminology
| Term | Meaning |
|------|---------|
| **Alembic** | Database migration tool — version control for your schema |
| **Migration** | A file describing schema changes (add table, add column) |
| **JWT** | JSON Web Token — signed token containing user claims |
| **`python-jose`** | Library for JWT creation and verification |
| **`passlib`** | Password hashing library |
| **`bcrypt`** | Strong password hashing algorithm |
| **Hash** | One-way transformation of a password (can't reverse it) |
| **`get_current_user`** | FastAPI dependency that validates JWT and returns user |
| **Access token** | Short-lived JWT sent with each request to authenticate |

### Auth Flow
```
Register → POST /auth/register → hash password → store user → return success
Login    → POST /auth/login    → verify hash → create JWT → return token
Request  → GET /products       → send JWT in header → verify → return data
```

### What Improved from v4
- Users can register and log in
- Routes are protected — only authenticated users can modify data
- Passwords are hashed, never stored in plain text
- Schema changes are version-controlled with Alembic

### Limitations
- Only email/password — no social login (Google, GitHub)
- No tests for auth routes
- No role-based permissions (admin vs user)
- No refresh tokens

---

## v6 — OAuth2 + Production Patterns (Score: 9/10 — solid mid-level)

### What I Learned
- OAuth2 flow — Login with Google/GitHub
- Third-party OAuth providers — redirect + callback pattern
- Pagination — `?limit=&offset=` query parameters
- Rate limiting — protecting the API from abuse
- Health check endpoint — required for deployment orchestration
- Background tasks — `BackgroundTasks` for non-blocking operations
- Redis caching — reducing database load for frequent queries
- `docker-compose` — running app + PostgreSQL + Redis together
- Testing with auth — pytest + TestClient with JWT override

### What I Implemented
- **OAuth2 with Google** — `GET /auth/google` redirect + callback
- **Pagination** — `GET /products?limit=10&offset=0` with metadata
- **Rate limiting** — `slowapi` or custom middleware (per-user limits)
- **`GET /health`** — returns DB + Redis status
- **Background task** — welcome email on registration
- **Redis caching** — cached product list with TTL invalidation
- **`docker-compose.yml`** — app + PostgreSQL + Redis services
- **Tests with auth** — `TestClient` + dependency override for `get_current_user`

### Project Structure
```
v6/
├── main.py             # Routes + middleware + lifespan
├── db.py               # Async CRUD with pagination
├── model.py            # Pydantic schemas + SQLAlchemy models
├── database.py         # Engine, get_db()
├── auth.py             # JWT + OAuth2 handlers
├── jwt.py              # Token utilities
├── oauth.py            # Google OAuth2 config + callback
├── cache.py            # Redis connection + caching helpers
├── tasks.py            # Background task functions
├── settings.py         # pydantic-settings
├── test_main.py        # Tests with authenticated client
├── alembic/            # Migrations
├── docker-compose.yml  # PostgreSQL + Redis + app
├── Dockerfile
├── .env.example
├── .gitignore
└── pyproject.toml
```

### Key Terminology
| Term | Meaning |
|------|---------|
| **OAuth2** | Protocol for delegated authorization — "Login with Google" |
| **Authorization code** | Temporary code from OAuth provider, exchanged for a token |
| **Redirect URI** | Where the OAuth provider sends the user after login |
| **Pagination** | Splitting results into pages with limit/offset or cursor |
| **Rate limiting** | Restricting how many requests a user can make in a time window |
| **`BackgroundTasks`** | FastAPI utility for running tasks after the response is sent |
| **Redis** | In-memory data store — used for caching and rate limiting |
| **TTL** | Time-To-Live — how long a cache entry stays valid |
| **Docker Compose** | Tool to run multi-container apps (app + DB + Redis) |
| **Health check** | Endpoint that reports if the service is healthy |

### Production Patterns
```
                                  ┌──────────────┐
                                  │   Client     │
                                  └──────┬───────┘
                                         │
                           ┌─────────────▼──────────────┐
                           │     Nginx / Reverse Proxy    │
                           │  (rate limiting, SSL, etc.)  │
                           └─────────────┬──────────────┘
                                         │
                    ┌────────────────────▼───────────────────┐
                    │          FastAPI Application            │
                    │  ┌──────────┐  ┌────────┐  ┌────────┐ │
                    │  │   Auth   │  │  Prod  │  │ Health │ │
                    │  │ (JWT+OAuth)│  │  CRUD  │  │   OK   │ │
                    │  └──────────┘  └────────┘  └────────┘ │
                    └────────┬──────────────┬────────────────┘
                             │              │
                    ┌────────▼──┐    ┌──────▼──────┐
                    │ PostgreSQL │    │    Redis    │
                    │ (persist)  │    │   (cache)   │
                    └───────────┘    └─────────────┘
```

### What Improved from v5
- Social login (Google/GitHub) — users don't need to create a new account
- Pagination — API won't crash with 10,000 products
- Rate limiting — API won't go down from abuse
- Health check — devops can monitor the service
- Background tasks — welcome emails, cleanup jobs
- Redis caching — frequently accessed data is instant
- Docker Compose — one command to start everything
- Tests with auth — confidence that protected routes work

### Limitations (next steps)
- No WebSockets for real-time features
- No GraphQL for flexible queries
- No CI/CD pipeline
- No cloud deployment (AWS/GCP/Azure)
- No monitoring / alerting

---

## Version Comparison

| Feature | v1 | v2 | v3 | v4 | v5 | v6 |
|---------|:--:|:--:|:--:|:--:|:--:|:--:|
| RESTful routes | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Input validation | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Correct HTTP codes | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Persistence (DB) | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Async handlers | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Dependency Injection | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| CORS | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| Error handlers | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| Logging | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| Environment config | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| `.gitignore` | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| Alembic migrations | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| JWT auth | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| OAuth2 (Google/GitHub) | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Pagination | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Rate limiting | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Health check | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Background tasks | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Redis caching | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Docker Compose | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Tests with auth | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| **Score** | **4/10** | **6/10** | **7/10** | **7/10** | **7/10** | **9/10** |

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
| **PostgreSQL** | Advanced open-source relational database (production-grade) |
| **Asyncpg** | High-performance async PostgreSQL driver for Python |
| **Session** | A single database transaction/connection |
| **Dependency Injection** | Pattern where dependencies are passed in, not created internally |
| **`Depends()`** | FastAPI's built-in DI mechanism |
| **Async/Await** | Python syntax for concurrent, non-blocking code |
| **`@field_validator`** | Pydantic decorator that validates/transforms a specific field |
| **`@classmethod`** | Method that receives the class (`cls`) instead of an instance (`self`) |
| **Middleware** | Code that processes every request/response in the pipeline |
| **CORS** | Security mechanism that controls which websites can call your API |
| **`pydantic-settings`** | Reads config from `.env` files with validation |
| **Lifespan** | FastAPI's startup/shutdown event system |
| **Context manager** | `async with` block that auto-closes resources |
| **Alembic** | Database migration tool — version control for your schema |
| **Migration** | A file describing schema changes (add table, add column, etc.) |
| **JWT** | JSON Web Token — signed token containing user identity claims |
| **`python-jose`** | Library for JWT creation and verification |
| **`passlib`** | Password hashing library |
| **`bcrypt`** | Strong password hashing algorithm |
| **Hash** | One-way transformation of a password (can't reverse it) |
| **`get_current_user`** | FastAPI dependency that validates JWT and returns the user |
| **Access token** | Short-lived JWT sent with each request to authenticate |
| **OAuth2** | Protocol for delegated authorization — "Login with Google" |
| **Authorization code** | Temporary code from OAuth provider, exchanged for a real token |
| **Redirect URI** | Where the OAuth provider sends the user after successful login |
| **Pagination** | Splitting results into pages with limit/offset |
| **Rate limiting** | Restricting requests per user within a time window |
| **`BackgroundTasks`** | FastAPI utility for running tasks after the response is sent |
| **Redis** | In-memory data store — used for caching and rate limiting |
| **TTL** | Time-To-Live — how long a cache entry stays valid |
| **Docker Compose** | Tool to run multi-container apps together (app + DB + Redis) |
| **Health check** | Endpoint that reports if the service is healthy and ready |

---

## Architecture Evolution

```
v1:              v2:               v3:               v4:                v5:                    v6:
┌──────────┐    ┌──────────┐      ┌──────────┐      ┌──────────┐       ┌───────────┐          ┌──────────────┐
│  main.py │    │  main.py │      │  main.py │      │  main.py │       │  main.py  │          │   main.py    │
│ (routes) │    │ (routes) │      │ (routes) │      │ (routes) │       │  (routes) │          │   (routes)   │
│ (models) │    │          │      │   async  │      │   async  │       │   async   │          │    async     │
│ (logic)  │    ├──────────┤      │ lifespan │      │ CORS     │       │  CORS     │          │   CORS       │
└──────────┘    │  db.py   │      ├──────────┤      │ logging  │       │  logging  │          │   logging    │
                │ (logic)  │      │  db.py   │      │ handlers │       │  handlers │          │   handlers   │
                ├──────────┤      │  async   │      │ Depends  │       │  Depends  │          │   Depends    │
                │ model.py │      │  no DI   │      ├──────────┤       │  JWT auth │          │   JWT+OAuth  │
                │ (schemas)│      ├──────────┤      │  db.py   │       ├───────────┤          │   pagination │
                └──────────┘      │ model.py │      │  async   │       │  db.py    │          │   rate limit │
                                  │ (schemas)│      │  with DI │       │  auth.py  │          │   health     │
                                  │ (ORM)    │      ├──────────┤       │  jwt.py   │          │   bg tasks   │
                                  ├──────────┤      │ model.py │       ├───────────┤          ├──────────────┤
                                  │database  │      │ (schemas)│       │ model.py  │          │  db.py       │
                                  │ .py      │      │ (ORM)    │       │ (schemas) │          │  auth.py     │
                                  └──────────┘      ├──────────┤       │ (ORM)     │          │  jwt.py      │
                                                     │database  │       ├───────────┤          │  oauth.py    │
                                                     │ .py      │       │database   │          │  cache.py    │
                                                     │ (get_db) │       │ .py       │          │  tasks.py    │
                                                     ├──────────┤       ├───────────┤          ├──────────────┤
                                                     │settings  │       │ alembic/  │          │ model.py     │
                                                     │ .py      │       │ .env      │          │ database.py  │
                                                     └──────────┘       └───────────┘          │ alembic/     │
                                                                                               │ settings.py  │
                                                                                               │ test_main.py │
                                                                                               │ docker-      │
                                                                                               │ compose.yml  │
                                                                                               └──────────────┘
```

---

## Final Thoughts

This journey took me from writing a single-file prototype (v1) to a fully-featured, production-ready API with OAuth2, caching, and Docker Compose (v6). Each version taught a core skill:

1. **v1** — Getting something working
2. **v2** — Writing clean, validated REST APIs
3. **v3** — Using databases and async properly (no DI)
4. **v4** — Learning dependency injection, PostgreSQL, and infra polish
5. **v5** — Authentication with JWT and schema migrations with Alembic
6. **v6** — OAuth2, pagination, rate limiting, caching, and production patterns

The key insight from this progression is that each version adds exactly one or two new concepts — never overwhelming, always building on what came before.

### Career Level by Version

| Version | Level | Can do |
|---------|-------|--------|
| v1–v2 | Beginner | Build a basic CRUD API |
| v3–v4 | Beginner → Junior | Build a persistent API with async, DI, PostgreSQL |
| v5 | Junior → Mid | Add auth, migrations, user management |
| v6 | Mid-level | Build a production-ready API with OAuth, caching, rate limiting |

The next steps beyond v6 would be: WebSockets (real-time), GraphQL, microservices, Kubernetes, and cloud deployment (AWS/GCP/Azure).
