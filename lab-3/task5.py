from abc import ABC, abstractmethod
from enum import Enum, auto
import urllib.request
import os

class DisplayType(Enum):
    BLOCK = auto()  
    INLINE = auto() 

class ClosureType(Enum):
    SELF_CLOSING = auto() 
    PAIRED = auto()   

class ImageLoadStrategy(ABC):
    @abstractmethod
    def load_image(self, source):
        pass

class FileSystemImageStrategy(ImageLoadStrategy):
    def load_image(self, source):
        if os.path.exists(source):
            return f"Зображення завантажено з файлової системи: {source}"
        else:
            return f"Помилка: Файл '{source}' не знайдено"

class NetworkImageStrategy(ImageLoadStrategy):
    def load_image(self, source):
        try:
            if source.startswith(('http://', 'https://', 'ftp://')):
                return f"Зображення завантажено з мережі: {source}"
            else:
                return f"Помилка: URL '{source}' має неправильний формат"
        except Exception as e:
            return f"Помилка при завантаженні зображення з мережі: {str(e)}"

class ImageStrategyFactory:
    @staticmethod
    def create_strategy(source):
        if source.startswith(('http://', 'https://', 'ftp://')):
            return NetworkImageStrategy()
        else:
            return FileSystemImageStrategy()

class LightNode(ABC):
    @abstractmethod
    def render(self, indent=0):
        pass
    
    @property
    @abstractmethod
    def outer_html(self):
        pass
    
    @property
    @abstractmethod
    def inner_html(self):
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
        self.attributes = {}
        self.event_listeners = {}
    
    def add_child(self, child):
        self.children.append(child)
        return self
    
    def add_class(self, css_class):
        self.css_classes.append(css_class)
        return self  
    
    def add_text(self, text):
        self.add_child(LightTextNode(text))
        return self
    
    def add_attribute(self, name, value):
        self.attributes[name] = value
        return self
    
    def add_event_listener(self, event_type, handler):
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(handler)
        return self
    
    def trigger_event(self, event_type, event_data=None):
        if event_type in self.event_listeners:
            for handler in self.event_listeners[event_type]:
                handler(self, event_data)
    
    @property
    def children_count(self):
        return len(self.children)
    
    def _open_tag(self):
        result = f"<{self.tag_name}"
        
        if self.css_classes:
            class_str = " ".join(self.css_classes)
            result += f' class="{class_str}"'

        for name, value in self.attributes.items():
            result += f' {name}="{value}"'
        
        for event_type, handlers in self.event_listeners.items():
            event_attr = f"on{event_type}"
            handlers_str = ";".join([f"handler{i}(event)" for i in range(len(handlers))])
            result += f' {event_attr}="{handlers_str}"'
        
        if self.closure_type == ClosureType.SELF_CLOSING:
            result += "/>"
        else:
            result += ">"
        
        return result
    
    def _close_tag(self):
        if self.closure_type == ClosureType.PAIRED:
            return f"</{self.tag_name}>"
        return ""
    
    def render(self, indent=0):
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
        if self.closure_type == ClosureType.SELF_CLOSING:
            return self._open_tag()
        
        inner = "".join(child.outer_html for child in self.children)
        return f"{self._open_tag()}{inner}{self._close_tag()}"
    
    @property
    def inner_html(self):
        return "".join(child.outer_html for child in self.children)

class LightImageNode(LightElementNode):
    def __init__(self, src, alt="", width=None, height=None):
        super().__init__("img", display_type=DisplayType.INLINE, closure_type=ClosureType.SELF_CLOSING)
        self.add_attribute("src", src)
        self.add_attribute("alt", alt)
        
        if width:
            self.add_attribute("width", width)
        if height:
            self.add_attribute("height", height)
        
        strategy = ImageStrategyFactory.create_strategy(src)
        self.load_result = strategy.load_image(src)
    
    def get_load_result(self):
        return self.load_result

def create_element(tag, *args, display=DisplayType.BLOCK, closure=ClosureType.PAIRED):
    element = LightElementNode(tag, display, closure)
    for arg in args:
        if isinstance(arg, str):
            element.add_text(arg)
        elif isinstance(arg, LightNode):
            element.add_child(arg)
    return element

