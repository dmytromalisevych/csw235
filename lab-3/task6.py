import os
import sys
import gc
import requests
from abc import ABC, abstractmethod
from enum import Enum, auto
import time

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

class ElementType:
    def __init__(self, tag_name, display_type, closure_type):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closure_type = closure_type

class ElementTypeFactory:
    def __init__(self):
        self._element_types = {}
    
    def get_element_type(self, tag_name, display_type=DisplayType.BLOCK, 
                         closure_type=ClosureType.PAIRED):
        key = (tag_name, display_type, closure_type)
        
        if key not in self._element_types:
            self._element_types[key] = ElementType(tag_name, display_type, closure_type)
        
        return self._element_types[key]

class LightElementNodeFlyweight(LightNode):
    def __init__(self, element_type):
        self.element_type = element_type 
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
        result = f"<{self.element_type.tag_name}"
        
        if self.css_classes:
            class_str = " ".join(self.css_classes)
            result += f' class="{class_str}"'
        
        if self.element_type.closure_type == ClosureType.SELF_CLOSING:
            result += "/>"
        else:
            result += ">"
        
        return result
    
    def _close_tag(self):
        """Повертає закриваючий тег, якщо він потрібен"""
        if self.element_type.closure_type == ClosureType.PAIRED:
            return f"</{self.element_type.tag_name}>"
        return ""
    
    def render(self, indent=0):
        """Рендерить HTML з відступами для красивого форматування"""
        result = []
        indentation = " " * indent
        
        result.append(indentation + self._open_tag())

        if self.element_type.closure_type == ClosureType.PAIRED:
            child_indent = indent + 2
            for child in self.children:
                result.append(child.render(child_indent))

            result.append(indentation + self._close_tag())
        
        return "\n".join(result)
    
    @property
    def outer_html(self):
        """Повертає зовнішній HTML (весь елемент)"""
        if self.element_type.closure_type == ClosureType.SELF_CLOSING:
            return self._open_tag()
        
        inner = "".join(child.outer_html for child in self.children)
        return f"{self._open_tag()}{inner}{self._close_tag()}"
    
    @property
    def inner_html(self):
        """Повертає внутрішній HTML (тільки вміст)"""
        return "".join(child.outer_html for child in self.children)

