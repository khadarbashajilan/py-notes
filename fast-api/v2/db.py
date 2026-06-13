import uuid
from fastapi import HTTPException
from model import ProductCreate, ProductUpdate, ProductResponse

products: list[ProductResponse] = []


def create_product(data: ProductCreate) -> ProductResponse:
    for p in products:
        if p.name == data.name:
            raise HTTPException(409, "Product with this name already exists")

    product = ProductResponse(
        id=str(uuid.uuid4()),
        name=data.name,
        price=data.price,
        description=data.description,
    )
    products.append(product)
    return product


def get_all_products() -> list[ProductResponse]:
    return products


def get_product(name: str) -> ProductResponse:
    name = name.strip().lower()
    for p in products:
        if p.name == name:
            return p
    raise HTTPException(404, "Product not found")


def update_product(name: str, data: ProductUpdate) -> ProductResponse:
    name = name.strip().lower()

    idx = None
    for i, p in enumerate(products):
        if p.name == name:
            idx = i
            break

    if idx is None:
        raise HTTPException(404, "Product not found")

    new_name = data.name if data.name is not None else products[idx].name
    if new_name != name:
        for p in products:
            if p.name == new_name:
                raise HTTPException(409, "Product with this name already exists")

    updated = ProductResponse(
        id=products[idx].id,
        name=new_name,
        price=data.price if data.price is not None else products[idx].price,
        description=data.description if data.description is not None else products[idx].description,
    )
    products[idx] = updated
    return updated


def delete_product(name: str) -> None:
    name = name.strip().lower()
    for i, p in enumerate(products):
        if p.name == name:
            products.pop(i)
            return
    raise HTTPException(404, "Product not found")
