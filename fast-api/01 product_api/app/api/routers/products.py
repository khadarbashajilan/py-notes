from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.models.product import ProductResponse, ProductCreate, ProductUpdate
from app.services import product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
def get_all(category: Optional[str] = None, min_price: Optional[float] = None):
    return product_service.get_all_products(category, min_price)  

@router.get("/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product_by_id(id:int):
    return product_service.get_product_by_id(id)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(data:ProductCreate):
    return product_service.create_product(data)
    
@router.patch("/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def partial_update(id:int, data:ProductUpdate):
    return product_service.partial_update(id, data)
        
        
@router.put("/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def update_product(id:int, product:ProductCreate):
    return product_service.update_product(id, product)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def  delete_product(id:int):
    return product_service.delete_product(id)