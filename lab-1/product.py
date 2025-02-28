from money import Money

class Product:
    def __init__(self, name: str, brand: str, price: Money, category: str = "Загальна"):
        self.name = name
        self.brand = brand
        self.price = price
        self.category = category
        self.stock = 0

    def decrease_price(self, amount: Money):
        total_cents = self.price.whole * 100 + self.price.cents - (amount.whole * 100 + amount.cents)
        if total_cents < 0:
            total_cents = 0
        self.price.whole, self.price.cents = divmod(total_cents, 100)

    def __str__(self):
        prices = self.price.get_all_currencies()
        return (f"{self.name} ({self.brand}, {self.category}) - Ціна: "
                f"{prices['UAH']}, {prices['USD']}, {prices['EUR']}")