from abc import ABC, abstractmethod

class Device(ABC):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    @abstractmethod
    def get_info(self):
        pass

class Laptop(Device):
    def get_info(self):
        return f"Ноутбук {self.brand} {self.model}"

class Netbook(Device):
    def get_info(self):
        return f"Нетбук {self.brand} {self.model}"

class EBook(Device):
    def get_info(self):
        return f"Електронна книга {self.brand} {self.model}"

class Smartphone(Device):
    def get_info(self):
        return f"Смартфон {self.brand} {self.model}"

class DeviceFactory(ABC):
    @abstractmethod
    def create_laptop(self):
        pass
    
    @abstractmethod
    def create_netbook(self):
        pass
    
    @abstractmethod
    def create_ebook(self):
        pass
    
    @abstractmethod
    def create_smartphone(self):
        pass

class IProneFactory(DeviceFactory):
    def create_laptop(self):
        return Laptop("IProne", "MacX Pro")
    
    def create_netbook(self):
        return Netbook("IProne", "MacBook Air Mini")
    
    def create_ebook(self):
        return EBook("IProne", "iRead Pro")
    
    def create_smartphone(self):
        return Smartphone("IProne", "iProne 15")

class KiaomiFactory(DeviceFactory):
    def create_laptop(self):
        return Laptop("Kiaomi", "Mi Notebook Pro")
    
    def create_netbook(self):
        return Netbook("Kiaomi", "Redmi Book 14")
    
    def create_ebook(self):
        return EBook("Kiaomi", "Mi Read 2")
    
    def create_smartphone(self):
        return Smartphone("Kiaomi", "Kiaomi 13 Pro")

class BalaxyFactory(DeviceFactory):
    def create_laptop(self):
        return Laptop("Balaxy", "Galaxy Book Flex")
    
    def create_netbook(self):
        return Netbook("Balaxy", "Galaxy Chromebook Go")
    
    def create_ebook(self):
        return EBook("Balaxy", "Balaxy Tab S7 eReader")
    
    def create_smartphone(self):
        return Smartphone("Balaxy", "Balaxy S24 Ultra")

def main():
    factories = {
        "1": IProneFactory(),
        "2": KiaomiFactory(),
        "3": BalaxyFactory()
    }
    
    devices = {
        "1": "create_laptop",
        "2": "create_netbook",
        "3": "create_ebook",
        "4": "create_smartphone"
    }
    
    while True:
        print("\nОберіть бренд:")
        print("1. IProne")
        print("2. Kiaomi")
        print("3. Balaxy")
        print("4. Вихід")
        brand_choice = input("Ваш вибір: ")
        
        if brand_choice == "4":
            print("До побачення!")
            break
        
        if brand_choice not in factories:
            print("Невірний вибір! Спробуйте ще раз.")
            continue
        
        factory = factories[brand_choice]
        
        print("\nОберіть тип девайсу:")
        print("1. Ноутбук")
        print("2. Нетбук")
        print("3. Електронна книга")
        print("4. Смартфон")
        print("5. Назад")
        device_choice = input("Ваш вибір: ")
        
        if device_choice == "5":
            continue
        
        if device_choice not in devices:
            print("Невірний вибір! Спробуйте ще раз.")
            continue
        
        device = getattr(factory, devices[device_choice])()
        print(f"\nВи створили: {device.get_info()}")

if __name__ == "__main__":
    main()
