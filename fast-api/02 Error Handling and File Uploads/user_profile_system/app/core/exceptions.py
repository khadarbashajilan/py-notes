from fastapi.responses import JSONResponse
from fastapi import Request


class AppException(Exception):
    def __init__(self,status_code:int, error_code:str, message:str):
        self.status_code=status_code
        self.error_code=error_code
        self.message=message

        super().__init__(message)


class UserNotFoundException(AppException):
    def __init__(self, message:str="User Not Found", error_code:str="NOT_FOUND"):
        super().__init__(status_code=404,error_code=error_code,message=message)

class DuplicateUsernameException(AppException):
    def __init__(self, message:str="User Already Exists", error_code:str="ALREADY_EXISTS"):
        super().__init__(status_code=409,error_code=error_code,message=message)

class InvalidFileTypeException (AppException):
    def __init__(self,message:str="Unsupported file type. Allowed types are: JPEG, PNG, WEBP.", error_code:str="INVALID_FILETYPE"):
        super().__init__(status_code=406, error_code=error_code,message=message)

async def app_exception_handler(request: Request, exc: AppException):
    """
    Catches any exception that inherits from AppException and formats it into a consistent JSON response.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "error_code": exc.error_code,
            "message": exc.message,
            "path": request.url.path  # Helpful for debugging
        }
    )
