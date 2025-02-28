from money import Money
from product import Product
from warehouse import Warehouse
from reporting import Reporting

if __name__ == "__main__":
    print("\n" + "*" * 50)
    print(" СИСТЕМА УПРАВЛІННЯ СКЛАДОМ ".center(50, "*"))
    print("*" * 50 + "\n")
    
    price1 = Money("UAH", 40000, 50)
    price2 = Money("USD", 1500, 75)
    price3 = Money("EUR", 2500, 30)
    price4 = Money("UAH", 5000, 99)
    price5 = Money("USD", 800, 25)
    price_discount = Money("UAH", 5000, 0)

    product1 = Product("Ноутбук", "Dell", price1, "Електроніка")
    product2 = Product("Планшет", "Samsung", price2, "Електроніка")
    product3 = Product("Смартфон", "Apple", price3, "Електроніка")
    product4 = Product("Навушники", "Sony", price4, "Аксесуари")
    product5 = Product("Чохол для телефону", "Baseus", price5, "Аксесуари")

    warehouse = Warehouse()
    warehouse.add_product(product1, 5)
    warehouse.add_product(product2, 10)
    warehouse.add_product(product3, 7)
    warehouse.add_product(product4, 15)
    warehouse.add_product(product5, 30)

    print("Товари на складі:")
    for item in warehouse.get_inventory():
        print(item)
    
    print("\n" + "-" * 50)
    print("ЗМЕНШЕННЯ ЦІНИ".center(50))
    print("-" * 50)
    
    product1.decrease_price(price_discount)
    print(f"Оновлена ціна на {product1.name}: {product1}")

    print("\n" + "-" * 50)
    print("ВИДАЛЕННЯ ТОВАРІВ".center(50))
    print("-" * 50)
    
    warehouse.remove_product("Планшет", 3)
    warehouse.remove_product("Навушники", 5)

    Reporting.inventory_report(warehouse)
