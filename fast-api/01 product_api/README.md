# Product Management API

A simple REST API built with **FastAPI** for managing products in an in-memory store.
Designed as a learning project to demonstrate CRUD operations, layered architecture, and Pydantic validation.

## Tech Stack

- **FastAPI** (modern, high-performance web framework)
- **Pydantic** v2 (data validation)
- **Uvicorn** (ASGI server)
- Python 3.12+

## Setup & Run

```bash
# Clone the repo
cd "fast-api/01 product_api"

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install fastapi[standard]

# Start the server
fastapi dev main.py
# or: uvicorn main:app --reload
```

Visit **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

## API Endpoints

| Method | Endpoint           | Description              | Status Code |
|--------|--------------------|--------------------------|-------------|
| GET    | `/`                | Welcome message          | 200         |
| GET    | `/products`        | List all products        | 200         |
| GET    | `/products/{id}`   | Get product by ID        | 200         |
| POST   | `/products`        | Create a new product     | 201         |
| PUT    | `/products/{id}`   | Full update of product   | 200         |
| PATCH  | `/products/{id}`   | Partial update of product| 200         |
| DELETE | `/products/{id}`   | Delete a product         | 204         |

### Query Parameters (`GET /products`)

| Parameter   | Type   | Description                    |
|-------------|--------|--------------------------------|
| `category`  | string | Filter by category (case-insensitive) |
| `min_price` | float  | Filter by minimum price        |

## Request Examples

### Create a Product

```json
POST /products
{
  "name": "Laptop",
  "price": 999.99,
  "category": "Electronics"
}
```

### Partial Update

```json
PATCH /products/1
{
  "price": 899.99
}
```

## Project Structure

```
01 product_api/
├── app/
│   ├── api/routers/
│   │   └── products.py    # Route definitions
│   ├── db/
│   │   └── memory.py      # In-memory data store
│   ├── models/
│   │   └── product.py     # Pydantic schemas
│   └── services/
│       └── product_service.py  # Business logic
├── main.py                # FastAPI app entry point
├── pyproject.toml
└── README.md
```

## Features

- Full CRUD (Create, Read, Update, Delete)
- Partial updates via PATCH
- Category & price filtering
- Pydantic validation with auto-capitalization
- Interactive API docs at `/docs`
- Clean layered architecture
