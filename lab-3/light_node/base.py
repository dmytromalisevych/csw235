from abc import ABC, abstractmethod
from enum import Enum, auto

class DisplayType(Enum):
    """Тип відображення елемента"""
    BLOCK = auto()   
    INLINE = auto()  

class ClosureType(Enum):
    """Тип закриття тегу"""
    SELF_CLOSING = auto()  
    PAIRED = auto()        

class LightNode(ABC):
    """Базовий абстрактний клас для всіх вузлів"""
    
    def __init__(self):
        self.parent = None
        self.children = []
        self.css_classes = []
    
    @abstractmethod
    def render(self, indent=0) -> str:
        """Рендеринг вузла у HTML"""
        pass
    
    def add_child(self, child):
        """Додати дочірній елемент"""
        self.children.append(child)
        child.parent = self
        return self
    
    def remove_child(self, child):
        """Видалити дочірній елемент"""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
        return self
    
    def add_class(self, css_class: str):
        """Додати CSS клас"""
        if css_class not in self.css_classes:
            self.css_classes.append(css_class)
        return self
    
    def remove_class(self, css_class: str):
        """Видалити CSS клас"""
        if css_class in self.css_classes:
            self.css_classes.remove(css_class)
        return self

class LightElementNode(LightNode):
    """Клас для HTML елементів"""
    
    def __init__(self, tag_name: str, display_type=DisplayType.BLOCK, 
                 closure_type=ClosureType.PAIRED):
        super().__init__()
        self.tag_name = tag_name
        self.display_type = display_type
        self.closure_type = closure_type
    
    def render(self, indent=0) -> str:
        """Рендеринг HTML елемента"""
        result = []
        indentation = " " * indent
        
        result.append(f"{indentation}<{self.tag_name}")
        

        if self.css_classes:
            class_list = " ".join(self.css_classes)
            result.append(f' class="{class_list}"')
        
        if self.closure_type == ClosureType.SELF_CLOSING:
            result.append("/>")
            return "".join(result)
        
        result.append(">")
        
        if self.children:
            for child in self.children:
                result.append("\n" + child.render(indent + 2))
            result.append(f"\n{indentation}")
        
        result.append(f"</{self.tag_name}>")
        
        return "".join(result)

class LightTextNode(LightNode):
    """Клас для текстових вузлів"""
    
    def __init__(self, text: str):
        super().__init__()
        self.text = text
        self.display_type = DisplayType.INLINE
    
    def render(self, indent=0) -> str:
        """Рендеринг текстового вузла"""
        return " " * indent + self.text
    
    def add_child(self, child):
        """Текстові вузли не можуть мати дочірніх елементів"""
        raise ValueError("Текстовий вузол не може мати дочірніх елементів")
    
    def add_class(self, css_class: str):
        """Текстові вузли не можуть мати CSS класів"""
        raise ValueError("Текстовий вузол не може мати CSS класів")
