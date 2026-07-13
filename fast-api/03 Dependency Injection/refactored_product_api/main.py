import asyncio
from fastapi import FastAPI
from app.api.routers import products, reviews

app = FastAPI(
    title="Product Management API",
    description="A simple in-memory REST API for learning FastAPI.",
    version="1.0.0"
)

app.include_router(products.router)
app.include_router(products.protected_router)
app.include_router(reviews.review_router)


@app.get("/")
async def root():
    await asyncio.sleep(0.01)
    return {"message": "Welcome to the Product API! Visit /docs to test everything."}