from light_node import (
    DisplayType, 
    ClosureType,
    LightNode,
    LightElementNode, 
    LightTextNode,
    LifecycleEvent,
    LifecycleLightNode,
    HTMLValidator,
    StyleCollector,
    NodeMetricsCollector,
    AccessibilityChecker,
    VisibilityState,
    StatefulNode,
    TraversalType,
    IterableLightNode,
    AddNodeCommand,
    CommandableLightNode
)

class EnhancedLightNode(LightNode, StatefulNode, IterableLightNode,
                       CommandableLightNode, LifecycleLightNode):
    """Розширений базовий клас з підтримкою всіх функцій"""
    def __init__(self):
        LightNode.__init__(self)
        StatefulNode.__init__(self)
        IterableLightNode.__init__(self)
        CommandableLightNode.__init__(self)
        LifecycleLightNode.__init__(self)

class EnhancedElementNode(LightElementNode, EnhancedLightNode):  
    """Розширений клас елемента з підтримкою всіх функцій"""
    def __init__(self, tag_name: str, display_type=DisplayType.BLOCK,
                 closure_type=ClosureType.PAIRED):
        LightElementNode.__init__(self, tag_name, display_type, closure_type)
        EnhancedLightNode.__init__(self)
        
    def _do_render(self, indent=0) -> str:
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

class EnhancedTextNode(LightTextNode, EnhancedLightNode): 
    """Розширений клас текстового вузла з підтримкою всіх функцій"""
    def __init__(self, text: str):
        LightTextNode.__init__(self, text)
        EnhancedLightNode.__init__(self)

    def _do_render(self, indent=0) -> str:
        indentation = " " * indent
        return f"{indentation}{self.text}"

def create_element(tag, *args, display=DisplayType.BLOCK, closure=ClosureType.PAIRED):
    """Створює елемент з можливими дочірніми елементами"""
    element = EnhancedElementNode(tag, display, closure)
    for arg in args:
        if isinstance(arg, str):
            element.add_child(EnhancedTextNode(arg))
        elif isinstance(arg, LightNode):
            element.add_child(arg)
    return element

def main():
    """
    Головна функція для демонстрації всіх можливостей системи
    Автор: dmytromalisevych
    Дата створення: 2025-05-12 17:54:46
    """
    table = create_element("table")
    table.add_class("styled-table")

    header = create_element("tr")
    header.add_child(create_element("th", "Назва"))
    header.add_child(create_element("th", "Опис"))
    
    table.add_child(header)

    row = create_element("tr")
    row.add_child(create_element("td", "Visitor"))
    row.add_child(create_element("td", "Патерн для обходу структури"))
    
    add_command = AddNodeCommand(table, row)
    table.execute_command(add_command)

    validator = HTMLValidator()
    table.accept(validator)
    print("Помилки валідації:", validator.errors)

    metrics = NodeMetricsCollector()
    table.accept(metrics)
    print(f"\nМетрики:")
    print(f"Елементів: {metrics.element_count}")
    print(f"Текстових вузлів: {metrics.text_nodes_count}")
    print(f"Максимальна глибина: {metrics.max_depth}")

    collector = StyleCollector()
    table.accept(collector)
    print("\nВикористання класів:", collector.class_usage)

    checker = AccessibilityChecker()
    table.accept(checker)
    print("\nПроблеми доступності:", checker.warnings)

    print("\nЗвичайний рендеринг:")
    print(table.render())

    print("\nЗгорнутий стан:")
    table.set_visibility(VisibilityState.COLLAPSED)
    print(table.render())

    print("\nПрихований стан:")
    table.set_visibility(VisibilityState.HIDDEN)
    print(table.render())

    print("\nОбхід в глибину:")
    for node in table.traverse(TraversalType.DEPTH_FIRST):
        if isinstance(node, EnhancedElementNode):
            print(f"Елемент: {node.tag_name}")
        else:
            print(f"Текст: {node.text}")

    print("\nОбхід в ширину:")
    for node in table.traverse(TraversalType.BREADTH_FIRST):
        if isinstance(node, EnhancedElementNode):
            print(f"Елемент: {node.tag_name}")
        else:
            print(f"Текст: {node.text}")

if __name__ == "__main__":
    main()