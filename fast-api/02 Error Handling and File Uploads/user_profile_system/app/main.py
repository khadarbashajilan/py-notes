from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.middleware import logs_
from app.core.exceptions import AppException, app_exception_handler
from app.core.config import settings
from app.api.routes import users  

app = FastAPI(title="User Profile API")

app.add_middleware(BaseHTTPMiddleware, dispatch=logs_)

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(users.router)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads") 


@app.get("/")
def root():
    return {"message": "API is running!"}
