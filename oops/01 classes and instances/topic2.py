class Product:
    discount_rate = 0.1
    total_products = 0

    def __init__(self,name, price):
        self.name = name
        self.price = price
        Product.total_products += 1

    def apply_discount(self):
        return self.price - (self.price * Product.discount_rate)

    def __str__(self):
        return f"The product name : {self.name} \nThe Price : {self.price}"


products = {"laptop":1000, "mouse":50, "keyboard":80}

products_cls = []

for name, price in products.items():
    products_cls.append(Product(name, price))

for prod in products_cls:
    print(prod)
    print(f"After Applying Discount : {prod.apply_discount()}")
    print()
