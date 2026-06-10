from fastapi import FastAPI, HTTPException
from models import Product

app = FastAPI()

products = []

@app.get("/")
def greet():
    return {"message":"Welcome"}


@app.get("/all")
def all_products():
    if not products:
        return {"message": "Its Empty"}
    return products

# Create:

@app.post("/add")
def add_product(product:Product):
    products.append(product)
    return {"message":"Successfully added"}

#Read :

@app.get("/product/{product_id}")
def get_product(product_id :int):
    for p in products:
        if p.id == product_id:
            return p

    raise HTTPException(status_code=404, detail="Product not found")

#Update :

@app.put("/update/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for index, p in enumerate(products):
        if p.id == product_id :
            products[index] = updated_product
            return {"message": "Product updated successfully"}

    raise HTTPException(status_code=404, detail="Product not found")

#Delete:

@app.delete("/delete/{product_id}")
def delete_product(product_id:int):
    for index, p in enumerate(products):
        if p.id == product_id:
            products.pop(index)
            return {"message" : "Product deleted successfully"}

    raise HTTPException(status_code=404, detail="product not found")


