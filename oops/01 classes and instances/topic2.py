class Product:
    discount_rate = 0.1
    total_products = 0

    def __init__(self, name, price):
        """Initialize a Product with name, price, and increment total_products."""
        self.name = name
        self.price = price
        Product.total_products += 1

    def apply_discount(self):
        """Return the price after applying the class-level discount_rate."""
        return self.price - (self.price * Product.discount_rate)

    def __str__(self):
        """Return a formatted string with product name and price."""
        return f"The product name : {self.name} \nThe Price : {self.price}"


products = {"laptop":1000, "mouse":50, "keyboard":80}

products_cls = []

for name, price in products.items():
    products_cls.append(Product(name, price))

for prod in products_cls:
    print(prod)
    print(f"After Applying Discount : {prod.apply_discount()}")
    print()

# ============================================================
# Concept: Class Attributes vs Instance Attributes
# ============================================================
# Class attributes (discount_rate, total_products) are shared by
# all instances. They are defined directly in the class body and
# accessed via ClassName.attribute. Instance attributes (name,
# price) are unique to each object and set in __init__ via self.
#
# Key Terminology:
#   - Class Attribute:  A variable shared by all instances of a
#                       class (e.g., discount_rate)
#   - Instance Attribute: A variable unique to each instance
#                         (e.g., self.name)
#   - Class Variable:   Another name for class attribute
#   - self:             Refers to the current instance
#   - ClassName.attr:   Way to access class-level attributes
# ============================================================"
