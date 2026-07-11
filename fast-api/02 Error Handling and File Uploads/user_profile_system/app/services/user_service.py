from app.schemas.user import UserCreate, UserResponse
from app.core.exceptions import UserNotFoundException, DuplicateUsernameException

# In-memory store for demo purposes. Replace with a real DB in production.
_users: dict[str, dict] = {}


def _to_response(user: dict) -> UserResponse:
    return UserResponse(
        username=user["username"],
        email=user["email"],
        avatar_url=user.get("avatar_url"),
    )


async def create_new_user(user: UserCreate) -> UserResponse:
    if user.username in _users:
        raise DuplicateUsernameException()
    _users[user.username] = {
        "username": user.username,
        "email": user.email,
        "password": user.password,  # demo only: never store plaintext in real apps
        "avatar_url": None,
    }
    return _to_response(_users[user.username])


async def get_user_by_username(username: str) -> UserResponse:
    user = _users.get(username)
    if not user:
        raise UserNotFoundException()
    return _to_response(user)


async def update_avatar(username: str, avatar_url: str) -> UserResponse:
    user = _users.get(username)
    if not user:
        raise UserNotFoundException()
    user["avatar_url"] = avatar_url
    return _to_response(user)
