import re
import os
from datetime import datetime

class TextReader:
    def read_file(self, file_path):
        pass

class SmartTextReader(TextReader):
    def read_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не знайдено!")
        
        result = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.rstrip('\n')
                    result.append(list(line))
            return result
        except Exception as e:
            raise RuntimeError(f"Помилка при читанні файлу {file_path}: {str(e)}")

class SmartTextChecker(TextReader):
    def __init__(self, text_reader):
        self._text_reader = text_reader
    
    def read_file(self, file_path):
        print(f"[{self._get_timestamp()}] Відкриття файлу: {file_path}")
        
        try:
            result = self._text_reader.read_file(file_path)
            
            line_count = len(result)
            char_count = sum(len(line) for line in result)
            
            print(f"[{self._get_timestamp()}] Файл успішно прочитано: {file_path}")
            print(f"[{self._get_timestamp()}] Статистика файлу: {line_count} рядків, {char_count} символів")
            
            return result
        except Exception as e:
            print(f"[{self._get_timestamp()}] Помилка при читанні файлу {file_path}: {str(e)}")
            raise
        finally:
            print(f"[{self._get_timestamp()}] Закриття файлу: {file_path}")
    
    def _get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class SmartTextReaderLocker(TextReader):
    def __init__(self, text_reader, pattern):
        self._text_reader = text_reader
        self._pattern = pattern
    
    def read_file(self, file_path):
        if re.search(self._pattern, file_path):
            print(f"Access denied! Доступ до файлу {file_path} заблоковано.")
            return None
        
        return self._text_reader.read_file(file_path)

def create_test_files():
    with open("test_file1.txt", "w", encoding="utf-8") as f:
        f.write("Це тестовий файл 1.\nВін має декілька рядків.\nПросто для тесту.")
    
    with open("test_file2.txt", "w", encoding="utf-8") as f:
        f.write("Це тестовий файл 2.\nВін містить конфіденційну інформацію.")
    
    with open("secret_data.txt", "w", encoding="utf-8") as f:
        f.write("КОНФІДЕНЦІЙНО!\nЦе секретні дані.\nНе читати!")

def print_array(array):
    if array is None:
        return
        
    print("Вміст файлу як двомірний масив:")
    for i, line in enumerate(array):
        print(f"Рядок {i+1}: {line}")
    print()

def main():
    create_test_files()
    
    reader = SmartTextReader()
    
    logger_proxy = SmartTextChecker(reader)
    
    access_control_proxy = SmartTextReaderLocker(logger_proxy, r"secret")
    
    print("=== Тест 1: Звичайний файл ===")
    result1 = access_control_proxy.read_file("test_file1.txt")
    print_array(result1)
    
    print("=== Тест 2: Інший звичайний файл ===")
    result2 = access_control_proxy.read_file("test_file2.txt")
    print_array(result2)
    
    print("=== Тест 3: Заблокований файл ===")
    result3 = access_control_proxy.read_file("secret_data.txt")
    print_array(result3)
    
    try:
        print("=== Тест 4: Неіснуючий файл ===")
        result4 = access_control_proxy.read_file("non_existent_file.txt")
        print_array(result4)
    except FileNotFoundError as e:
        print(f"Очікувана помилка: {e}")
    
    for file in ["test_file1.txt", "test_file2.txt", "secret_data.txt"]:
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    main()