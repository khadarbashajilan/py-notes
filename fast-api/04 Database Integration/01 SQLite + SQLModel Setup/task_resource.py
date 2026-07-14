# --- Imports ---
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select

# --- Database Configuration ---
sqlite_url = "sqlite:///./todo.db"
# Create SQLite engine with echo enabled for SQL logging
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

# --- SQLModel ORM Models ---

# Database table model (maps directly to the "table" table in SQLite)
class Table(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    completed: bool = False

# Request model for creating a new task (no id field — auto-generated)
class CreateTask(SQLModel):
    title: str
    description: str | None = None
    completed: bool = False

# Response model that includes the generated id
class TaskResponse(SQLModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False


# --- Startup ---
def create_db_and_tables():
    """Create all database tables defined by SQLModel metadata."""
    SQLModel.metadata.create_all(engine)

# Run table creation on module import / app startup
create_db_and_tables()


# --- Dependency: Database Session ---
def get_session():
    """Yield a new SQLModel database session per request."""
    with Session(engine) as session:
        yield session


# --- FastAPI Application ---
app = FastAPI()


# --- API Endpoints ---

@app.post("/tasks", response_model=TaskResponse)
def add_post(task: CreateTask, session: Session = Depends(get_session)):
    """Create a new task and return it with its generated id."""
    db_task = Table(title=task.title, description=task.description, completed=task.completed)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)  # Load auto-generated id and defaults
    return db_task


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, session: Session = Depends(get_session)):
    """Retrieve a single task by its id. Returns 404 if not found."""
    t = session.get(Table, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task Not Found")
    return t


@app.get("/tasks", response_model=List[TaskResponse])
def get_all(session: Session = Depends(get_session)):
    """Retrieve all tasks."""
    st = select(Table)
    t = session.exec(st)
    t = t.all()
    return t






