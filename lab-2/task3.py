import threading

class Authenticator:
    _instance = None
    _lock = threading.Lock()
    _users = {"admin": "1234", "user": "password"}  
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    def authenticate(self, username, password):
        if username in self._users and self._users[username] == password:
            return f"Користувач {username} успішно автентифікований!"
        else:
            return "Помилка автентифікації: невірний логін або пароль."

def test_singleton():
    auth1 = Authenticator()
    auth2 = Authenticator()
    
    print("auth1 і auth2 є тим самим екземпляром:", auth1 is auth2)
    print(auth1.authenticate("admin", "1234"))
    print(auth2.authenticate("user", "password"))
    print(auth2.authenticate("guest", "1234"))  

if __name__ == "__main__":
    test_singleton()
