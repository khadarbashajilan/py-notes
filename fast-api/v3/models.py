from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Credential(Base):
    __tablename__ = "credentials"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_name : Mapped[str] = mapped_column(nullable=False)
    username : Mapped[str | None] = mapped_column(nullable=True)
    password : Mapped[str] = mapped_column(nullable=False)
    notes : Mapped[str | None] = mapped_column(nullable=True)




