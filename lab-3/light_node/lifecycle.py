from abc import ABC, abstractmethod
from enum import Enum, auto

class LifecycleEvent(Enum):
    CREATED = auto()          
    INSERTED = auto()     
    REMOVED = auto()        
    STYLES_APPLIED = auto() 
    CLASSLIST_APPLIED = auto()
    TEXT_RENDERED = auto()   

class LifecycleLightNode(ABC):
    """Базовий клас для вузлів з підтримкою життєвого циклу"""
    
    def __init__(self):
        self.parent = None
        self.on_created()
    
    def render(self, indent=0):
        """Шаблонний метод для рендерингу"""
        self.before_render()
        result = self._do_render(indent)
        self.after_render()
        return result
    
    @abstractmethod
    def _do_render(self, indent=0):
        """Конкретна реалізація рендерингу"""
        pass
    
    def before_render(self):
        """Хук перед рендерингом"""
        pass
    
    def after_render(self):
        """Хук після рендерингу"""
        pass
    
    def on_created(self):
        """Хук створення елемента"""
        self._notify_lifecycle(LifecycleEvent.CREATED)
    
    def on_inserted(self, parent):
        """Хук вставки елемента"""
        self.parent = parent
        self._notify_lifecycle(LifecycleEvent.INSERTED)
    
    def on_removed(self):
        """Хук видалення елемента"""
        self.parent = None
        self._notify_lifecycle(LifecycleEvent.REMOVED)
    
    def on_styles_applied(self):
        """Хук застосування стилів"""
        self._notify_lifecycle(LifecycleEvent.STYLES_APPLIED)
    
    def on_classlist_applied(self):
        """Хук застосування класів"""
        self._notify_lifecycle(LifecycleEvent.CLASSLIST_APPLIED)
    
    def _notify_lifecycle(self, event: LifecycleEvent):
        """Сповіщення про подію життєвого циклу"""
        print(f"Подія життєвого циклу: {event.name}")
