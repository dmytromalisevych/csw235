from abc import ABC, abstractmethod
from typing import List, Optional

class Command(ABC):
    """Базовий інтерфейс команди"""
    
    @abstractmethod
    def execute(self) -> bool:
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        pass

class AddNodeCommand(Command):
    """Команда додавання вузла"""
    
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        self.index: Optional[int] = None
    
    def execute(self) -> bool:
        if self.child not in self.parent.children:
            self.parent.children.append(self.child)
            self.index = len(self.parent.children) - 1
            self.child.on_inserted(self.parent)
            return True
        return False
    
    def undo(self) -> bool:
        if self.index is not None:
            self.parent.children.pop(self.index)
            self.child.on_removed()
            return True
        return False

class RemoveNodeCommand(Command):
    """Команда видалення вузла"""
    
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        self.index: Optional[int] = None
    
    def execute(self) -> bool:
        if self.child in self.parent.children:
            self.index = self.parent.children.index(self.child)
            self.parent.children.remove(self.child)
            self.child.on_removed()
            return True
        return False
    
    def undo(self) -> bool:
        if self.index is not None:
            self.parent.children.insert(self.index, self.child)
            self.child.on_inserted(self.parent)
            return True
        return False

class CommandHistory:
    """Менеджер історії команд"""
    
    def __init__(self):
        self.commands: List[Command] = []
        self.current = -1
    
    def execute(self, command: Command):
        """Виконати нову команду"""
        if command.execute():
            self.current += 1
            self.commands[self.current:] = [command]
    
    def undo(self) -> bool:
        """Скасувати останню команду"""
        if self.current >= 0:
            result = self.commands[self.current].undo()
            if result:
                self.current -= 1
            return result
        return False
    
    def redo(self) -> bool:
        """Повторити скасовану команду"""
        if self.current + 1 < len(self.commands):
            self.current += 1
            return self.commands[self.current].execute()
        return False

class CommandableLightNode:
    """Мікшин для додавання підтримки команд"""
    
    def __init__(self):
        self.command_history = CommandHistory()
    
    def execute_command(self, command: Command):
        self.command_history.execute(command)
    
    def undo_last(self) -> bool:
        return self.command_history.undo()
    
    def redo_last(self) -> bool:
        return self.command_history.redo()
