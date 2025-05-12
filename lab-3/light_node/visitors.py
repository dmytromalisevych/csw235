from abc import ABC, abstractmethod
from typing import List, Dict
from .base import LightNode, LightElementNode, LightTextNode, ClosureType

class NodeVisitor(ABC):
    """Базовий клас для відвідувачів"""
    
    @abstractmethod
    def visit_element(self, element: LightElementNode) -> None:
        """Відвідати елемент"""
        pass
    
    @abstractmethod
    def visit_text(self, text: LightTextNode) -> None:
        """Відвідати текстовий вузол"""
        pass

class HTMLValidator(NodeVisitor):
    """Відвідувач для валідації HTML"""
    
    def __init__(self):
        self.errors: List[str] = []
    
    def visit_element(self, element: LightElementNode) -> None:
        if not element.tag_name:
            self.errors.append("Елемент не має назви тегу")
        
        if element.closure_type == ClosureType.PAIRED and not element.children:
            self.errors.append(f"Порожній парний тег: {element.tag_name}")
    
    def visit_text(self, text: LightTextNode) -> None:
        if not text.text.strip():
            self.errors.append("Порожній текстовий вузол")

class StyleCollector(NodeVisitor):
    """Відвідувач для аналізу стилів"""
    
    def __init__(self):
        self.class_usage: Dict[str, int] = {}
    
    def visit_element(self, element: LightElementNode) -> None:
        for css_class in element.css_classes:
            self.class_usage[css_class] = self.class_usage.get(css_class, 0) + 1
    
    def visit_text(self, text: LightTextNode) -> None:
        pass

def accept(self, visitor: NodeVisitor) -> None:
    """Прийняти відвідувача"""
    if isinstance(self, LightElementNode):
        visitor.visit_element(self)
        for child in self.children:
            child.accept(visitor)
    elif isinstance(self, LightTextNode):
        visitor.visit_text(self)

LightNode.accept = accept

class NodeMetricsCollector(NodeVisitor):
    """Відвідувач для збору метрик про дерево"""
    
    def __init__(self):
        self.element_count: int = 0
        self.text_nodes_count: int = 0
        self.max_depth: int = 0
        self.current_depth: int = 0
    
    def visit_element(self, element: LightElementNode) -> None:
        self.element_count += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        
        for child in element.children:
            child.accept(self)
            
        self.current_depth -= 1
    
    def visit_text(self, text: LightTextNode) -> None:
        self.text_nodes_count += 1

class AccessibilityChecker(NodeVisitor):
    """Відвідувач для перевірки доступності"""
    
    def __init__(self):
        self.warnings: List[str] = []
    
    def visit_element(self, element: LightElementNode) -> None:
        if element.tag_name == 'img':
            self.warnings.append(f"Зображення повинно мати атрибут alt")
            
        if element.tag_name in ['a', 'button']:
            self.warnings.append(f"Інтерактивний елемент {element.tag_name} повинен мати aria-label")
    
    def visit_text(self, text: LightTextNode) -> None:
        pass
