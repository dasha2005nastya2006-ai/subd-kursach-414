from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QDialog, QFormLayout, QComboBox,
                             QDateEdit, QLabel, QGroupBox)
from PyQt6.QtCore import Qt, QDate  # <-- Убедитесь, что Qt импортирован
from database import Database
from config import Config


class LoansWindow(QWidget):
    def __init__(self, is_admin):
        super().__init__()
        self.db = Database()
        self.is_admin = is_admin
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()

        # Панель инструментов
        toolbar = QHBoxLayout()

        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.clicked.connect(self.refresh_data)

        self.new_loan_btn = QPushButton("Новая выдача")
        self.new_loan_btn.clicked.connect(self.create_loan)

        self.return_btn = QPushButton("Возврат книги")
        self.return_btn.clicked.connect(self.return_book)

        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.new_loan_btn)
        toolbar.addWidget(self.return_btn)
        toolbar.addStretch()

        # Таблица с выдачами
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Книга", "Автор", "Читатель", "Дата выдачи",
            "Срок возврата", "Дата возврата", "Статус", "Примечания"
        ])

        # Настройка таблицы
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Сборка интерфейса
        layout.addLayout(toolbar)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.refresh_data()

    def refresh_data(self):
        """Обновление данных в таблице"""
        loans = self.db.get_active_loans()
        self.table.setRowCount(len(loans))

        today = QDate.currentDate()

        for row, loan in enumerate(loans):
            due_date = QDate.fromString(str(loan['due_date']), Qt.DateFormat.ISODate)
            is_overdue = due_date < today

            items = [
                str(loan['id']),
                loan['title'],
                loan['author'],
                loan['full_name'],
                str(loan['loan_date']),
                str(loan['due_date']),
                str(loan['return_date']) if loan['return_date'] else '',
                loan['status'],
                loan['notes'] or ''
            ]

            for col, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setData(Qt.ItemDataRole.UserRole, loan['id'])

                # Подсветка просроченных выдач
                if col == 5 and is_overdue and loan['status'] == 'active':
                    item.setBackground(Qt.GlobalColor.red)
                    item.setForeground(Qt.GlobalColor.white)

                self.table.setItem(row, col, item)

    def get_selected_loan_id(self):
        """Получение ID выбранной выдачи"""
        selected = self.table.selectedItems()
        if selected:
            return selected[0].data(Qt.ItemDataRole.UserRole)
        return None

    def create_loan(self):
        """Создание новой выдачи"""
        dialog = LoanDialog(self)
        if dialog.exec():
            data = dialog.get_data()

            result = self.db.create_loan(
                data['book_id'], data['user_id'],
                data['due_date'], data['notes']
            )

            if result:
                QMessageBox.information(self, "Успех", "Книга выдана успешно!")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось выдать книгу")

    def return_book(self):
        """Возврат книги"""
        loan_id = self.get_selected_loan_id()
        if not loan_id:
            QMessageBox.warning(self, "Ошибка", "Выберите выдачу для возврата")
            return

        loan_status = self.table.item(self.table.currentRow(), 7).text()
        if loan_status != 'active':
            QMessageBox.warning(self, "Ошибка", "Эта книга уже возвращена")
            return

        reply = QMessageBox.question(self, 'Подтверждение',
                                     'Подтвердите возврат книги',
                                     QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            result = self.db.return_book(loan_id)

            if result:
                QMessageBox.information(self, "Успех", "Книга возвращена успешно!")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось вернуть книгу")

    def get_active_loans_count(self):
        """Получение количества активных выдач"""
        return self.db.get_active_loans_count()

    def get_overdue_loans_count(self):
        """Получение количества просроченных выдач"""
        return self.db.get_overdue_loans_count()


class LoanDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса диалога"""
        self.setWindowTitle("Новая выдача книги")
        self.setModal(True)

        layout = QFormLayout()

        # Получение списков книг и пользователей
        books = self.db.execute_query("SELECT id, title, author FROM books WHERE available > 0", fetchall=True)
        users = self.db.execute_query("SELECT id, full_name FROM users", fetchall=True)

        # Выпадающие списки
        self.book_combo = QComboBox()
        for book in books:
            self.book_combo.addItem(f"{book['title']} - {book['author']}", book['id'])

        self.user_combo = QComboBox()
        for user in users:
            self.user_combo.addItem(user['full_name'], user['id'])

        # Дата возврата (по умолчанию +14 дней)
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.currentDate().addDays(14))
        self.due_date_input.setCalendarPopup(True)

        # Примечания
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)

        # Добавление полей в форму
        layout.addRow("Книга *:", self.book_combo)
        layout.addRow("Читатель *:", self.user_combo)
        layout.addRow("Срок возврата *:", self.due_date_input)
        layout.addRow("Примечания:", self.notes_input)

        # Кнопки
        buttons_layout = QHBoxLayout()
        ok_btn = QPushButton("Выдать")
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)

        layout.addRow("", buttons_layout)

        self.setLayout(layout)
        self.setFixedSize(400, 300)

    def get_data(self):
        """Получение данных из формы"""
        return {
            'book_id': self.book_combo.currentData(),
            'user_id': self.user_combo.currentData(),
            'due_date': self.due_date_input.date().toString(Qt.DateFormat.ISODate),
            'notes': self.notes_input.toPlainText().strip() or None
        }

    def accept(self):
        """Проверка и принятие формы"""
        if self.book_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу")
            return

        if self.user_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите читателя")
            return

        super().accept()
