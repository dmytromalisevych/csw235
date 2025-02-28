class Money:
    exchange_rates = {"UAH": 1, "USD": 40, "EUR": 43}

    def __init__(self, currency: str, whole: int, cents: int):
        self.currency = currency
        self.whole = whole
        self.cents = cents

    def __str__(self):
        return f"{self.whole}.{self.cents:02d} {self.currency}"

    def set_value(self, whole: int, cents: int):
        self.whole = whole
        self.cents = cents

    def convert_to(self, target_currency: str):
        total_uah = (self.whole * 100 + self.cents) * self.exchange_rates[self.currency] / 100
        total_target = total_uah / self.exchange_rates[target_currency]
        whole, cents = divmod(round(total_target * 100), 100)
        return Money(target_currency, whole, cents)
    
    def get_all_currencies(self):
        return {currency: self.convert_to(currency) for currency in self.exchange_rates}
