from abc import ABC, abstractmethod
from enum import Enum, auto

class NodeState(ABC):
    """Базовий клас для станів вузла"""
    
    @abstractmethod
    def render(self, node, indent=0) -> str:
        """Рендеринг вузла в поточному стані"""
        pass

class VisibilityState(Enum):
    VISIBLE = auto()    # Видимий
    HIDDEN = auto()     # Прихований
    COLLAPSED = auto()  # Згорнутий

class VisibleState(NodeState):
    """Стан видимого вузла"""
    
    def render(self, node, indent=0) -> str:
        return node._do_render(indent)

class HiddenState(NodeState):
    """Стан прихованого вузла"""
    
    def render(self, node, indent=0) -> str:
        return ""

class CollapsedState(NodeState):
    """Стан згорнутого вузла"""
    
    def render(self, node, indent=0) -> str:
        indentation = " " * indent
        return f"{indentation}{node._render_self()}"

class StatefulNode:
    """Мікшин для додавання підтримки станів"""
    
    def __init__(self):
        self._state: NodeState = VisibleState()
    
    def set_visibility(self, state: VisibilityState):
        """Змінити стан видимості"""
        if state == VisibilityState.VISIBLE:
            self._state = VisibleState()
        elif state == VisibilityState.HIDDEN:
            self._state = HiddenState()
        elif state == VisibilityState.COLLAPSED:
            self._state = CollapsedState()
    
    def render_with_state(self, indent=0) -> str:
        """Рендеринг з урахуванням стану"""
        return self._state.render(self, indent)
