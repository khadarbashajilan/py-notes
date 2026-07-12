"""
Dependency Injection Levels
This module explores different levels of dependency injection in FastAPI, including router-level dependencies and shared logic.
"""

from fastapi import APIRouter, FastAPI, Depends, HTTPException, Header

app = FastAPI()


async def verify_admin(X_Admin_Key:str = Header(default=None)):
    if X_Admin_Key != "super-secret":
        raise HTTPException(status_code=403, detail='Admin access required')


admin_router = APIRouter(dependencies=[Depends(verify_admin)], prefix="/admin")

@admin_router.get("/status")
def get_status():
    return {"message" : "Success"}

@admin_router.delete("/users/{user_id}")
def delete_user(user_id:int):
    return {"message" : "Deleted"}

app.include_router(admin_router)


#explain all 3 dependency levels.. and switching dependency with real and fake... while testing... 