def create_text(text):
    return LightTextNode(text)

def create_image(src, alt="", width=None, height=None):
    return LightImageNode(src, alt, width, height)

def main():
    print("=== Демонстрація EventListener ===")
    
    button = create_element("button", "Натисни мене")
    
    def click_handler(element, event):
        print(f"Кнопку '{element.inner_html}' було натиснуто!")
    
    def mouseover_handler(element, event):
        print(f"Курсор наведено на кнопку '{element.inner_html}'")
    
    button.add_event_listener("click", click_handler)
    button.add_event_listener("mouseover", mouseover_handler)
    
    print("\nHTML кнопки з подіями:")
    print(button.render())
    
    print("\nСимуляція подій:")
    button.trigger_event("mouseover")
    button.trigger_event("click")
    
    print("\n=== Демонстрація Image ===")
    
    local_image = create_image("example.jpg", "Локальне зображення", "300", "200")
    print("\nЗображення з файлової системи:")
    print(local_image.render())
    print(local_image.get_load_result())
    
    network_image = create_image("https://imgv3.fotor.com/images/blog-cover-image/a-shadow-of-a-boy-carrying-the-camera-with-red-sky-behind.jpg", "Мережеве зображення", "300", "200")
    print("\nЗображення з мережі:")
    print(network_image.render())
    print(network_image.get_load_result())

    print("\n=== Інтеграція подій із зображеннями ===")
    
    interactive_image = create_image("https://imgv3.fotor.com/images/blog-cover-image/a-shadow-of-a-boy-carrying-the-camera-with-red-sky-behind.jpg", "Інтерактивне зображення")
    
    def image_click_handler(element, event):
        print(f"Зображення '{element.attributes.get('alt')}' було натиснуто!")
    
    interactive_image.add_event_listener("click", image_click_handler)
    
    print("\nHTML інтерактивного зображення:")
    print(interactive_image.render())
    print("\nСимуляція натискання на зображення:")
    interactive_image.trigger_event("click")
    
    print("\n=== Демонстрація складної форми ===")
    
    form = create_element("form").add_class("contact-form")
    
    header = create_element("div").add_class("form-header")
    header.add_child(create_element("h2", "Контактна форма"))
    header.add_child(create_image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Facebook_Logo_%282019%29.png/1200px-Facebook_Logo_%282019%29.png", "Логотип", "100", "50"))
    
    form.add_child(header)
    
    name_div = create_element("div").add_class("form-group")
    name_div.add_child(create_element("label", "Ваше ім'я:"))
    name_input = create_element("input", display=DisplayType.INLINE, closure=ClosureType.SELF_CLOSING)
    name_input.add_attribute("type", "text")
    name_input.add_attribute("placeholder", "Введіть ваше ім'я")
    
    def input_focus_handler(element, event):
        print(f"Поле введення отримало фокус")
    
    name_input.add_event_listener("focus", input_focus_handler)
    name_div.add_child(name_input)
    
    email_div = create_element("div").add_class("form-group")
    email_div.add_child(create_element("label", "Email:"))
    email_div.add_child(
        create_element("input", display=DisplayType.INLINE, closure=ClosureType.SELF_CLOSING)
            .add_attribute("type", "email")
            .add_attribute("placeholder", "example@mail.com")
    )
    
    button_div = create_element("div").add_class("form-group")
    submit_button = create_element("button", "Відправити", display=DisplayType.INLINE)
    submit_button.add_class("btn").add_class("btn-primary")
    
    def submit_handler(element, event):
        print("Форму відправлено!")
    
    submit_button.add_event_listener("click", submit_handler)
    button_div.add_child(submit_button)
    
    form.add_child(name_div)
    form.add_child(email_div)
    form.add_child(button_div)
    
    print(form.render())
    print("\nСимуляція взаємодії з формою:")
    name_input.trigger_event("focus")
    submit_button.trigger_event("click")

if __name__ == "__main__":
    main()