from datetime import datetime
from product import Product

class Warehouse:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product, quantity: int):
        self.products.append({"Товар": product, "К-ть": quantity, "Останнє оновлення": datetime.now()})

    def remove_product(self, product_name: str, quantity: int):
        for item in self.products:
            if item["Товар"].name == product_name:
                if item["К-ть"] >= quantity:
                    item["К-ть"] -= quantity
                else:
                    print(f"Недостатньо товару {product_name} на складі!")
                item["Останнє оновлення"] = datetime.now()
                return
        print(f"Товар {product_name} не знайдено на складі!")

    def get_inventory(self):
        return [
            f"{item['Товар']} - К-ть: {item['К-ть']} (Останнє оновлення: {item['Останнє оновлення']})"
            for item in self.products
        ]