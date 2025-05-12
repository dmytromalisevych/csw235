from abc import ABC, abstractmethod
from collections import deque
from enum import Enum

class TraversalType(Enum):
    DEPTH_FIRST = "depth-first"     
    BREADTH_FIRST = "breadth-first" 

class NodeIterator(ABC):
    """Базовий інтерфейс ітератора"""
    
    @abstractmethod
    def has_next(self) -> bool:
        pass
    
    @abstractmethod
    def next(self):
        pass

class DepthFirstIterator(NodeIterator):
    """Ітератор для обходу в глибину"""
    
    def __init__(self, root):
        self.stack = [root]
    
    def has_next(self) -> bool:
        return bool(self.stack)
    
    def next(self):
        if not self.has_next():
            raise StopIteration("Немає більше елементів")
        
        node = self.stack.pop()
        if hasattr(node, 'children'):
            self.stack.extend(reversed(node.children))
        return node

class BreadthFirstIterator(NodeIterator):
    """Ітератор для обходу в ширину"""
    
    def __init__(self, root):
        self.queue = deque([root])
    
    def has_next(self) -> bool:
        return bool(self.queue)
    
    def next(self):
        if not self.has_next():
            raise StopIteration("Немає більше елементів")
        
        node = self.queue.popleft()
        if hasattr(node, 'children'):
            self.queue.extend(node.children)
        return node

class IterableLightNode:
    """Мікшин для додавання можливості ітерації"""
    
    def get_iterator(self, traversal_type=TraversalType.DEPTH_FIRST):
        """Отримати ітератор вказаного типу"""
        if traversal_type == TraversalType.DEPTH_FIRST:
            return DepthFirstIterator(self)
        return BreadthFirstIterator(self)
    
    def traverse(self, traversal_type=TraversalType.DEPTH_FIRST):
        """Генератор для зручного обходу дерева"""
        iterator = self.get_iterator(traversal_type)
        while iterator.has_next():
            yield iterator.next()
