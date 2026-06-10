from pydantic import BaseModel

class Product(BaseModel):
    name:str
    id:int
    quantity:int
    price:float


