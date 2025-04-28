class TextDocument:
    
    def __init__(self, content=""):
        self._content = content
    
    def get_content(self):
        return self._content
    
    def set_content(self, content):
        self._content = content
    
    def __str__(self):
        return self._content


class DocumentMemento:
    
    def __init__(self, document):
        self._content = document.get_content()
    
    def get_saved_content(self):
        return self._content


class TextEditor:
    
    def __init__(self):
        self._document = TextDocument()
        self._history = [] 
        self._redo_stack = []  
    
    def write(self, text):
        self._save_state()
        current_content = self._document.get_content()
        self._document.set_content(current_content + text)
        self._redo_stack = []
    
    def replace_all(self, new_text):
        self._save_state()
        
        self._document.set_content(new_text)
        
        self._redo_stack = []
    
    def _save_state(self):
        memento = DocumentMemento(self._document)
        self._history.append(memento)
    
    def undo(self):
        """Скасовує останню зміну"""
        if not self._history:
            print("Немає змін для скасування")
            return False
        
        current_memento = DocumentMemento(self._document)
        self._redo_stack.append(current_memento)
        
        last_memento = self._history.pop()
        self._document.set_content(last_memento.get_saved_content())
        return True
    
    def redo(self):
        if not self._redo_stack:
            print("Немає змін для відновлення")
            return False
        
        current_memento = DocumentMemento(self._document)
        self._history.append(current_memento)
        
        redo_memento = self._redo_stack.pop()
        self._document.set_content(redo_memento.get_saved_content())
        return True
    
    def get_text(self):
        return self._document.get_content()


if __name__ == "__main__":
    editor = TextEditor()
    
    editor.write("Привіт, світ!")
    print(f"Після першого запису: '{editor.get_text()}'")
    
    editor.write(" Це тестовий документ.")
    print(f"Після другого запису: '{editor.get_text()}'")
    
    editor.undo()
    print(f"Після скасування: '{editor.get_text()}'")
    
    editor.redo()
    print(f"Після відновлення: '{editor.get_text()}'")
    
    editor.replace_all("Абсолютно новий текст!")
    print(f"Після заміни: '{editor.get_text()}'")
    
    editor.undo()
    print(f"Після скасування заміни: '{editor.get_text()}'")