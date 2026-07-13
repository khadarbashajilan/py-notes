import asyncio
from fastapi import APIRouter, Depends, status
from typing import List, Optional
from models import ProductResponse, ProductCreate, ProductUpdate
from app.services import product_service
from dependencies import get_pagination, verify_token

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

protected_router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(verify_token)]
)


@router.get("/", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
async def read_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    pagination: tuple[int, int] = Depends(get_pagination)
):
    await asyncio.sleep(0.01)
    skip, limit = pagination
    all_products = product_service.get_all_products(category, min_price)
    return all_products[skip:skip + limit]


@router.get("/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product_by_id(id: int):
    await asyncio.sleep(0.01)
    return product_service.get_product_by_id(id)


@protected_router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate):
    await asyncio.sleep(0.01)
    return product_service.create_product(data)


@protected_router.patch("/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product_partial(id: int, data: ProductUpdate):
    await asyncio.sleep(0.01)
    return product_service.partial_update(id, data)


@protected_router.put("/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(id: int, product: ProductCreate):
    await asyncio.sleep(0.01)
    return product_service.update_product(id, product)


@protected_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int):
    await asyncio.sleep(0.01)
    return product_service.delete_product(id)
