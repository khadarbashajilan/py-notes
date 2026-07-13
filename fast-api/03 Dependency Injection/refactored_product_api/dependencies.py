from fastapi import Header, HTTPException

def get_pagination(skip: int = 0, limit: int = 10) -> tuple[int, int]:
    return (skip, limit)

def verify_token(x_token: str = Header()):
    if x_token != 'super-admin':
        raise HTTPException(status_code=401, detail="Invalid x_token")
