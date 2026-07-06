"""
Custom Exception Classes for FastAPI Error Handling
Defines a hierarchy of application-specific exceptions with standardised
status codes, error codes, and optional detail payloads.
"""

from typing import Any, Optional


# ==========================================
# 1. Base Exception
# ==========================================

class AppException(Exception):
    """
    Base class for all application-level exceptions.
    Carries an HTTP status_code, a machine-readable error_code,
    a human-readable message, and optional details.
    """

    def __init__(self, status_code: int, error_code: str, message: str, details: Optional[Any] = None):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        # Initialise the base Exception so str(exc) returns the message
        super().__init__(message)


# ==========================================
# 2. Concrete Exceptions
# ==========================================

class NotFoundException(AppException):
    """
    Raised when a requested resource does not exist.
    Maps to HTTP 404 by default.
    """

    def __init__(self, message: str = "Resource not found", error_code: str = "NOT_FOUND", details: Optional[Any] = None):
        # Defaults provided so call sites can raise with just a message
        super().__init__(status_code=404, message=message, error_code=error_code, details=details)


class ConflictException(AppException):
    """
    Raised when an operation conflicts with the current state.
    Maps to HTTP 409 by default.
    """

    def __init__(self, message: str = "Resource conflict", error_code: str = "CONFLICT", details: Optional[Any] = None):
        super().__init__(status_code=409, error_code=error_code, message=message, details=details)


class ValidationException(AppException):
    """
    Raised when input data fails validation.
    Maps to HTTP 400 by default.
    """

    def __init__(self, message: str = "Validation failed", error_code: str = "VALIDATION_ERROR", details: Optional[Any] = None):
        super().__init__(status_code=400, error_code=error_code, message=message, details=details)
