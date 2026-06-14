from fastapi import FastAPI
from model import ProductCreate, ProductUpdate, ProductResponse
from db import create_product, get_all_products, get_product, update_product, patch_product, delete_product

app = FastAPI()


@app.post("/products", status_code=201, response_model=ProductResponse)
def create(data: ProductCreate):
    return create_product(data)


@app.get("/products", response_model=list[ProductResponse])
def list_all():
    return get_all_products()


@app.get("/products/{name}", response_model=ProductResponse)
def read(name: str):
    return get_product(name)


@app.put("/products/{name}", response_model=ProductResponse)
def update(name: str, data: ProductCreate):
    return update_product(name, data)


@app.patch("/products/{name}", response_model=ProductResponse)
def patch(name: str, data: ProductUpdate):
    return patch_product(name, data)


@app.delete("/products/{name}")
def delete(name: str):
    delete_product(name)
    return {"message": "product deleted successfully"}
