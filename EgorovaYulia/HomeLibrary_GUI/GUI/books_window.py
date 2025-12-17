from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QDialog, QFormLayout, QLineEdit,
                             QSpinBox, QTextEdit, QComboBox, QDateEdit, QLabel,
                             QInputDialog)
from PyQt6.QtCore import Qt, QDate  # <-- Убедитесь, что Qt импортирован
from database import Database
from config import Config


class BooksWindow(QWidget):
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

        self.add_btn = QPushButton("Добавить книгу")
        self.add_btn.clicked.connect(self.add_book)
        self.add_btn.setEnabled(self.is_admin)

        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self.edit_book)
        self.edit_btn.setEnabled(self.is_admin)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_book)
        self.delete_btn.setEnabled(self.is_admin)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию или автору...")
        self.search_input.textChanged.connect(self.search_books)

        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.edit_btn)
        toolbar.addWidget(self.delete_btn)
        toolbar.addStretch()
        toolbar.addWidget(QLabel("Поиск:"))
        toolbar.addWidget(self.search_input)

        # Таблица с книгами
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Название", "Автор", "ISBN", "Год", "Жанр",
            "Всего", "Доступно", "Местоположение", "Примечания"
        ])

        # Настройка таблицы
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
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
        books = self.db.get_all_books()
        self.table.setRowCount(len(books))

        for row, book in enumerate(books):
            items = [
                str(book['id']),
                book['title'],
                book['author'],
                book['isbn'] or '',
                str(book['year']) if book['year'] else '',
                book['genre'] or '',
                str(book['quantity']),
                str(book['available']),
                book['location'] or '',
                book['notes'] or ''
            ]

            for col, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setData(Qt.ItemDataRole.UserRole, book['id'])

                # Подсветка, если книг мало
                if col == 7 and book['available'] < 3:
                    item.setBackground(Qt.GlobalColor.yellow)

                self.table.setItem(row, col, item)

    def search_books(self):
        """Поиск книг"""
        search_text = self.search_input.text().lower()

        for row in range(self.table.rowCount()):
            title = self.table.item(row, 1).text().lower()
            author = self.table.item(row, 2).text().lower()

            if search_text in title or search_text in author:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def get_selected_book_id(self):
        """Получение ID выбранной книги"""
        selected = self.table.selectedItems()
        if selected:
            return selected[0].data(Qt.ItemDataRole.UserRole)
        return None

    def add_book(self):
        """Добавление новой книги"""
        dialog = BookDialog(self)
        if dialog.exec():
            data = dialog.get_data()

            result = self.db.add_book(
                data['title'], data['author'], data['isbn'],
                data['year'], data['genre'], data['publisher'],
                data['quantity'], data['location'], data['notes']
            )

            if result:
                QMessageBox.information(self, "Успех", "Книга добавлена успешно!")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить книгу")

    def edit_book(self):
        """Редактирование книги"""
        book_id = self.get_selected_book_id()
        if not book_id:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для редактирования")
            return

        # Получение данных книги
        query = "SELECT * FROM books WHERE id = %s"
        book = self.db.execute_query(query, (book_id,), fetchone=True)

        if book:
            dialog = BookDialog(self, book)
            if dialog.exec():
                data = dialog.get_data()

                result = self.db.update_book(book_id, **data)

                if result:
                    QMessageBox.information(self, "Успех", "Книга обновлена успешно!")
                    self.refresh_data()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось обновить книгу")

    def delete_book(self):
        """Удаление книги"""
        book_id = self.get_selected_book_id()
        if not book_id:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для удаления")
            return

        reply = QMessageBox.question(self, 'Подтверждение',
                                     'Вы уверены, что хотите удалить эту книгу?',
                                     QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            result = self.db.delete_book(book_id)

            if result:
                QMessageBox.information(self, "Успех", "Книга удалена успешно!")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить книгу")

    def get_total_books(self):
        """Получение общего количества книг"""
        return self.db.get_total_books_count()

    def get_available_books(self):
        """Получение количества доступных книг"""
        return self.db.get_available_books_count()


class BookDialog(QDialog):
    def __init__(self, parent=None, book=None):
        super().__init__(parent)
        self.book = book
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса диалога"""
        self.setWindowTitle("Добавить книгу" if not self.book else "Редактировать книгу")
        self.setModal(True)

        layout = QFormLayout()

        # Поля ввода
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.year_input = QSpinBox()
        self.year_input.setRange(1000, 2100)
        self.year_input.setSpecialValueText("Не указан")

        self.genre_input = QComboBox()
        self.genre_input.setEditable(True)
        self.genre_input.addItems([
            "Художественная литература", "Научная литература",
            "Фантастика", "Детектив", "Роман", "Поэзия",
            "Биография", "История", "Наука", "Техника"
        ])

        self.publisher_input = QLineEdit()
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 1000)
        self.quantity_input.setValue(1)

        self.location_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)

        # Заполнение полей, если редактируем
        if self.book:
            self.title_input.setText(self.book['title'])
            self.author_input.setText(self.book['author'])
            self.isbn_input.setText(self.book['isbn'] or '')
            self.year_input.setValue(self.book['year'] or 0)

            if self.book['genre']:
                self.genre_input.setCurrentText(self.book['genre'])

            self.publisher_input.setText(self.book['publisher'] or '')
            self.quantity_input.setValue(self.book['quantity'])
            self.location_input.setText(self.book['location'] or '')
            self.notes_input.setText(self.book['notes'] or '')

        # Добавление полей в форму
        layout.addRow("Название *:", self.title_input)
        layout.addRow("Автор *:", self.author_input)
        layout.addRow("ISBN:", self.isbn_input)
        layout.addRow("Год издания:", self.year_input)
        layout.addRow("Жанр:", self.genre_input)
        layout.addRow("Издательство:", self.publisher_input)
        layout.addRow("Количество:", self.quantity_input)
        layout.addRow("Местоположение:", self.location_input)
        layout.addRow("Примечания:", self.notes_input)

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
        self.setFixedSize(400, 500)

    def get_data(self):
        """Получение данных из формы"""
        return {
            'title': self.title_input.text().strip(),
            'author': self.author_input.text().strip(),
            'isbn': self.isbn_input.text().strip() or None,
            'year': self.year_input.value() or None,
            'genre': self.genre_input.currentText().strip() or None,
            'publisher': self.publisher_input.text().strip() or None,
            'quantity': self.quantity_input.value(),
            'location': self.location_input.text().strip() or None,
            'notes': self.notes_input.toPlainText().strip() or None
        }

    def accept(self):
        """Проверка и принятие формы"""
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название книги")
            return

        if not self.author_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите автора книги")
            return

        super().accept()
