from abc import ABC, abstractmethod
import time
import random
import os
import sys
from termcolor import colored

def fancy_print(text, color=None, delay=0.03, style=None):
    for char in text:
        sys.stdout.write(colored(char, color, attrs=style))
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')

def print_box(message, width=50, title="", color="white"):
    lines = message.split('\n')
    space = width - 4
    
    if title:
        title = f" {title} "
        left_padding = (width - len(title)) // 2
        right_padding = width - len(title) - left_padding
        fancy_print(f"╭{'─' * left_padding}{title}{'─' * right_padding}╮", color)
    else:
        fancy_print(f"╭{'─' * (width - 2)}╮", color)
    
    for line in lines:
        chunks = [line[i:i+space] for i in range(0, len(line), space)]
        for chunk in chunks:
            padding = space - len(chunk)
            fancy_print(f"│ {chunk}{' ' * padding}   │", color)
    
    fancy_print(f"╰{'─' * (width)}╯", color)
    time.sleep(0.5)

class Hero(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_attack(self):
        pass

    @abstractmethod
    def get_defense(self):
        pass

    @abstractmethod
    def get_health(self):
        pass
    
    @abstractmethod
    def display_stats(self):
        pass

class Warrior(Hero):
    def get_description(self):
        return "Воїн"

    def get_attack(self):
        return 10

    def get_defense(self):
        return 8

    def get_health(self):
        return 100
    
    def display_stats(self):
        description = f"{self.get_description()}"
        stats = f"⚔️ Атака: {self.get_attack()}  |  🛡️ Захист: {self.get_defense()}  |  ❤️ Здоров'я: {self.get_health()}"
        print_box(stats, width=60, title=description, color="red")


class Mage(Hero):
    def get_description(self):
        return "Маг"

    def get_attack(self):
        return 15

    def get_defense(self):
        return 4

    def get_health(self):
        return 70
    
    def display_stats(self):
        description = f"{self.get_description()}"
        stats = f"⚔️ Атака: {self.get_attack()}  |  🛡️ Захист: {self.get_defense()}  |  ❤️ Здоров'я: {self.get_health()}"
        print_box(stats, width=60, title=description, color="blue")


class Paladin(Hero):
    def get_description(self):
        return "Паладін"

    def get_attack(self):
        return 8

    def get_defense(self):
        return 12

    def get_health(self):
        return 120
    
    def display_stats(self):
        description = f"{self.get_description()}"
        stats = f"⚔️ Атака: {self.get_attack()}  |  🛡️ Захист: {self.get_defense()}  |  ❤️ Здоров'я: {self.get_health()}"
        print_box(stats, width=60, title=description, color="yellow")


class ItemDecorator(Hero):
    def __init__(self, hero):
        self.hero = hero
        self._item_name = "Предмет"
        self._attack_bonus = 0
        self._defense_bonus = 0
        self._health_bonus = 0

    def get_description(self):
        return self.hero.get_description()

    def get_attack(self):
        return self.hero.get_attack() + self._attack_bonus

    def get_defense(self):
        return self.hero.get_defense() + self._defense_bonus

    def get_health(self):
        return self.hero.get_health() + self._health_bonus
    
    def display_stats(self):
        description = f"{self.get_description()}"
        stats = f"⚔️ Атака: {self.get_attack()}  |  🛡️ Захист: {self.get_defense()}  |  ❤️ Здоров'я: {self.get_health()}"
        
        if isinstance(self.hero, ItemDecorator):
            color = random.choice(["cyan", "magenta", "green", "white"])
        else:
            if isinstance(self.hero, Warrior):
                color = "red"
            elif isinstance(self.hero, Mage):
                color = "blue"
            else:
                color = "yellow"
        
        print_box(stats, width=60, title=description, color=color)


class Sword(ItemDecorator):
    def __init__(self, hero):
        super().__init__(hero)
        self._item_name = "Меч"
        self._attack_bonus = 7

    def get_description(self):
        return f"{self.hero.get_description()} з мечем"


class Staff(ItemDecorator):
    def __init__(self, hero):
        super().__init__(hero)
        self._item_name = "Посох"
        self._attack_bonus = 5
        self._health_bonus = 15

    def get_description(self):
        return f"{self.hero.get_description()} з посохом"


class Hammer(ItemDecorator):
    def __init__(self, hero):
        super().__init__(hero)
        self._item_name = "Молот"
        self._attack_bonus = 10
        self._defense_bonus = 2

    def get_description(self):
        return f"{self.hero.get_description()} з молотом"


class LeatherArmor(ItemDecorator):
    def __init__(self, hero):
        super().__init__(hero)
        self._item_name = "Шкіряна броня"
        self._defense_bonus = 3

    def get_description(self):
        return f"{self.hero.get_description()} в шкіряній броні"


class PlateArmor(ItemDecorator):
    def __init__(self, hero):
        super().__init__(hero)
        self._item_name = "Латна броня"
        self._defense_bonus = 8
        self._health_bonus = 20

    def get_description(self):
        return f"{self.hero.get_description()} в латній броні"


class Robe(ItemDecorator):
    def __init__(self, hero):
        super().__init__(hero)
        self._item_name = "Магічна мантія"
        self._defense_bonus = 2
        self._attack_bonus = 3

    def get_description(self):
        return f"{self.hero.get_description()} в магічній мантії"


class AmuletOfPower(ItemDecorator):
    def __init__(self, hero):
        super().__init__(hero)
        self._item_name = "Амулет сили"
        self._attack_bonus = 4
        self._health_bonus = 10

    def get_description(self):
        return f"{self.hero.get_description()} з амулетом сили"


class RingOfProtection(ItemDecorator):
    def __init__(self, hero):
        super().__init__(hero)
        self._item_name = "Перстень захисту"
        self._defense_bonus = 5

    def get_description(self):
        return f"{self.hero.get_description()} з перснем захисту"


class Helmet(ItemDecorator):
    def __init__(self, hero):
        super().__init__(hero)
        self._item_name = "Шолом"
        self._defense_bonus = 4
        self._health_bonus = 5

    def get_description(self):
        return f"{self.hero.get_description()} в шоломі"


def create_hero_scene(hero_class, name):
    os.system('cls' if os.name == 'nt' else 'clear')
    fancy_print("СТВОРЕННЯ ГЕРОЯ...", "yellow", delay=0.1, style=["bold"])
    time.sleep(1)
    
    fancy_print(f"З глибин творення з'являється нова душа...", "cyan", delay=0.05)
    time.sleep(0.5)
    
    if hero_class == Warrior:
        fancy_print("Могутній ВОЇН! Дух битви наповнює його серце!", "red", delay=0.05, style=["bold"])
    elif hero_class == Mage:
        fancy_print("Загадковий МАГ! Потік магії тече через його вени!", "blue", delay=0.05, style=["bold"])
    elif hero_class == Paladin:
        fancy_print("Благородний ПАЛАДІН! Світло і мужність — його зброя!", "yellow", delay=0.05, style=["bold"])
    
    time.sleep(1)
    hero = hero_class()
    hero.display_stats()
    return hero


def equip_item_scene(hero, item_class):
    fancy_print("\nЕКІПІРУВАННЯ ГЕРОЯ...", "magenta", delay=0.08, style=["bold"])
    time.sleep(0.8)
    
    item_names = {
        Sword: "МЕЧ", Staff: "ПОСОХ", Hammer: "МОЛОТ",
        LeatherArmor: "ШКІРЯНУ БРОНЮ", PlateArmor: "ЛАТНУ БРОНЮ", Robe: "МАГІЧНУ МАНТІЮ",
        AmuletOfPower: "АМУЛЕТ СИЛИ", RingOfProtection: "ПЕРСТЕНЬ ЗАХИСТУ", Helmet: "ШОЛОМ"
    }
    
    item_name = item_names.get(item_class, "ПРЕДМЕТ")
    fancy_print(f"Герой знаходить {item_name}!", "green", delay=0.05)
    
    sys.stdout.write("Екіпірування")
    for _ in range(5):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write(" ЗАВЕРШЕНО!\n")
    time.sleep(0.5)
    
    decorated_hero = item_class(hero)
    decorated_hero.display_stats()
    return decorated_hero


def epic_battle_simulation(hero1, hero2):
    fancy_print("\n⚔️ ЕПІЧНА БИТВА! ⚔️", "yellow", delay=0.1, style=["bold"])
    time.sleep(1)
    
    fancy_print(f"{hero1.get_description()} проти {hero2.get_description()}!", "red", delay=0.05)
    time.sleep(0.5)
    
    hero1_hp = hero1.get_health()
    hero2_hp = hero2.get_health()
    
    round_num = 1
    while hero1_hp > 0 and hero2_hp > 0:
        fancy_print(f"\nРаунд {round_num}", "cyan", delay=0.05, style=["bold"])
        time.sleep(0.5)
        
        damage = max(1, hero1.get_attack() - hero2.get_defense() // 2)
        hero2_hp -= damage
        fancy_print(f"{hero1.get_description()} завдає {damage} шкоди! У {hero2.get_description()} залишається {max(0, hero2_hp)} здоров'я", "white", delay=0.03)
        time.sleep(0.3)
        
        if hero2_hp <= 0:
            break
            
        damage = max(1, hero2.get_attack() - hero1.get_defense() // 2)
        hero1_hp -= damage
        fancy_print(f"{hero2.get_description()} завдає {damage} шкоди! У {hero1.get_description()} залишається {max(0, hero1_hp)} здоров'я", "white", delay=0.03)
        
        round_num += 1
        time.sleep(0.7)
    
    fancy_print("\n🏆 РЕЗУЛЬТАТ БИТВИ 🏆", "yellow", delay=0.1, style=["bold"])
    if hero1_hp <= 0 and hero2_hp <= 0:
        fancy_print("НІЧИЯ! Обидва герої впали від виснаження!", "yellow", delay=0.05)
    elif hero1_hp <= 0:
        fancy_print(f"ПЕРЕМОГА! {hero2.get_description()} здобуває перемогу!", "green", delay=0.05)
    else:
        fancy_print(f"ПЕРЕМОГА! {hero1.get_description()} здобуває перемогу!", "green", delay=0.05)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    fancy_print("╔═════════════════════════════════════╗", "yellow", delay=0.01)
    fancy_print("║      ЛЕГЕНДИ ФЕНТЕЗІЙНИХ СВІТІВ     ║", "yellow", delay=0.01)
    fancy_print("╚═════════════════════════════════════╝", "yellow", delay=0.01)
    time.sleep(1)
    
    warrior = create_hero_scene(Warrior, "Воїн")
    time.sleep(1)

    equipped_warrior = warrior
    equipped_warrior = equip_item_scene(equipped_warrior, Sword)
    time.sleep(0.5)
    equipped_warrior = equip_item_scene(equipped_warrior, PlateArmor)
    time.sleep(0.5)
    equipped_warrior = equip_item_scene(equipped_warrior, Helmet)
    
    fancy_print("\n\n" + "=" * 60, "white", delay=0.01)
    time.sleep(0.5)
    mage = create_hero_scene(Mage, "Маг")
    time.sleep(1)
    
    equipped_mage = mage
    equipped_mage = equip_item_scene(equipped_mage, Staff)
    time.sleep(0.5)
    equipped_mage = equip_item_scene(equipped_mage, Robe)
    time.sleep(0.5)
    equipped_mage = equip_item_scene(equipped_mage, AmuletOfPower)
    
    time.sleep(1)
    fancy_print("\n\n" + "=" * 60, "white", delay=0.01)
    epic_battle_simulation(equipped_warrior, equipped_mage)
    
    time.sleep(1)
    fancy_print("\n\n" + "=" * 60, "white", delay=0.01)
    fancy_print("СТВОРЕННЯ ЛЕГЕНДАРНОГО ГЕРОЯ", "cyan", delay=0.05, style=["bold"])
    time.sleep(1)
    
    paladin = create_hero_scene(Paladin, "Паладін")
    super_paladin = paladin
    super_paladin = equip_item_scene(super_paladin, Hammer)
    super_paladin = equip_item_scene(super_paladin, PlateArmor)
    super_paladin = equip_item_scene(super_paladin, Helmet)
    super_paladin = equip_item_scene(super_paladin, RingOfProtection)
    super_paladin = equip_item_scene(super_paladin, AmuletOfPower)
    
    fancy_print("\nЛЕГЕНДАРНИЙ ГЕРОЙ СТВОРЕНИЙ!", "yellow", delay=0.05, style=["bold"])
    time.sleep(1)
    fancy_print("\nДекоратор успішно застосований для створення героїв з різним спорядженням.", "green", delay=0.02)
    fancy_print("Кожен предмет додає унікальні бонуси до характеристик героя.", "green", delay=0.02)
    fancy_print("Можливе використання декількох предметів одночасно.", "green", delay=0.02)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        fancy_print("\nПрограма завершена користувачем", "red")
    except Exception as e:
        fancy_print(f"\nПомилка: {e}", "red")