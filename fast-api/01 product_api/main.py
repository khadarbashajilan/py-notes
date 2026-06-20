from fastapi import FastAPI
from app.api.routers import products

app = FastAPI(
    title="Product Management API",
    description="A simple in-memory REST API for learning FastAPI.",
    version="1.0.0"
)

app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Product API! Visit /docs to test everything."}