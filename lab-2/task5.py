from abc import ABC, abstractmethod

class Character:
    def __init__(self, role, name):
        self.role = role
        self.name = name
        self.height = None
        self.body_type = None
        self.hair_color = None
        self.eye_color = None
        self.clothes = None
        self.weapon = None
        self.inventory = []
        self.actions = []

    def __str__(self):
        return (f"🔹 {self.role}: {self.name}\n"
                f"  🔸 Зріст: {self.height}\n"
                f"  🔸 Статура: {self.body_type}\n"
                f"  🔸 Колір волосся: {self.hair_color}\n"
                f"  🔸 Колір очей: {self.eye_color}\n"
                f"  🔸 Одяг: {self.clothes}\n"
                f"  🔸 Зброя: {self.weapon}\n"
                f"  🔸 Інвентар: {', '.join(self.inventory) if self.inventory else 'Порожньо'}\n"
                f"  🔸 Дії: {', '.join(self.actions) if self.actions else 'Не здійснював дій'}\n")

class CharacterBuilder(ABC):
    def __init__(self, role, name):
        self.character = Character(role, name)

    def set_height(self, height):
        self.character.height = height
        return self

    def set_body_type(self, body_type):
        self.character.body_type = body_type
        return self

    def set_hair_color(self, color):
        self.character.hair_color = color
        return self

    def set_eye_color(self, color):
        self.character.eye_color = color
        return self

    def set_clothes(self, clothes):
        self.character.clothes = clothes
        return self

    def set_weapon(self, weapon):
        self.character.weapon = weapon
        return self

    def add_item(self, item):
        self.character.inventory.append(item)
        return self

    @abstractmethod
    def add_special_action(self, action):
        pass

    def build(self):
        return self.character

class HeroBuilder(CharacterBuilder):
    def __init__(self, name):
        super().__init__("Богатир", name)

    def add_special_action(self, action):
        self.character.actions.append(f"Добрий вчинок: {action}")
        return self

class EnemyBuilder(CharacterBuilder):
    def __init__(self, name):
        super().__init__("Орк", name)

    def add_special_action(self, action):
        self.character.actions.append(f"Злий вчинок: {action}")
        return self

class Director:
    @staticmethod
    def create_bogatyr():
        return (HeroBuilder("Ілля Муромець")
                .set_height("200 см")
                .set_body_type("Міцна, мускулиста")
                .set_hair_color("Світлий")
                .set_eye_color("Сині")
                .set_clothes("Золоті обладунки, червоний плащ")
                .set_weapon("Кінний спис")
                .add_item("Меч богатирський")
                .add_item("Обруч честі")
                .add_special_action("Захистив князівство від ворогів")
                .add_special_action("Переміг Змія Горинича")
                .build())

    @staticmethod
    def create_orc():
        return (EnemyBuilder("Грог-Мясоруб")
                .set_height("230 см")
                .set_body_type("Гігантська, мускулиста")
                .set_hair_color("Лисий, зеленокожий")
                .set_eye_color("Палаючі червоні")
                .set_clothes("Броня з черепами")
                .set_weapon("Величезна булава")
                .add_item("Амулет темряви")
                .add_item("Флакон отрути")
                .add_special_action("Розграбував село")
                .add_special_action("Захопив фортецю людей")
                .build())

def main():
    bogatyr = Director.create_bogatyr()
    orc = Director.create_orc()

    print(bogatyr)
    print(orc)

if __name__ == "__main__":
    main()
