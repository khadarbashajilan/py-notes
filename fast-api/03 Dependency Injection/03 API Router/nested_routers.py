"""
API Router Nesting
This module demonstrates how to organize complex APIs using nested routers in FastAPI for better structure and scalability.
"""

from fastapi import FastAPI, APIRouter, Depends, HTTPException

# ==========================================
# FILE: dependencies.py
# ==========================================
# In a real project, this would be in its own file.
# It holds shared logic like authentication, database sessions, etc.

async def verify_api_key(api_key: str):
    if api_key != "12345":
        raise HTTPException(status_code=401, detail="Invalid API Key")


# ==========================================
# FILE: routers/reviews.py
# ==========================================
# In a real project, this would be in routers/reviews.py
# Notice there is no prefix here. The parent router will handle it.

reviews_router = APIRouter(tags=["Reviews"])

@reviews_router.get("/")
async def get_reviews(product_id: int):
    return [{"product_id": product_id, "text": "Great product!"}]

# Router-level dependency: protects this route without cluttering the function signature
@reviews_router.post("/", dependencies=[Depends(verify_api_key)])
async def add_review(product_id: int, text: str):
    return {"product_id": product_id, "text": text}


# ==========================================
# FILE: routers/products.py
# ==========================================
# In a real project, this would be in routers/products.py
# Notice we import reviews_router here and nest it.

products_router = APIRouter(prefix="/products", tags=["Products"])

@products_router.get("/")
async def list_products():
    return [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Phone"}]

@products_router.post("/", dependencies=[Depends(verify_api_key)])
async def create_product(name: str):
    return {"id": 3, "name": name}

# NESTING: We attach the reviews_router to the products_router.
# Because products_router has "/products", this creates "/products/{product_id}/reviews"
products_router.include_router(
    reviews_router, 
    prefix="/{product_id}/reviews"
)


# ==========================================
# FILE: main.py
# ==========================================
# The entry point of your application. 
# It simply creates the app and wires the main routers together.

app = FastAPI(title="My Organized API")

# We only need to include the products_router. 
# Because reviews_router is nested inside it, it gets included automatically!
app.include_router(products_router)

