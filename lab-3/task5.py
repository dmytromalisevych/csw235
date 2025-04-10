from abc import ABC, abstractmethod
from enum import Enum, auto

class DisplayType(Enum):
    BLOCK = auto()  
    INLINE = auto() 

class ClosureType(Enum):
    SELF_CLOSING = auto() 
    PAIRED = auto()   

class LightNode(ABC):
    @abstractmethod
    def render(self, indent=0):
        """Відображає вузол з відступами"""
        pass
    
    @property
    @abstractmethod
    def outer_html(self):
        """Повертає зовнішній HTML вузла"""
        pass
    
    @property
    @abstractmethod
    def inner_html(self):
        """Повертає внутрішній HTML вузла"""
        pass

class LightTextNode(LightNode):
    def __init__(self, text):
        self.text = text
    
    def render(self, indent=0):
        return " " * indent + self.text
    
    @property
    def outer_html(self):
        return self.text
    
    @property
    def inner_html(self):
        return self.text

class LightElementNode(LightNode):
    def __init__(self, tag_name, display_type=DisplayType.BLOCK, 
                 closure_type=ClosureType.PAIRED):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closure_type = closure_type
        self.children = []
        self.css_classes = []
    
    def add_child(self, child):
        """Додає дочірній вузол"""
        self.children.append(child)
        return self
    
    def add_class(self, css_class):
        """Додає CSS клас"""
        self.css_classes.append(css_class)
        return self  
    
    def add_text(self, text):
        """Зручний метод для додавання текстового вузла"""
        self.add_child(LightTextNode(text))
        return self  
    
    @property
    def children_count(self):
        """Повертає кількість дочірніх елементів"""
        return len(self.children)
    
    def _open_tag(self):
        """Формує відкриваючий тег з атрибутами"""
        result = f"<{self.tag_name}"
        
        if self.css_classes:
            class_str = " ".join(self.css_classes)
            result += f' class="{class_str}"'
        
        if self.closure_type == ClosureType.SELF_CLOSING:
            result += "/>"
        else:
            result += ">"
        
        return result
    
    def _close_tag(self):
        """Повертає закриваючий тег, якщо він потрібен"""
        if self.closure_type == ClosureType.PAIRED:
            return f"</{self.tag_name}>"
        return ""
    
    def render(self, indent=0):
        """Рендерить HTML з відступами для красивого форматування"""
        result = []
        indentation = " " * indent
        
        result.append(indentation + self._open_tag())
        
        if self.closure_type == ClosureType.PAIRED:
            child_indent = indent + 2
            for child in self.children:
                result.append(child.render(child_indent))
            result.append(indentation + self._close_tag())
        
        return "\n".join(result)
    
    @property
    def outer_html(self):
        """Повертає зовнішній HTML (весь елемент)"""
        if self.closure_type == ClosureType.SELF_CLOSING:
            return self._open_tag()
        
        inner = "".join(child.outer_html for child in self.children)
        return f"{self._open_tag()}{inner}{self._close_tag()}"
    
    @property
    def inner_html(self):
        """Повертає внутрішній HTML (тільки вміст)"""
        return "".join(child.outer_html for child in self.children)

def create_element(tag, *args, display=DisplayType.BLOCK, closure=ClosureType.PAIRED):
    """Створює елемент з можливими дочірніми елементами"""
    element = LightElementNode(tag, display, closure)
    for arg in args:
        if isinstance(arg, str):
            element.add_text(arg)
        elif isinstance(arg, LightNode):
            element.add_child(arg)
    return element

def create_text(text):
    """Створює текстовий вузол"""
    return LightTextNode(text)

def main():
    caption = create_element("caption", "Навчальні курси з програмування")
    header_row = create_element("tr")
    header_row.add_child(create_element("th", "Назва курсу"))
    header_row.add_child(create_element("th", "Мова програмування"))
    header_row.add_child(create_element("th", "Тривалість (годин)"))
    header_row.add_child(create_element("th", "Рівень складності"))
    
    thead = create_element("thead").add_child(header_row)

    tbody = create_element("tbody")
    
    courses = [
        ["Основи програмування", "Python", "40", "Початковий"],
        ["Backend", "PHP", "60", "Середній"],
        ["Алгоритми та структури даних", "Java", "50", "Високий"],
    ]
    
    for course_data in courses:
        tr = create_element("tr")
        
        if course_data[3] == "Високий":
            tr.add_class("advanced-course")
        
        for item in course_data:
            tr.add_child(create_element("td", item, display=DisplayType.INLINE))
        
        tbody.add_child(tr)
    
    table = create_element("table").add_class("course-table").add_class("styled")
    table.add_child(caption)
    table.add_child(thead)
    table.add_child(tbody)
    
    print("=== Приклад використання LightHTML ===")
    print("\nРендеринг з відступами для зручності читання:")
    print(table.render())
    
    print("\nouterHTML таблиці:")
    print(table.outer_html)
    
    print("\ninnerHTML таблиці:")
    print(table.inner_html)
    
    print("\nКількість дочірніх елементів таблиці:", table.children_count)
    print("CSS класи таблиці:", table.css_classes)
    
    print("\n=== Приклад форми з різними типами елементів ===")
    
    form = create_element("form").add_class("contact-form")
    
    form.add_child(create_element("h2", "Контактна форма"))
    
    name_div = create_element("div").add_class("form-group")
    name_div.add_child(create_element("label", "Ваше ім'я:"))
    name_div.add_child(create_element("input", display=DisplayType.INLINE, closure=ClosureType.SELF_CLOSING))
    
    email_div = create_element("div").add_class("form-group")
    email_div.add_child(create_element("label", "Email:"))
    email_div.add_child(create_element("input", display=DisplayType.INLINE, closure=ClosureType.SELF_CLOSING))
    
    message_div = create_element("div").add_class("form-group")
    message_div.add_child(create_element("label", "Повідомлення:"))
    message_div.add_child(create_element("textarea", display=DisplayType.BLOCK, closure=ClosureType.PAIRED))
    
    button_div = create_element("div").add_class("form-group")
    button_div.add_child(
        create_element("button", "Відправити", display=DisplayType.INLINE)
            .add_class("btn")
            .add_class("btn-primary")
    )
    
    form.add_child(name_div)
    form.add_child(email_div)
    form.add_child(message_div)
    form.add_child(button_div)
    
    print(form.render())

if __name__ == "__main__":
    main()