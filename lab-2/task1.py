from abc import ABC, abstractmethod

class Subscription(ABC):
    def __init__(self, name, monthly_fee, min_period, channels, features):
        self.name = name
        self.monthly_fee = monthly_fee
        self.min_period = min_period
        self.channels = channels
        self.features = features

    def __str__(self):
        return (f"Підписка {self.name}:\n"
                f"  Щомісячна плата: {self.monthly_fee} грн\n"
                f"  Мінімальний період: {self.min_period} місяців\n"
                f"  Канали: {', '.join(self.channels)}\n"
                f"  Можливості: {', '.join(self.features)}")

class DomesticSubscription(Subscription):
    def __init__(self):
        super().__init__("Домашня", 400, 3, [
            "ICTV", "1+1", "Інтер", "СТБ", "Новий канал", "ТЕТ", "Україна", "Мега", "НЛО TV", "К1", "К2"
        ], ["HD Якість"])

class EducationalSubscription(Subscription):
    def __init__(self):
        super().__init__("Освітня", 320, 6, [
            "Наука", "Історія", "Discovery Channel", "National Geographic", "MEGOGO Енциклопедія",
            "Animal Planet", "Da Vinci Learning", "Еспресо TV", "Україна 24", "ПЛЮСПЛЮС"
        ], ["Без реклами", "Офлайн-доступ"])

class PremiumSubscription(Subscription):
    def __init__(self):
        super().__init__("Преміум", 800, 1, [
            "Усі канали", "HBO", "Netflix", "FOX", "EUROSPORT", "CNN", "BBC World News", "MTV", "VH1", "Cartoon Network",
            "Disney Channel", "Cinemax", "AMC", "Discovery Science", "Comedy Central", "Nickelodeon"
        ], ["4K Стрімінг", "Багатоекранний режим", "Без реклами"])

class SubscriptionCreator(ABC):
    @abstractmethod
    def create_subscription(self, sub_type):
        pass

class WebSite(SubscriptionCreator):
    def create_subscription(self, sub_type):
        print("Оформлення через вебсайт...")
        return self._create(sub_type)

    def _create(self, sub_type):
        return sub_type()

class MobileApp(SubscriptionCreator):
    def create_subscription(self, sub_type):
        print("Оформлення через мобільний застосунок...")
        return self._create(sub_type)

    def _create(self, sub_type):
        return sub_type()

class ManagerCall(SubscriptionCreator):
    def create_subscription(self, sub_type):
        print("Оформлення через дзвінок менеджера...")
        return self._create(sub_type)

    def _create(self, sub_type):
        return sub_type()

def main():
    website = WebSite()
    mobile_app = MobileApp()
    manager_call = ManagerCall()

    domestic_sub = website.create_subscription(DomesticSubscription)
    print(domestic_sub, '\n')
    
    edu_sub = mobile_app.create_subscription(EducationalSubscription)
    print(edu_sub, '\n')
    
    premium_sub = manager_call.create_subscription(PremiumSubscription)
    print(premium_sub, '\n')

if __name__ == "__main__":
    main()
