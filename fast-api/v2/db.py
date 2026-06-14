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


def update_product(name: str, data: ProductCreate) -> ProductResponse:
    name = name.strip().lower()

    for i, p in enumerate(products):
        if p.name == name:
            if data.name != name:
                for q in products:
                    if q.name == data.name:
                        raise HTTPException(409, "Product with this name already exists")
            updated = ProductResponse(
                id=p.id,
                name=data.name,
                price=data.price,
                description=data.description,
            )
            products[i] = updated
            return updated

    raise HTTPException(404, "Product not found")


def patch_product(name: str, data: ProductUpdate) -> ProductResponse:
    name = name.strip().lower()

    for i, p in enumerate(products):
        if p.name == name:
            new_name = data.name if data.name is not None else p.name
            if new_name != name:
                for q in products:
                    if q.name == new_name:
                        raise HTTPException(409, "Product with this name already exists")
            updated = ProductResponse(
                id=p.id,
                name=new_name,
                price=data.price if data.price is not None else p.price,
                description=data.description if data.description is not None else p.description,
            )
            products[i] = updated
            return updated

    raise HTTPException(404, "Product not found")


def delete_product(name: str) -> None:
    name = name.strip().lower()
    for i, p in enumerate(products):
        if p.name == name:
            products.pop(i)
            return
    raise HTTPException(404, "Product not found")
