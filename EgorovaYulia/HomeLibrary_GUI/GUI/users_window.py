from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QDialog, QFormLayout, QLineEdit,
                             QCheckBox, QLabel)
from PyQt6.QtCore import Qt  # <-- ДОБАВЬТЕ ЭТУ СТРОЧКУ!
from PyQt6.QtGui import QIcon
import hashlib
from database import Database
from config import Config


class UsersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()

        # Панель инструментов
        toolbar = QHBoxLayout()

        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.clicked.connect(self.refresh_data)

        self.add_btn = QPushButton("Добавить пользователя")
        self.add_btn.clicked.connect(self.add_user)

        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self.edit_user)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_user)

        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.edit_btn)
        toolbar.addWidget(self.delete_btn)
        toolbar.addStretch()

        # Таблица с пользователями
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Логин", "ФИО", "Email", "Телефон",
            "Администратор", "Дата регистрации", "Активность"
        ])

        # Настройка таблицы
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Сборка интерфейса
        layout.addLayout(toolbar)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.refresh_data()

    def refresh_data(self):
        """Обновление данных в таблице"""
        query = "SELECT * FROM users ORDER BY id"
        users = self.db.execute_query(query, fetchall=True)
        self.table.setRowCount(len(users))

        for row, user in enumerate(users):
            items = [
                str(user['id']),
                user['username'],
                user['full_name'],
                user['email'] or '',
                user['phone'] or '',
                "Да" if user['is_admin'] else "Нет",
                str(user['created_at']),
                "Активен"
            ]

            for col, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setData(Qt.ItemDataRole.UserRole, user['id'])

                # Подсветка администраторов
                if col == 5 and user['is_admin']:
                    item.setBackground(Qt.GlobalColor.cyan)

                self.table.setItem(row, col, item)

    def get_selected_user_id(self):
        """Получение ID выбранного пользователя"""
        selected = self.table.selectedItems()
        if selected:
            return selected[0].data(Qt.ItemDataRole.UserRole)
        return None

    def add_user(self):
        """Добавление нового пользователя"""
        dialog = UserDialog(self)
        if dialog.exec():
            data = dialog.get_data()

            # Хеширование пароля
            hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()

            result = self.db.add_user(
                data['username'], hashed_password, data['full_name'],
                data['email'], data['phone'], data['is_admin']
            )

            if result:
                QMessageBox.information(self, "Успех", "Пользователь добавлен успешно!")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить пользователя")

    def edit_user(self):
        """Редактирование пользователя"""
        user_id = self.get_selected_user_id()
        if not user_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для редактирования")
            return

        # Получение данных пользователя
        query = "SELECT * FROM users WHERE id = %s"
        user = self.db.execute_query(query, (user_id,), fetchone=True)

        if user:
            dialog = UserDialog(self, user)
            if dialog.exec():
                data = dialog.get_data()

                # Подготовка данных для обновления
                update_data = {
                    'username': data['username'],
                    'full_name': data['full_name'],
                    'email': data['email'] or None,
                    'phone': data['phone'] or None,
                    'is_admin': data['is_admin']
                }

                # Если пароль изменен
                if data['password']:
                    update_data['password'] = hashlib.sha256(data['password'].encode()).hexdigest()

                # Выполнение обновления
                set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
                query = f"UPDATE users SET {set_clause} WHERE id = %s"
                params = list(update_data.values()) + [user_id]

                result = self.db.execute_query(query, params)

                if result:
                    QMessageBox.information(self, "Успех", "Пользователь обновлен успешно!")
                    self.refresh_data()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось обновить пользователя")

    def delete_user(self):
        """Удаление пользователя"""
        user_id = self.get_selected_user_id()
        if not user_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления")
            return

        # Проверка, не является ли пользователь последним администратором
        query = "SELECT is_admin FROM users WHERE id = %s"
        user = self.db.execute_query(query, (user_id,), fetchone=True)

        if user and user['is_admin']:
            admin_count = self.get_admin_count()
            if admin_count <= 1:
                QMessageBox.warning(self, "Ошибка", "Нельзя удалить последнего администратора!")
                return

        reply = QMessageBox.question(self, 'Подтверждение',
                                     'Вы уверены, что хотите удалить этого пользователя?',
                                     QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM users WHERE id = %s"
            result = self.db.execute_query(query, (user_id,))

            if result:
                QMessageBox.information(self, "Успех", "Пользователь удален успешно!")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить пользователя")

    def get_total_users(self):
        """Получение общего количества пользователей"""
        return self.db.get_total_users_count()  # Используйте новый метод

    def get_admin_count(self):
        """Получение количества администраторов"""
        return self.db.get_admin_users_count()  # Используйте новый метод


class UserDialog(QDialog):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса диалога"""
        self.setWindowTitle("Добавить пользователя" if not self.user else "Редактировать пользователя")
        self.setModal(True)

        layout = QFormLayout()

        # Поля ввода
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.full_name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()

        self.is_admin_check = QCheckBox("Администратор")

        # Заполнение полей, если редактируем
        if self.user:
            self.username_input.setText(self.user['username'])
            self.full_name_input.setText(self.user['full_name'])
            self.email_input.setText(self.user['email'] or '')
            self.phone_input.setText(self.user['phone'] or '')
            self.is_admin_check.setChecked(self.user['is_admin'])

            # Для редактирования пароль не обязателен
            self.password_input.setPlaceholderText("Оставьте пустым, чтобы не менять")
            self.confirm_password_input.setPlaceholderText("Оставьте пустым, чтобы не менять")

        # Добавление полей в форму
        layout.addRow("Логин *:", self.username_input)
        layout.addRow("Пароль *:", self.password_input)
        layout.addRow("Подтверждение пароля *:", self.confirm_password_input)
        layout.addRow("ФИО *:", self.full_name_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Телефон:", self.phone_input)
        layout.addRow("", self.is_admin_check)

        # Кнопки
        buttons_layout = QHBoxLayout()
        ok_btn = QPushButton("Сохранить")
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)

        layout.addRow("", buttons_layout)

        self.setLayout(layout)
        self.setFixedSize(400, 350)

    def get_data(self):
        """Получение данных из формы"""
        return {
            'username': self.username_input.text().strip(),
            'password': self.password_input.text().strip(),
            'full_name': self.full_name_input.text().strip(),
            'email': self.email_input.text().strip() or None,
            'phone': self.phone_input.text().strip() or None,
            'is_admin': self.is_admin_check.isChecked()
        }

    def accept(self):
        """Проверка и принятие формы"""
        data = self.get_data()

        # Проверка обязательных полей
        if not data['username']:
            QMessageBox.warning(self, "Ошибка", "Введите логин")
            return

        if not data['full_name']:
            QMessageBox.warning(self, "Ошибка", "Введите ФИО")
            return

        # Проверка пароля (только для нового пользователя или если пароль изменен)
        if not self.user or data['password']:
            if not data['password']:
                QMessageBox.warning(self, "Ошибка", "Введите пароль")
                return

            if data['password'] != self.confirm_password_input.text().strip():
                QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
                return

        super().accept()
