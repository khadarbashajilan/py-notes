import os
import uuid
import filetype

from app.core.config import settings
from app.core.exceptions import InvalidFileTypeException
from app.services.user_service import get_user_by_username, update_avatar
from app.schemas.user import UserResponse


def _validate(content: bytes) -> None:
    kind = filetype.guess(content)
    if kind is None or kind.mime not in settings.ALLOWED_IMAGE_TYPES:
        raise InvalidFileTypeException(
            message="Unsupported file type. Allowed types are: JPEG, PNG, WEBP."
        )


async def upload_avatar(username: str, file, request) -> UserResponse:
    await get_user_by_username(username)  # raises UserNotFoundException if missing

    contents = await file.read()
    _validate(contents)

    if len(contents) > settings.MAX_FILE_SIZE_BYTES:
        raise InvalidFileTypeException(
            message="File is too large. Maximum allowed size is 1 MB.",
            error_code="FILE_TOO_LARGE",
        )

    ext = filetype.guess(contents).extension or ""
    filename = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex
    path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(contents)

    base = str(request.base_url).rstrip("/")
    avatar_url = f"{base}/uploads/{filename}"
    return await update_avatar(username, avatar_url)
