"""
FastAPI Error Handling — Main Application
Demonstrates custom exception handlers, structured error responses,
and routes that raise application-specific exceptions.
"""

import logging
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from exceptions import AppException, ConflictException, NotFoundException, ValidationException

app = FastAPI(
    title="User Management API",
    description="Hands-on practice with FastAPI error handling patterns.",
)

# Configure logging to output to the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==========================================
# 1. Pydantic Models
# ==========================================

class User(BaseModel):
    """
    Model representing a user in our system.
    The id field is optional because it is auto-assigned on creation.
    """
    id: Optional[int] = None
    email: str
    age: int


# ==========================================
# 2. In-Memory Database
# ==========================================

# A simple dictionary acting as our fake persistent storage
users_db = {1: {"id": 1, "email": "test@test.com", "age": 25}}


# ==========================================
# 3. Exception Handlers
# ==========================================

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """
    Handles all custom AppException subclasses.
    Logs the error with the client's IP and request path,
    then returns a structured JSON error response.
    """
    client_ip = request.client.host if request.client else "unknown"

    # Log server errors (5xx) at ERROR level, client errors at DEBUG level
    if exc.status_code >= 500:
        logger.error(f"[{client_ip}] Server Error [{exc.error_code}] : {exc.message} | Path : {request.url.path}")
    else:
        logger.debug(f"[{client_ip}] Client Error [{exc.error_code}] : {exc.message} | Path : {request.url.path}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "status_code": exc.status_code,
            "details": exc.details,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Global catch-all for any unhandled exceptions.
    Logs the full stack trace on the server but returns a sanitised
    500 response to the client, preventing information leakage.
    """
    logger.exception(f"Unhandled Exception on {request.url.path}")

    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Our team has been notified.",
            "status_code": 500,
            "details": None,
        },
    )


# ==========================================
# 4. API Routes (Endpoints)
# ==========================================

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """
    GET /users/{user_id}
    Retrieves a user by their ID. Raises a NotFoundException
    if the user does not exist in the database.
    """
    if user_id not in users_db:
        raise NotFoundException(
            message=f"User with ID {user_id} not found",
            error_code="USER_NOT_FOUND",
        )
    # Convert the stored dict back to a User model for a consistent response shape
    return User(**users_db[user_id])


@app.post('/users', response_model=User)
async def create_user(user: User):
    """
    POST /users
    Creates a new user. Checks for duplicate emails and raises
    a ConflictException if a user with the same email already exists.
    """
    for existing_user in users_db.values():
        if existing_user["email"] == user.email:
            raise ConflictException(
                error_code='USER_EXISTS',
                message='User Already Exists',
                details={"duplicate_email": user.email},
            )

    # Auto-increment the ID based on existing keys
    new_id = max(users_db.keys(), default=0) + 1
    user_dict = user.model_dump()
    user_dict["id"] = new_id
    users_db[new_id] = user_dict
    return User(**user_dict)


@app.put("/users/{user_id}/age")
async def update_age(user_id: int, age: int):
    """
    PUT /users/{user_id}/age
    Updates the age of an existing user. Raises ValidationException
    if the provided age is under 18.
    """
    if user_id not in users_db:
        raise NotFoundException(message="User not found")

    if age < 18:
        raise ValidationException(
            message="User must be 18 or older",
            error_code="AGE_RESTRICTION",
            details={"provided_age": age},
        )

    users_db[user_id]["age"] = age
    return {"message": "Age updated", "user": users_db[user_id]}


@app.get('/crash')
async def crash_server():
    """
    GET /crash
    A dummy endpoint that triggers a ZeroDivisionError,
    allowing us to test the global 500 exception handler.
    """
    x = 1 / 0  # This will raise ZeroDivisionError
    return {"message": "This will never print"}
