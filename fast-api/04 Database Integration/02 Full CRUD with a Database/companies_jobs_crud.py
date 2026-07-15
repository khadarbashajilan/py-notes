# --- Imports ---
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Relationship, create_engine, SQLModel, Field, Session, select

# --- Database Configuration ---
sqlite_url = "sqlite:///./database.db"
# Create SQLite engine with echo enabled for SQL logging
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

# --- SQLModel ORM Models (Database Tables) ---

# Company table: stores company details with a one-to-many relationship to JobListing
class Company(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    industry: str
    jobs: List["JobListing"] = Relationship(back_populates="company_", cascade_delete=True)

# JobListing table: stores job posts linked to a company via foreign key
class JobListing(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    salary: int
    is_active: bool = Field(default=True)
    company_id: int = Field(foreign_key="company.id")
    company_: Optional[Company] = Relationship(back_populates="jobs")

# --- Request / Response Models ---

# Request model for creating a new job
class CreateJob(SQLModel):
    company_id: int
    title: str
    description: str
    salary: int
    is_active: bool

# Request model for partial job update (all fields optional)
class UpdateJob(SQLModel):
    company_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[int] = None
    is_active: Optional[bool] = None

# Response model for a single job (includes generated id)
class GetJob(SQLModel):
    id: int
    title: str
    salary: int
    description: str
    company_id: int

# Request model for creating a new company
class CreateCompany(SQLModel):
    name: str
    industry: str

# Response model for a company (includes auto-generated id and nested jobs)
class GetCompany(CreateCompany):
    id: int
    jobs: List[GetJob]


# --- Startup: Create Database Tables ---
def create_db_and_tables():
    """Create all database tables defined by SQLModel metadata."""
    SQLModel.metadata.create_all(engine)

# Run table creation on module import / app startup
create_db_and_tables()


# --- Dependency: Database Session ---
def get_db():
    """Yield a new SQLModel database session per request."""
    with Session(engine) as session:
        yield session


# --- FastAPI Application ---
app = FastAPI()


# --- API Endpoints ---

@app.post("/companies")
def create_company(company: CreateCompany, session: Session = Depends(get_db)):
    """Create a new company and return it with its generated id."""
    cmp = Company(name=company.name, industry=company.industry)
    session.add(cmp)
    session.commit()
    session.refresh(cmp)  # Load auto-generated id
    return cmp


@app.get("/companies", response_model=List[GetCompany])
def get_companies(session: Session = Depends(get_db)):
    """Retrieve all companies with their nested job listings."""
    st = select(Company)
    cmps = session.exec(st).all()
    return cmps


@app.post("/jobs")
def create_job(job: CreateJob, session: Session = Depends(get_db)):
    """Create a new job listing linked to a company."""
    jb = JobListing(
        title=job.title,
        description=job.description,
        company_id=job.company_id,
        salary=job.salary,
        is_active=job.is_active,
    )
    session.add(jb)
    session.commit()
    session.refresh(jb)
    return jb


@app.get("/jobs", response_model=List[GetJob])
def get_jobs(session: Session = Depends(get_db)):
    """Retrieve all job listings."""
    st = select(JobListing)
    jbs = session.exec(st).all()
    return jbs


@app.put("/jobs/{id}")
def update_job(id: int, update_job: UpdateJob, session: Session = Depends(get_db)):
    """Update an existing job listing. Returns 404 if not found."""
    job = session.get(JobListing, id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {id} not found")

    # Apply only the fields that were explicitly provided
    update_data = update_job.model_dump(exclude_none=True)
    for k, v in update_data.items():
        setattr(job, k, v)

    session.add(job)
    session.commit()
    session.refresh(job)
    return job


@app.delete("/jobs/{id}")
def delete_job(id: int, session: Session = Depends(get_db)):
    """Delete a job listing by id. Returns 404 if not found."""
    job = session.get(JobListing, id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {id} not found")

    session.delete(job)
    session.commit()
    return None


