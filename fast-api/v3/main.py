from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routes import router


# lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # create all tables if not exists
    await init_db()
    print("Database connected and tables ready")

    yield

    print("Shutting down app")


# create backend server
app = FastAPI(lifespan=lifespan)

app.include_router(router)
