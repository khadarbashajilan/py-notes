from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import List
from database import init_db
from repository import get_all, get_credential, create_credential, partial_update, full_update
from model import AddCred, UpdateCred, CredResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database connected and tables ready")
    yield
    print("Shutting down app")


app = FastAPI(lifespan=lifespan)


@app.get("/credentials", response_model=List[CredResponse])
async def list_credentials():
    return await get_all()


@app.get("/credentials/{cred_id}", response_model=CredResponse)
async def retrieve_credential(cred_id: int):
    return await get_credential(cred_id)


@app.post("/credentials", response_model=CredResponse, status_code=201)
async def add_credential(payload: AddCred):
    return await create_credential(payload)


@app.patch("/credentials/{cred_id}", response_model=CredResponse)
async def patch_credential(cred_id: int, payload: UpdateCred):
    return await partial_update(cred_id, payload)


@app.put("/credentials/{cred_id}", response_model=CredResponse)
async def replace_credential(cred_id: int, payload: AddCred):
    return await full_update(cred_id, payload)
