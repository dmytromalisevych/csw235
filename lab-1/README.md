# Система управління складом

## Опис

Цей проєкт реалізує систему управління складом товарів з можливістю обліку найменувань, цін у трьох валютах (гривня, долар, євро), кількості товарів, дати останнього оновлення та можливості зменшення цін.

Програма підтримує:

- Додавання товарів на склад

- Видалення товарів зі складу

- Перерахунок цін у трьох валютах

- Формування звітності

- Класи та їх функціональність

``Money``

Клас Money відповідає за роботу з грошовими одиницями. Він дозволяє конвертувати суми між гривнями, доларами та євро, а також зберігає вартість товарів у трьох валютах одночасно.

Фрагмент коду:

```class Money:
exchange_rates = {"UAH": 1, "USD": 40, "EUR": 43}
def convert_to(self, target_currency: str):
total_uah = (self.whole * 100 + self.cents) * self.exchange_rates[self.currency] / 100
total_target = total_uah / self.exchange_rates[target_currency]
whole, cents = divmod(round(total_target * 100), 100)
return Money(target_currency, whole, cents)
```
``Product``

Клас Product містить інформацію про товар: назву, бренд, категорію та ціну в трьох валютах. Він також має метод decrease_price(), який дозволяє змінювати ціну товару.

Фрагмент коду:
```
class Product:
    def decrease_price(self, amount: Money):
        total_cents = self.price.whole * 100 + self.price.cents - (amount.whole * 100 + amount.cents)
        if total_cents < 0:
            total_cents = 0
        self.price.whole, self.price.cents = divmod(total_cents, 100)
```
``Warehouse``

Клас Warehouse управляє списком товарів на складі. Він дозволяє додавати товари, видаляти їх та отримувати список усіх товарів.

Фрагмент коду:
```
class Warehouse:
    def add_product(self, product: Product, quantity: int):
        self.products.append({"Товар": product, "К-ть": quantity, "Останнє оновлення": datetime.now()})
```
``Reporting``

Клас Reporting формує звіти по залишкам на складі.

Фрагмент коду:
```
class Reporting:
    @staticmethod
    def inventory_report(warehouse: Warehouse):
        print("РЕЗУЛЬТАТ ІНВЕНТАРИЗАЦІЇ")
        for item in warehouse.get_inventory():
            print(item)
```
Використані принципи програмування

``SOLID``

- ✅ S: Принцип єдиної відповідальності (SRP) – кожен клас виконує лише свою функцію.
- ✅ O: Принцип відкритості/закритості (OCP) – легко додати нові валюти без зміни існуючого коду.
- ✅ L: Принцип підстановки Лісков (LSP) – всі об'єкти Money можуть використовуватися взаємозамінно.
- ✅ I: Принцип розділення інтерфейсів (ISP) – клас Reporting містить лише звітність.
- ✅ D: Принцип інверсії залежностей (DIP) – Warehouse працює з Product, не залежачи від конкретних реалізацій.

``Додаткові принципи``

- ✅ DRY: Уникаємо дублювання коду завдяки використанню класів.
- ✅ KISS: Код зрозумілий та легкий для читання.
- ✅ YAGNI: Реалізовано лише необхідний функціонал.
- ✅ Fail Fast: Помилки виводяться одразу при їх виникненні.
- ✅ Program to Interfaces: Методи працюють з абстракціями (Product, Money).