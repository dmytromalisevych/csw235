import copy

class FluVirus:
    def __init__(self, name, weight, age, virus_type):
        self.name = name
        self.weight = weight  
        self.age = age  
        self.virus_type = virus_type 
        self.children = []

    def add_child(self, child_virus):
        self.children.append(child_virus)

    def clone(self):
        cloned_virus = copy.deepcopy(self)
        return cloned_virus

    def display_info(self, level=0):
        indent = "  " * level
        print(f"{indent}Вірус: {self.name}, Тип: {self.virus_type}, Вага: {self.weight} мкг, Вік: {self.age} днів")
        for child in self.children:
            child.display_info(level + 1)

parent_virus = FluVirus("Грип A", 0.8, 5, "H1N1")
child_virus1 = FluVirus("Грип A1", 0.6, 3, "H1N1")
child_virus2 = FluVirus("Грип A2", 0.5, 2, "H1N1")
grandchild_virus = FluVirus("Грип A1.1", 0.3, 1, "H1N1")

child_virus1.add_child(grandchild_virus)
parent_virus.add_child(child_virus1)
parent_virus.add_child(child_virus2)

cloned_virus = parent_virus.clone()

print("Оригінальне сімейство вірусів:")
parent_virus.display_info()

print("\nКлоноване сімейство вірусів:")
cloned_virus.display_info()
