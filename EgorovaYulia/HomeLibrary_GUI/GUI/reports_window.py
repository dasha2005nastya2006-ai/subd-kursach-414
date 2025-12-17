from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QComboBox, QDateEdit, QLabel, QGroupBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox)
from PyQt6.QtCore import Qt, QDate  # <-- Убедитесь, что Qt импортирован
from database import Database
from config import Config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os


class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()

        # Панель управления отчетами
        control_group = QGroupBox("Параметры отчета")
        control_layout = QVBoxLayout()

        # Выбор типа отчета
        report_type_layout = QHBoxLayout()
        report_type_layout.addWidget(QLabel("Тип отчета:"))

        self.report_type_combo = QComboBox()
        self.report_type_combo.addItems([
            "Статистика библиотеки",
            "Активные выдачи",
            "Просроченные книги",
            "Популярные книги",
            "Читательская активность"
        ])
        self.report_type_combo.currentIndexChanged.connect(self.update_report_params)

        report_type_layout.addWidget(self.report_type_combo)
        report_type_layout.addStretch()

        # Параметры даты
        self.date_params_group = QGroupBox("Период")
        date_layout = QHBoxLayout()

        date_layout.addWidget(QLabel("С:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)

        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("По:"))

        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)

        date_layout.addWidget(self.end_date)
        date_layout.addStretch()

        self.date_params_group.setLayout(date_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.generate_btn = QPushButton("Сгенерировать отчет")
        self.generate_btn.clicked.connect(self.generate_report)

        self.export_btn = QPushButton("Экспорт в PDF")
        self.export_btn.clicked.connect(self.export_to_pdf)

        buttons_layout.addWidget(self.generate_btn)
        buttons_layout.addWidget(self.export_btn)
        buttons_layout.addStretch()

        # Сборка панели управления
        control_layout.addLayout(report_type_layout)
        control_layout.addWidget(self.date_params_group)
        control_layout.addLayout(buttons_layout)
        control_group.setLayout(control_layout)

        # Таблица с результатами
        self.table = QTableWidget()
        self.table.setColumnCount(5)

        # Сборка интерфейса
        layout.addWidget(control_group)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.update_report_params()

    def update_report_params(self):
        """Обновление параметров отчета"""
        report_type = self.report_type_combo.currentText()

        # Показываем/скрываем параметры даты в зависимости от типа отчета
        if report_type in ["Активные выдачи", "Просроченные книги",
                           "Популярные книги", "Читательская активность"]:
            self.date_params_group.show()
        else:
            self.date_params_group.hide()

    def generate_report(self):
        """Генерация отчета"""
        report_type = self.report_type_combo.currentText()

        if report_type == "Статистика библиотеки":
            self.generate_library_stats()
        elif report_type == "Активные выдачи":
            self.generate_active_loans_report()
        elif report_type == "Просроченные книги":
            self.generate_overdue_books_report()
        elif report_type == "Популярные книги":
            self.generate_popular_books_report()
        elif report_type == "Читательская активность":
            self.generate_reader_activity_report()

    def generate_library_stats(self):
        """Генерация статистики библиотеки"""
        # Общая статистика
        total_books = self.db.execute_query(
            "SELECT COUNT(*) as count FROM books", fetchone=True
        )['count']

        total_available = self.db.execute_query(
            "SELECT SUM(available) as total FROM books", fetchone=True
        )['total'] or 0

        total_loans = self.db.execute_query(
            "SELECT COUNT(*) as count FROM loans", fetchone=True
        )['count']

        active_loans = self.db.execute_query(
            "SELECT COUNT(*) as count FROM loans WHERE status = 'active'", fetchone=True
        )['count']

        total_users = self.db.execute_query(
            "SELECT COUNT(*) as count FROM users", fetchone=True
        )['count']

        # Статистика по жанрам
        genre_stats = self.db.execute_query("""
            SELECT genre, COUNT(*) as count 
            FROM books 
            WHERE genre IS NOT NULL 
            GROUP BY genre 
            ORDER BY count DESC
        """, fetchall=True)

        # Настройка таблицы
        self.table.setRowCount(6 + len(genre_stats))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Показатель", "Значение"])

        # Заполнение общей статистики
        stats = [
            ("Всего книг", str(total_books)),
            ("Доступно книг", str(total_available)),
            ("Всего выдач", str(total_loans)),
            ("Активные выдачи", str(active_loans)),
            ("Всего пользователей", str(total_users)),
            ("", "")
        ]

        for row, (label, value) in enumerate(stats):
            self.table.setItem(row, 0, QTableWidgetItem(label))
            self.table.setItem(row, 1, QTableWidgetItem(value))

        # Заполнение статистики по жанрам
        self.table.setItem(6, 0, QTableWidgetItem("Распределение по жанрам:"))
        self.table.setItem(6, 1, QTableWidgetItem(""))

        for i, stat in enumerate(genre_stats, 1):
            self.table.setItem(6 + i, 0, QTableWidgetItem(stat['genre']))
            self.table.setItem(6 + i, 1, QTableWidgetItem(str(stat['count'])))

        # Настройка ширины столбцов
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

    def generate_active_loans_report(self):
        """Генерация отчета по активным выдачам"""
        start_date = self.start_date.date().toString(Qt.DateFormat.ISODate)
        end_date = self.end_date.date().toString(Qt.DateFormat.ISODate)

        query = """
            SELECT l.id, b.title, b.author, u.full_name, 
                   l.loan_date, l.due_date, l.notes
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN users u ON l.user_id = u.id
            WHERE l.status = 'active' 
            AND l.loan_date BETWEEN %s AND %s
            ORDER BY l.due_date
        """

        loans = self.db.execute_query(query, (start_date, end_date), fetchall=True)

        # Настройка таблицы
        self.table.setRowCount(len(loans))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Книга", "Автор", "Читатель",
            "Дата выдачи", "Срок возврата", "Примечания"
        ])

        # Заполнение данных
        for row, loan in enumerate(loans):
            items = [
                str(loan['id']),
                loan['title'],
                loan['author'],
                loan['full_name'],
                str(loan['loan_date']),
                str(loan['due_date']),
                loan['notes'] or ''
            ]

            for col, text in enumerate(items):
                self.table.setItem(row, col, QTableWidgetItem(text))

        # Настройка ширины столбцов
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

    def generate_overdue_books_report(self):
        """Генерация отчета по просроченным книгам"""
        query = """
            SELECT l.id, b.title, b.author, u.full_name, 
                   l.loan_date, l.due_date, 
                   CURRENT_DATE - l.due_date as days_overdue
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN users u ON l.user_id = u.id
            WHERE l.status = 'active' 
            AND l.due_date < CURRENT_DATE
            ORDER BY l.due_date
        """

        loans = self.db.execute_query(query, fetchall=True)

        # Настройка таблицы
        self.table.setRowCount(len(loans))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Книга", "Автор", "Читатель",
            "Дата выдачи", "Срок возврата", "Дней просрочки"
        ])

        # Заполнение данных
        for row, loan in enumerate(loans):
            items = [
                str(loan['id']),
                loan['title'],
                loan['author'],
                loan['full_name'],
                str(loan['loan_date']),
                str(loan['due_date']),
                str(loan['days_overdue'])
            ]

            for col, text in enumerate(items):
                item = QTableWidgetItem(text)

                # Подсветка просрочки
                if col == 6:
                    days = int(loan['days_overdue'])
                    if days > 30:
                        item.setBackground(Qt.GlobalColor.red)
                        item.setForeground(Qt.GlobalColor.white)
                    elif days > 14:
                        item.setBackground(Qt.GlobalColor.yellow)

                self.table.setItem(row, col, item)

    def generate_popular_books_report(self):
        """Генерация отчета по популярным книгам"""
        start_date = self.start_date.date().toString(Qt.DateFormat.ISODate)
        end_date = self.end_date.date().toString(Qt.DateFormat.ISODate)

        query = """
            SELECT b.title, b.author, b.genre,
                   COUNT(l.id) as loan_count,
                   b.quantity, b.available
            FROM books b
            LEFT JOIN loans l ON b.id = l.book_id 
                AND l.loan_date BETWEEN %s AND %s
            GROUP BY b.id, b.title, b.author, b.genre, b.quantity, b.available
            ORDER BY loan_count DESC
            LIMIT 20
        """

        books = self.db.execute_query(query, (start_date, end_date), fetchall=True)

        # Настройка таблицы
        self.table.setRowCount(len(books))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Книга", "Автор", "Жанр", "Количество выдач",
            "Всего экземпляров", "Доступно"
        ])

        # Заполнение данных
        for row, book in enumerate(books):
            items = [
                book['title'],
                book['author'],
                book['genre'] or '',
                str(book['loan_count']),
                str(book['quantity']),
                str(book['available'])
            ]

            for col, text in enumerate(items):
                self.table.setItem(row, col, QTableWidgetItem(text))

    def generate_reader_activity_report(self):
        """Генерация отчета по читательской активности"""
        start_date = self.start_date.date().toString(Qt.DateFormat.ISODate)
        end_date = self.end_date.date().toString(Qt.DateFormat.ISODate)

        query = """
            SELECT u.full_name, u.email,
                   COUNT(l.id) as books_borrowed,
                   COUNT(CASE WHEN l.return_date IS NULL THEN 1 END) as active_loans,
                   MIN(l.loan_date) as first_loan,
                   MAX(l.loan_date) as last_loan
            FROM users u
            LEFT JOIN loans l ON u.id = l.user_id 
                AND l.loan_date BETWEEN %s AND %s
            GROUP BY u.id, u.full_name, u.email
            ORDER BY books_borrowed DESC
        """

        readers = self.db.execute_query(query, (start_date, end_date), fetchall=True)

        # Настройка таблицы
        self.table.setRowCount(len(readers))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Читатель", "Email", "Книг взято",
            "Активных выдач", "Первая выдача", "Последняя выдача"
        ])

        # Заполнение данных
        for row, reader in enumerate(readers):
            items = [
                reader['full_name'],
                reader['email'] or '',
                str(reader['books_borrowed']),
                str(reader['active_loans']),
                str(reader['first_loan']) if reader['first_loan'] else '',
                str(reader['last_loan']) if reader['last_loan'] else ''
            ]

            for col, text in enumerate(items):
                self.table.setItem(row, col, QTableWidgetItem(text))

    def export_to_pdf(self):
        """Экспорт отчета в PDF"""
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Ошибка", "Нет данных для экспорта")
            return

        # Создание PDF документа
        filename = f"library_report_{QDate.currentDate().toString(Qt.DateFormat.ISODate)}.pdf"

        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        # Стили
        styles = getSampleStyleSheet()

        # Заголовок
        report_type = self.report_type_combo.currentText()
        title = Paragraph(f"<b>{Config.APP_TITLE} - {report_type}</b>", styles['Title'])
        elements.append(title)

        # Дата генерации
        date = Paragraph(f"Дата генерации: {QDate.currentDate().toString('dd.MM.yyyy')}", styles['Normal'])
        elements.append(date)

        # Подготовка данных для таблицы
        data = []

        # Заголовки таблицы
        headers = []
        for col in range(self.table.columnCount()):
            headers.append(self.table.horizontalHeaderItem(col).text())
        data.append(headers)

        # Данные таблицы
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        # Создание таблицы в PDF
        table = Table(data)

        # Стили таблицы
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        table.setStyle(style)
        elements.append(table)

        # Генерация PDF
        try:
            doc.build(elements)
            QMessageBox.information(self, "Успех", f"Отчет сохранен в файл: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать PDF: {str(e)}")
