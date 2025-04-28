from abc import ABC, abstractmethod

class SupportHandler(ABC):
    
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, handler):
        self._next_handler = handler
        return handler
    
    def handle(self, issue):

        if self.can_handle(issue):
            return self.process(issue)
        elif self._next_handler:
            return self._next_handler.handle(issue)
        return None
    
    @abstractmethod
    def can_handle(self, issue):
        pass
    
    @abstractmethod
    def process(self, issue):
        pass


class TechnicalSupportHandler(SupportHandler):
    
    def can_handle(self, issue):
        return issue.get('type') == 'technical'
    
    def process(self, issue):
        return f"Технічна підтримка: Вирішуємо проблему '{issue.get('description')}'. Можливо, вам допоможе перезавантаження пристрою."


class BillingSupportHandler(SupportHandler):
    
    def can_handle(self, issue):
        return issue.get('type') == 'billing'
    
    def process(self, issue):
        return f"Фінансова підтримка: Вирішуємо проблему з оплатою '{issue.get('description')}'. Перевірте ваші платіжні реквізити."


class ProductSupportHandler(SupportHandler):
    
    def can_handle(self, issue):
        return issue.get('type') == 'product'
    
    def process(self, issue):
        return f"Підтримка продукту: Надаємо інформацію про '{issue.get('description')}'. Ознайомтеся з нашою документацією."


class GeneralSupportHandler(SupportHandler):
    
    def can_handle(self, issue):
        return issue.get('type') == 'general'
    
    def process(self, issue):
        return f"Загальна підтримка: Відповідаємо на загальне питання '{issue.get('description')}'. Дякуємо за звернення!"


class SupportSystem:
    
    def __init__(self):
        # Створення ланцюжка обробників
        technical = TechnicalSupportHandler()
        billing = BillingSupportHandler()
        product = ProductSupportHandler()
        general = GeneralSupportHandler()
        
        technical.set_next(billing).set_next(product).set_next(general)
        
        self.handler = technical
    
    def start_support(self):
        print("Ласкаво просимо до системи підтримки користувачів!")
        print("Ми допоможемо вам вирішити вашу проблему.")
        
        while True:
            issue = self._get_issue_from_user()
            if issue:
                result = self.handler.handle(issue)
                if result:
                    print("\nРезультат обробки вашого запиту:")
                    print(result)
                    print("\nДякуємо за звернення до нашої служби підтримки!")
                    break
                else:
                    print("\nНа жаль, ми не змогли знайти відповідний рівень підтримки для вашої проблеми.")
                    print("Давайте спробуємо знову.")
            else:
                print("\nНа жаль, ми не змогли визначити тип вашої проблеми.")
                print("Давайте спробуємо знову.")
    
    def _get_issue_from_user(self):
        issue = {}
        
        print("\n--- Рівень 1: Визначення типу проблеми ---")
        print("1. Технічна проблема")
        print("2. Питання щодо оплати")
        print("3. Інформація про продукт")
        print("4. Загальне питання")
        
        choice = input("Виберіть тип проблеми (1-4): ")
        
        if choice == '1':
            issue['type'] = 'technical'
            print("\n--- Рівень 2: Технічна проблема ---")
            print("1. Проблема з підключенням")
            print("2. Проблема з пристроєм")
            print("3. Проблема з програмним забезпеченням")
            
            tech_choice = input("Виберіть тип технічної проблеми (1-3): ")
            
            if tech_choice == '1':
                issue['description'] = 'проблема з підключенням'
            elif tech_choice == '2':
                issue['description'] = 'проблема з пристроєм'
            elif tech_choice == '3':
                issue['description'] = 'проблема з програмним забезпеченням'
            else:
                return None
            
        elif choice == '2':
            issue['type'] = 'billing'
            print("\n--- Рівень 2: Питання щодо оплати ---")
            print("1. Перевірка балансу")
            print("2. Проблема з оплатою")
            print("3. Питання щодо тарифів")
            
            billing_choice = input("Виберіть тип питання щодо оплати (1-3): ")
            
            if billing_choice == '1':
                issue['description'] = 'перевірка балансу'
            elif billing_choice == '2':
                issue['description'] = 'проблема з оплатою'
            elif billing_choice == '3':
                issue['description'] = 'питання щодо тарифів'
            else:
                return None
            
        elif choice == '3':
            issue['type'] = 'product'
            print("\n--- Рівень 2: Інформація про продукт ---")
            print("1. Характеристики продукту")
            print("2. Порівняння продуктів")
            print("3. Наявність продукту")
            
            product_choice = input("Виберіть тип інформації про продукт (1-3): ")
            
            if product_choice == '1':
                issue['description'] = 'характеристики продукту'
            elif product_choice == '2':
                issue['description'] = 'порівняння продуктів'
            elif product_choice == '3':
                issue['description'] = 'наявність продукту'
            else:
                return None
            
        elif choice == '4':
            issue['type'] = 'general'
            print("\n--- Рівень 2: Загальне питання ---")
            print("1. Контактна інформація")
            print("2. Години роботи")
            print("3. Інше")
            
            general_choice = input("Виберіть тип загального питання (1-3): ")
            
            if general_choice == '1':
                issue['description'] = 'контактна інформація'
            elif general_choice == '2':
                issue['description'] = 'години роботи'
            elif general_choice == '3':
                print("\n--- Рівень 3: Уточнення ---")
                print("1. Скарга")
                print("2. Пропозиція")
                print("3. Запитання")
                
                detail_choice = input("Виберіть тип уточнення (1-3): ")
                
                if detail_choice == '1':
                    issue['description'] = 'скарга'
                elif detail_choice == '2':
                    issue['description'] = 'пропозиція'
                elif detail_choice == '3':
                    print("\n--- Рівень 4: Тип запитання ---")
                    print("1. Щодо акцій")
                    print("2. Щодо послуг")
                    print("3. Інше запитання")
                    
                    question_choice = input("Виберіть тип запитання (1-3): ")
                    
                    if question_choice == '1':
                        issue['description'] = 'запитання щодо акцій'
                    elif question_choice == '2':
                        issue['description'] = 'запитання щодо послуг'
                    elif question_choice == '3':
                        issue['description'] = 'інше запитання'
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            return None
        
        return issue


def main():
    support_system = SupportSystem()
    support_system.start_support()


if __name__ == "__main__":
    main()