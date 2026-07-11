from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # App info
    PROJECT_NAME: str = "User Profile System"
    
    # Task 5: Avatar Upload Settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_BYTES: int = 1024 * 1024  # 1MB in bytes
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/webp"]

settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
