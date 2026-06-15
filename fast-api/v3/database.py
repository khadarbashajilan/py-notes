from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.orm import declarative_base

#db url
DATABASE_URL = "sqlite+aiosqlite:///./passwords.db"

engine = create_async_engine(
    DATABASE_URL,
    # 'check_same_thread': False is specific to SQLite.
    # It allows multiple asynchronous tasks/threads to safely interact with the same SQLite connection.
    connect_args={"check_same_thread": False}
)

#creates DB session
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

#common base class for db tables
Base = declarative_base()

#created tables in startup
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#session dependency -> to manage db session lifecycle
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


