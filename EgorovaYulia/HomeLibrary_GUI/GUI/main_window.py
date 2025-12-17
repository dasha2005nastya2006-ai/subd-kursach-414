from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QMessageBox,
                             QMenuBar, QMenu, QStatusBar, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QFont, QIcon
import os
from config import Config
from .books_window import BooksWindow
from .loans_window import LoansWindow
from .users_window import UsersWindow
from .reports_window import ReportsWindow


class MainWindow(QMainWindow):
    def __init__(self, user_id, username, is_admin):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.is_admin = is_admin
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle(f"{Config.APP_TITLE} - {self.username}")
        self.setGeometry(100, 100, *Config.MAIN_WINDOW_SIZE)

        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QVBoxLayout(central_widget)

        # Заголовок
        header_layout = QHBoxLayout()
        title_label = QLabel(Config.APP_TITLE)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {Config.PRIMARY_COLOR}; padding: 10px;")

        user_label = QLabel(f"Пользователь: {self.username}")
        user_label.setStyleSheet(f"color: {Config.SECONDARY_COLOR}; padding: 10px;")

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(user_label)

        # Создание меню
        self.create_menu_bar()

        # Виджет с переключаемыми окнами
        self.stacked_widget = QStackedWidget()

        # Создание окон
        self.books_window = BooksWindow(self.is_admin)
        self.loans_window = LoansWindow(self.is_admin)
        self.users_window = UsersWindow()
        self.reports_window = ReportsWindow()

        # Добавление окон в stacked widget
        self.stacked_widget.addWidget(self.create_dashboard())
        self.stacked_widget.addWidget(self.books_window)
        self.stacked_widget.addWidget(self.loans_window)
        self.stacked_widget.addWidget(self.users_window)
        self.stacked_widget.addWidget(self.reports_window)

        # Панель навигации
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("📊 Дашборд", 0),
            ("📚 Книги", 1),
            ("📖 Выдачи", 2),
            ("👥 Пользователи", 3),
            ("📈 Отчеты", 4)
        ]

        self.nav_buttons = []
        for text, index in nav_buttons:
            if index == 3 and not self.is_admin:  # Пользователи только для админов
                continue

            btn = QPushButton(text)
            btn.setFixedHeight(40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Config.PRIMARY_COLOR};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    padding: 0 20px;
                }}
                QPushButton:hover {{
                    background-color: {Config.SECONDARY_COLOR};
                }}
                QPushButton:checked {{
                    background-color: {Config.ACCENT_COLOR};
                }}
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=index: self.switch_window(idx))
            nav_layout.addWidget(btn)
            self.nav_buttons.append((btn, index))

        nav_layout.addStretch()

        # Кнопка выхода
        logout_btn = QPushButton("Выход")
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Config.WARNING_COLOR};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
            }}
        """)
        nav_layout.addWidget(logout_btn)

        # Сборка интерфейса
        main_layout.addLayout(header_layout)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.stacked_widget)

        # Статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Добро пожаловать, {self.username}!")

        # Активация первого окна
        self.switch_window(0)

    def create_menu_bar(self):
        """Создание меню"""
        menu_bar = self.menuBar()

        # Меню Файл
        file_menu = menu_bar.addMenu("Файл")

        export_action = QAction("Экспорт данных", self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Справка
        help_menu = menu_bar.addMenu("Справка")

        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_dashboard(self):
        """Создание дашборда"""
        dashboard = QWidget()
        layout = QGridLayout(dashboard)
        layout.setSpacing(20)

        # Статистические карточки
        stats = [
            ("Всего книг", "📚", Config.PRIMARY_COLOR, self.books_window.get_total_books),
            ("Доступно книг", "✅", Config.SUCCESS_COLOR, self.books_window.get_available_books),
            ("Активные выдачи", "📖", Config.SECONDARY_COLOR, self.loans_window.get_active_loans_count),
            ("Просрочено", "⏰", Config.WARNING_COLOR, self.loans_window.get_overdue_loans_count),
            ("Всего пользователей", "👥", Config.ACCENT_COLOR, self.users_window.get_total_users),
            ("Администраторы", "👑", "#9b59b6", lambda: self.users_window.get_admin_count() if self.is_admin else "N/A")
        ]

        for i, (title, icon, color, func) in enumerate(stats):
            card = self.create_stat_card(title, icon, color, func)
            layout.addWidget(card, i // 3, i % 3)

        return dashboard

    def create_stat_card(self, title, icon, color, value_func):
        """Создание карточки статистики"""
        card = QWidget()
        card.setFixedHeight(120)
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)

        layout = QVBoxLayout(card)

        # Заголовок
        title_label = QLabel(f"{icon} {title}")
        title_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {color};
        """)

        # Значение
        value_label = QLabel()
        value_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        """)

        # Обновление значения
        def update_value():
            try:
                value = value_func()
                value_label.setText(str(value))
            except:
                value_label.setText("N/A")

        update_value()

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        return card

    def switch_window(self, index):
        """Переключение между окнами"""
        self.stacked_widget.setCurrentIndex(index)

        # Обновление состояния кнопок навигации
        for btn, btn_index in self.nav_buttons:
            btn.setChecked(btn_index == index)

        # Обновление данных в текущем окне
        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, 'refresh_data'):
            current_widget.refresh_data()

    def logout(self):
        """Выход из системы"""
        reply = QMessageBox.question(self, 'Подтверждение',
                                     'Вы уверены, что хотите выйти?',
                                     QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.close()

    def export_data(self):
        """Экспорт данных"""
        QMessageBox.information(self, "Экспорт", "Функция экспорта в разработке")

    def show_about(self):
        """Показать информацию о программе"""
        about_text = f"""
        <h2>{Config.APP_TITLE}</h2>
        <p>Версия: {Config.APP_VERSION}</p>
        <p>Система управления домашней библиотекой</p>
        <p>Разработано на PyQt6 и PostgreSQL</p>
        <hr>
        <p><small>© 2024 Домашняя библиотека</small></p>
        """
        QMessageBox.about(self, "О программе", about_text)
