from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QFormLayout,
                             QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import hashlib
from database import Database
from config import Config
import os


class AuthWindow(QWidget):
    login_successful = pyqtSignal(int, str, bool)  # user_id, username, is_admin

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle(f"{Config.APP_TITLE} - Авторизация")
        self.setFixedSize(*Config.LOGIN_WINDOW_SIZE)

        # Основной layout
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Заголовок
        title_label = QLabel(Config.APP_TITLE)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"color: {Config.PRIMARY_COLOR};")

        # Форма авторизации
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите имя пользователя")
        self.username_input.setMaximumWidth(250)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMaximumWidth(250)

        # Добавление полей в форму
        form_layout.addRow("Логин:", self.username_input)
        form_layout.addRow("Пароль:", self.password_input)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        self.login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {Config.SECONDARY_COLOR};
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """)

        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {Config.WARNING_COLOR};
                color: white;
                padding: 10px;
                border-radius: 5px;
            }}
        """)

        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.exit_button)

        # Сборка интерфейса
        form_frame.setLayout(form_layout)
        layout.addWidget(title_label)
        layout.addWidget(form_frame)
        layout.addLayout(buttons_layout)

        # Настройка Enter для входа
        self.username_input.returnPressed.connect(self.login)
        self.password_input.returnPressed.connect(self.login)

        self.setLayout(layout)

    def hash_password(self, password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        """Обработка входа"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        user = self.db.get_user_by_username(username)

        if user and user['password'] == self.hash_password(password):
            self.login_successful.emit(user['id'], user['username'], user['is_admin'])
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль!")
