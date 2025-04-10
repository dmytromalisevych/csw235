import sys
from colorama import init, Fore

init()

class Logger:
    def log(self, message):
        """Звичайне повідомлення - зелене"""
        print(f"{Fore.GREEN}{message}{Fore.RESET}")
    
    def error(self, message):
        """Повідомлення про помилку - червоне"""
        print(f"{Fore.RED}{message}{Fore.RESET}")
    
    def warn(self, message):
        """Повідомлення про попередження - жовте"""
        print(f"{Fore.YELLOW}{message}{Fore.RESET}")


class FileWriter:
    def __init__(self, filename):
        """Ініціалізація файлового запису"""
        self.filename = filename
        
    def write(self, text):
        """Запис тексту у файл"""
        with open(self.filename, 'a', encoding='utf-8') as file:
            file.write(text)
    
    def write_line(self, text):
        """Запис рядка з додаванням переносу"""
        self.write(text + '\n')


class FileLoggerAdapter(Logger):
    def __init__(self, filename="log.txt"):
        """Адаптер для перенаправлення логів у файл"""
        self.file_writer = FileWriter(filename)
        self.console_logger = Logger()
    
    def log(self, message):
        """Логування інформаційних повідомлень"""
        self.console_logger.log(message)
        self.file_writer.write_line(f"[INFO] {message}")
    
    def error(self, message):
        """Логування помилок"""
        self.console_logger.error(message)
        self.file_writer.write_line(f"[ERROR] {message}")
    
    def warn(self, message):
        """Логування попереджень"""
        self.console_logger.warn(message)
        self.file_writer.write_line(f"[WARNING] {message}")


def main():
    console_logger = Logger()
    console_logger.log("Звичайне повідомлення")
    console_logger.error("Помилка")
    console_logger.warn("Попередження")
    
    print("\n" + "-" * 50 + "\n")
    
    file_logger = FileLoggerAdapter("application_log.txt")
    file_logger.log("Вітаю тебе, користувачу!")
    file_logger.error("Ой, здається сталась помилка виконання операції")
    file_logger.warn("Увага! Закінчується пам'ять")
    
    print(f"\nПовідомлення також записані у файл 'application_log.txt'")


if __name__ == "__main__":
    main()