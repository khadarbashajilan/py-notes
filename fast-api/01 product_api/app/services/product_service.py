from typing import Optional
from app.db.memory import current_id_counter, products_list
from app.models.product import ProductCreate, ProductResponse, ProductUpdate 
from fastapi import HTTPException, status

def get_all_products(category: Optional[str] = None, min_price: Optional[float] = None):
    filtered_products = products_list
    if category:
        category = category.strip()
        category = category[0].upper() + category[1:]
    
    if category:
        filtered_products = [p for p in filtered_products if p.category == category]
        
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p.price >= min_price]
        
    return filtered_products

def get_product_by_id(id:int):
    for p in products_list:
        if p.id == id:
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not Found")



def create_product(data:ProductCreate):
    global current_id_counter
    current_id_counter += 1
    
    data_dict = data.model_dump()
    data_dict['id'] = current_id_counter
    
    new_product = ProductResponse(**data_dict)
    products_list.append(new_product)
    return new_product
    
def partial_update(id:int, data:ProductUpdate):
    for index,product in enumerate(products_list):
        if product.id == id:
            product_dict = product.model_dump()
            updated_data = data.model_dump(exclude_unset=True)
            
            product_dict.update(updated_data)
            
            updated_product = ProductResponse(**product_dict)
            products_list[index] = updated_product
            return updated_product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")

def update_product(id:int, product:ProductCreate):
    for i,p in enumerate(products_list):
        if p.id==id:
            updated_dict = product.model_dump()
            updated_dict['id'] = id
            
            updated_product = ProductResponse(**updated_dict)
            products_list[i] = updated_product
            return updated_product
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")
    
    
def  delete_product(id:int):
    for index, product in enumerate(products_list):
        if product.id == id:
            products_list.pop(index)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")
    