from fastapi import HTTPException

def get_review_from_product(product):
    if not product.review:
        raise HTTPException(status_code=404, detail="Review Not Found")
    return product

def add_review_to_product(product, review: str):
    product.review = review
    return product
