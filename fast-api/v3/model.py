from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Credential(Base):
    __tablename__ = "credentials"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str | None] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str | None] = mapped_column(nullable=True)


class AddCred(BaseModel):
    service_name: str
    username: str | None = None
    password: str
    notes: str | None = None

    @field_validator("service_name", "password")
    @classmethod
    def check_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Field cannot be Empty")
        return v.strip()


class UpdateCred(BaseModel):
    service_name: str | None = None
    username: str | None = None
    password: str | None = None
    notes: str | None = None

    @field_validator("service_name", "password")
    @classmethod
    def check_empty(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("Field cannot be Empty")
        return v.strip() if v else v


class CredResponse(BaseModel):
    id: int
    service_name: str
    username: str | None = None
    password: str
    notes: str | None = None
