"""
FastAPI Error Handling Practice
This module demonstrates how to properly handle errors in FastAPI, including 
custom exceptions, overriding validation errors, and global catch-all handlers.
"""

import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

# ==========================================
# 1. Setup & Data Models
# ==========================================

app = FastAPI(
    title="User Management API",
    description="An API to demonstrate robust error handling in FastAPI."
)

# Pydantic model for incoming user data
class UserCreate(BaseModel):
    """Model representing the data required to create a new user."""
    username: str
    age: int

# Our fake in-memory database
fake_users_db = {
    "alice": {"username": "alice", "age": 28}
}

# ==========================================
# 2. Custom Exception & Handler
# ==========================================

class UserAlreadyExistsError(Exception):
    """
    Custom exception raised when attempting to create a user 
    that already exists in the database.
    """
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User {username} already exists")

@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
    """
    Handles the UserAlreadyExistsError by returning a 409 Conflict response.
    """
    return JSONResponse(
        status_code=409,
        content={
            "error": "CONFLICT",
            "message": f"User {exc.username} already exists"
        },
    )

# ==========================================
# 3. Overriding Pydantic Validation (422)
# ==========================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Overrides FastAPI's default 422 validation error.
    Extracts just the missing/invalid field names to return a clean, 
    frontend-friendly JSON response.
    """
    missing_fields = []
    for error in exc.errors():
        # error["loc"] is a tuple like ('body', 'age'). We want the last element ('age').
        field_name = error["loc"][-1]
        if field_name not in missing_fields:
            missing_fields.append(field_name)

    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_FAILED",
            "missing_fields": missing_fields
        },
    )

# ==========================================
# 4. Global Catch-All Handler (500)
# ==========================================

# Configure logging to output to the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    A safety net that catches ALL unhandled exceptions.
    It logs the full stack trace for developers but returns a 
    sanitized 500 error to the client to prevent information leakage.
    """
    # Log the detailed error on the server
    logger.exception(f"Unhandled exception occurred on {request.url}: {exc}")

    # Return a safe, generic message to the client
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_ERROR",
            "message": "Something went wrong on our end."
        },
    )

# ==========================================
# 5. Database Helper Functions
# ==========================================

def get_user_db(username: str) -> dict:
    """
    Fetches a user from the fake database.
    Raises an HTTPException with custom headers if the user is not found.
    """
    username = username.lower()
    if username not in fake_users_db.keys():
        raise HTTPException(
            status_code=404,
            detail=f"User {username} not found",
            headers={"X-Error-Code": "USR_404"} # Custom header for the frontend
        )
    return fake_users_db[username]

def add_user_db(details: UserCreate) -> dict:
    """
    Adds a new user to the fake database.
    Raises a custom UserAlreadyExistsError if the username is taken.
    """
    username = details.username.lower()
    if username in fake_users_db.keys():
        raise UserAlreadyExistsError(username)
    
    # Convert Pydantic model to a standard dictionary to store in our "DB"
    user_data = details.model_dump()
    fake_users_db[username] = user_data
    return user_data

def crash_intentionally() -> float:
    """A dummy function that intentionally causes a ZeroDivisionError."""
    x = 1 / 0
    return x

# ==========================================
# 6. API Routes (Endpoints)
# ==========================================

@app.get("/users/{username}", tags=["Users"])
async def get_user(username: str):
    """
    GET endpoint to retrieve a user by their username.
    """
    user_data = get_user_db(username)
    return {"status": "success", "user": user_data}

@app.post("/users/", tags=["Users"])
async def create_user(details: UserCreate):
    """
    POST endpoint to create a new user.
    Validates input via Pydantic, checks for duplicates via custom exception.
    """
    user_data = add_user_db(details)
    return {"status": "created", "user": user_data}

@app.get("/crash", tags=["Testing"])
async def crash_server():
    """
    A dummy endpoint to test the global 500 exception handler.
    """
    result = crash_intentionally()
    return {"result": result}

