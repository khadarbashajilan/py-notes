import asyncio
from fastapi import APIRouter, Depends, Body
from app.services.product_service import get_product_by_id
from app.services.review_service import get_review_from_product, add_review_to_product


async def get_product_dep(product_id: int):
    return get_product_by_id(product_id)


review_router = APIRouter(
    prefix="/products",
    tags=["Reviews"]
)


@review_router.get("/{product_id}/reviews")
async def read_reviews(product=Depends(get_product_dep)):
    await asyncio.sleep(0.01)
    return get_review_from_product(product)


@review_router.post("/{product_id}/reviews")
async def create_review(review: str = Body(...), product=Depends(get_product_dep)):
    await asyncio.sleep(0.01)
    return add_review_to_product(product, review)
