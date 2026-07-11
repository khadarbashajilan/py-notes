from fastapi import Request, UploadFile, File, status, APIRouter
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_new_user, get_user_by_username
from app.services.file_service import upload_avatar

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate):
    return await create_new_user(user)

@router.post("/{username}/avatar", response_model=UserResponse)
async def avatar_update(username:str, request: Request, file:UploadFile=File(...)):
    return await upload_avatar(username, file, request)

@router.get("/user/{username}", response_model=UserResponse)
async def get_user(username:str):
    return await get_user_by_username(username)

