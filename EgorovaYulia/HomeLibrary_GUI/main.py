import sys
from PyQt6.QtWidgets import QApplication
from gui.auth_window import AuthWindow
from gui.main_window import MainWindow
from database import Database


class LibraryApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.db = Database()
        self.auth_window = None
        self.main_window = None

    def run(self):
        """Запуск приложения"""
        self.show_auth_window()
        sys.exit(self.app.exec())

    def show_auth_window(self):
        """Показать окно авторизации"""
        self.auth_window = AuthWindow()
        self.auth_window.login_successful.connect(self.on_login_successful)
        self.auth_window.show()

    def on_login_successful(self, user_id, username, is_admin):
        """Обработка успешной авторизации"""
        self.main_window = MainWindow(user_id, username, is_admin)
        self.main_window.show()

        # Закрытие окна авторизации
        if self.auth_window:
            self.auth_window.close()


def main():
    """Точка входа в приложение"""
    # Создание начального администратора (при первом запуске)
    db = Database()

    # Проверка наличия пользователей
    result = db.execute_query("SELECT COUNT(*) as count FROM users", fetchone=True)

    if result['count'] == 0:
        import hashlib
        print("Создание начального администратора...")
        print("Логин: admin")
        print("Пароль: admin123")

        hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
        db.add_user("admin", hashed_password, "Администратор", is_admin=True)

    # Запуск приложения
    app = LibraryApp()
    app.run()


if __name__ == "__main__":
    main()
