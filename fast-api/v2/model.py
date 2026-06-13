from pydantic import BaseModel, field_validator


class ProductCreate(BaseModel):
    name: str
    price: int
    description: str

    @field_validator("name", "description")
    @classmethod
    def check_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v.strip()

    @field_validator("name")
    @classmethod
    def lowercase_name(cls, v):
        return v.lower()

    @field_validator("price")
    @classmethod
    def check_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than zero")
        return v


class ProductUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    description: str | None = None

    @field_validator("name", "description")
    @classmethod
    def check_empty(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v.strip() if v else v

    @field_validator("name")
    @classmethod
    def lowercase_name(cls, v):
        if v is not None:
            return v.lower()
        return v

    @field_validator("price")
    @classmethod
    def check_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than zero")
        return v


class ProductResponse(BaseModel):
    id: str
    name: str
    price: int
    description: str


# ──────────────────────────────────────────────────────────────────────────────
# NOTE: How @field_validator & @classmethod work
# ──────────────────────────────────────────────────────────────────────────────
#
# @field_validator("field_name")
# Tells Pydantic: "run this method on 'field_name' after type checking".
# The return value REPLACES the original input.
# If it raises ValueError → FastAPI returns 422 automatically.
#
# @classmethod
# Python decorator that makes the method receive the class (cls) instead of
# an instance (self). Required by Pydantic because validators run during
# object construction, before 'self' exists.
#
# These always come as a pair. You never call them directly — Pydantic's
# BaseModel.__init__ calls them automatically when you create an instance:
#
#     ProductCreate(name="  LaPtop  ")
#         ↓ Pydantic internally
#         1. isinstance("  LaPtop  ", str)  ← built into BaseModel, invisible
#         2. check_empty → "LaPtop"          ← @field_validator
#         3. lowercase_name → "laptop"       ← @field_validator
#         ↓
#         self.name = "laptop"  ← stored automatically
