from typing import Optional
from pydantic import BaseModel, Field, field_validator

class ProductCreate(BaseModel):
    name:str=Field(min_length=2, max_length=10, description="Name Of The Product")
    price:float = Field(gt=0, description="Price of the Product" )
    category:str = Field(min_length=4)
    
    @field_validator("category", "name")
    @classmethod
    def check_alphanumeric(cls,v):
        v = v.strip()
        if not v:
            raise ValueError("Field Cannot be Empty")

        v = v[0].upper() + v[1:]
        return v
    
class ProductUpdate(BaseModel):
    name:Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    
    
class ProductResponse(ProductCreate):
    id:int
    
    