def get_size(obj, seen=None):
    """Рекурсивно знаходить розмір об'єкта в байтах"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    
    if isinstance(obj, dict):
        size += sum(get_size(k, seen) + get_size(v, seen) for k, v in obj.items())
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum(get_size(i, seen) for i in obj)
    
    return size

def parse_text_to_html(text_lines):
    root = LightElementNode("div").add_class("container")
    
    if text_lines:
        h1 = LightElementNode("h1")
        h1.add_text(text_lines[0])
        root.add_child(h1)
    
    for line in text_lines[1:]:
        if not line.strip():  
            continue
            
        if len(line) < 20:
            element = LightElementNode("h2")
        elif line[0].isspace():
            element = LightElementNode("blockquote")
        else:
            element = LightElementNode("p")
        
        element.add_text(line.strip())
        root.add_child(element)
    
    return root

def parse_text_to_html_flyweight(text_lines, factory):
    container_type = factory.get_element_type("div")
    h1_type = factory.get_element_type("h1")
    h2_type = factory.get_element_type("h2")
    blockquote_type = factory.get_element_type("blockquote")
    p_type = factory.get_element_type("p")
    
    root = LightElementNodeFlyweight(container_type).add_class("container")
    
    if text_lines:
        h1 = LightElementNodeFlyweight(h1_type)
        h1.add_text(text_lines[0])
        root.add_child(h1)
    
    for line in text_lines[1:]:
        if not line.strip():  
            continue
            
        if len(line) < 20:
            element = LightElementNodeFlyweight(h2_type)
        elif line[0].isspace():
            element = LightElementNodeFlyweight(blockquote_type)
        else:
            element = LightElementNodeFlyweight(p_type)
        
        element.add_text(line.strip())
        root.add_child(element)
    
    return root

def download_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Помилка при завантаженні тексту: {e}")
        return None

def main():
    book_url = "https://www.gutenberg.org/cache/epub/1513/pg1513.txt"
    
    print(f"Завантаження тексту з {book_url}...")
    book_text = download_text(book_url)
    
    if not book_text:
        print("Не вдалося завантажити текст. Перевірте URL або підключення до Інтернету.")
        return
    
    text_lines = book_text.splitlines()
    
    print(f"Успішно завантажено текст. Кількість рядків: {len(text_lines)}")
    
    start_idx = 0
    end_idx = len(text_lines)
    
    for i, line in enumerate(text_lines):
        if "START OF THE PROJECT GUTENBERG EBOOK" in line:
            start_idx = i + 1
            break
    
    for i, line in enumerate(text_lines[start_idx:], start_idx):
        if "END OF THE PROJECT GUTENBERG EBOOK" in line:
            end_idx = i
            break
    
    text_lines = text_lines[start_idx:end_idx]
    
    print(f"Відфільтровано метадані. Кількість рядків основного тексту: {len(text_lines)}")
    
    print("\n=== Без використання шаблону Легковаговик ===")
    
    gc.collect()
    
    start_time = time.time()
    
    html_tree = parse_text_to_html(text_lines)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    tree_size = get_size(html_tree)
    print(f"Розмір дерева HTML в пам'яті: {tree_size:,} байт")
    print(f"Середній розмір на елемент: {tree_size / (len(text_lines))} байт")
    print(f"Час виконання: {execution_time:.2f} секунд")
    
    print("\n=== З використанням шаблону Легковаговик ===")
    
    gc.collect()
    
    factory = ElementTypeFactory()
    
    start_time = time.time()
    
    html_tree_flyweight = parse_text_to_html_flyweight(text_lines, factory)
    
    end_time = time.time()
    execution_time_flyweight = end_time - start_time
    
    tree_size_flyweight = get_size(html_tree_flyweight)
    print(f"Розмір дерева HTML з легковаговиком в пам'яті: {tree_size_flyweight:,} байт")
    print(f"Середній розмір на елемент: {tree_size_flyweight / (len(text_lines))} байт")
    print(f"Час виконання: {execution_time_flyweight:.2f} секунд")
    
    reduction = (1 - tree_size_flyweight / tree_size) * 100
    print(f"Зменшення розміру: {reduction:.2f}%")
    
    print(f"Кількість унікальних типів елементів: {len(factory._element_types)}")
    
    print("\n=== Приклад HTML-розмітки (перші 10 елементів) ===")
    for i, child in enumerate(html_tree_flyweight.children[:10]):
        if i == 0:
            print(f"<h1>{child.inner_html}</h1>")
        else:
            tag_name = child.element_type.tag_name
            print(f"<{tag_name}>{child.inner_html}</{tag_name}>")
    
    output_file = "romeo_and_juliet.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang='en'>\n")
        f.write("<head>\n")
        f.write("  <meta charset='UTF-8'>\n")
        f.write("  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
        f.write("  <title>Romeo and Juliet - Rendered with LightHTML</title>\n")
        f.write("  <style>\n")
        f.write("    body { font-family: 'Georgia', serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }\n")
        f.write("    h1 { text-align: center; color: #333; margin-bottom: 30px; }\n")
        f.write("    h2 { color: #555; margin-top: 30px; }\n")
        f.write("    blockquote { font-style: italic; border-left: 3px solid #ccc; padding-left: 15px; margin-left: 0; }\n")
        f.write("    p { text-align: justify; }\n")
        f.write("    .container { padding: 20px; }\n")
        f.write("  </style>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        
        f.write(html_tree_flyweight.render())
        
        f.write("\n</body>\n")
        f.write("</html>")
    
    print(f"\nHTML-розмітка збережена у файл: {output_file}")

if __name__ == "__main__":
    main()