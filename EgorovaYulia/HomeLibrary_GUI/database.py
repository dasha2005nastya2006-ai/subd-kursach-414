import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from config import Config


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("Создание подключения к БД...")
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        """Инициализация соединения с БД"""
        print(f"\nПараметры подключения:")
        print(f"  host={Config.DB_HOST}")
        print(f"  port={Config.DB_PORT}")
        print(f"  dbname={Config.DB_NAME}")
        print(f"  user={Config.DB_USER}")

        try:
            self.conn = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            self.conn.autocommit = True
            print("✅ Подключение к PostgreSQL успешно!")

        except psycopg2.OperationalError as e:
            print(f"❌ Ошибка подключения: {e}")
            raise
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            raise

    @contextmanager
    def get_cursor(self):
        """Контекстный менеджер для работы с курсором"""
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            yield cursor
        finally:
            cursor.close()

    def execute_query(self, query, params=None, fetchone=False, fetchall=False):
        """Универсальный метод выполнения запросов"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            if fetchone:
                return cursor.fetchone()
            elif fetchall:
                return cursor.fetchall()
            return cursor.rowcount

    # ============ МЕТОДЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ============

    def get_user_by_username(self, username):
        """Получение пользователя по имени"""
        query = "SELECT * FROM users WHERE username = %s"
        return self.execute_query(query, (username,), fetchone=True)

    def add_user(self, username, password, full_name, email=None, phone=None, is_admin=False):
        """Добавление нового пользователя"""
        query = """
            INSERT INTO users (username, password, full_name, email, phone, is_admin)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        return self.execute_query(query, (username, password, full_name, email, phone, is_admin), fetchone=True)

    def get_all_users(self):
        """Получение всех пользователей"""
        query = "SELECT * FROM users ORDER BY id"
        return self.execute_query(query, fetchall=True)

    def update_user(self, user_id, **kwargs):
        """Обновление информации о пользователе"""
        if not kwargs:
            return 0

        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE users SET {set_clause} WHERE id = %s"
        params = list(kwargs.values()) + [user_id]

        return self.execute_query(query, params)

    def delete_user(self, user_id):
        """Удаление пользователя"""
        query = "DELETE FROM users WHERE id = %s"
        return self.execute_query(query, (user_id,))

    # ============ МЕТОДЫ ДЛЯ КНИГ ============

    def get_all_books(self):
        """Получение всех книг"""
        query = """
            SELECT b.*, 
                   (SELECT COUNT(*) FROM loans l WHERE l.book_id = b.id AND l.status = 'active') as borrowed_count
            FROM books b
            ORDER BY b.title
        """
        return self.execute_query(query, fetchall=True)

    def get_book_by_id(self, book_id):
        """Получение книги по ID"""
        query = "SELECT * FROM books WHERE id = %s"
        return self.execute_query(query, (book_id,), fetchone=True)

    def add_book(self, title, author, isbn=None, year=None, genre=None,
                 publisher=None, quantity=1, location=None, notes=None):
        """Добавление новой книги"""
        query = """
            INSERT INTO books (title, author, isbn, year, genre, publisher, quantity, available, location, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        available = quantity
        return self.execute_query(query, (title, author, isbn, year, genre, publisher,
                                          quantity, available, location, notes), fetchone=True)

    def update_book(self, book_id, **kwargs):
        """Обновление информации о книге"""
        if not kwargs:
            return 0

        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE books SET {set_clause} WHERE id = %s"
        params = list(kwargs.values()) + [book_id]

        return self.execute_query(query, params)

    def delete_book(self, book_id):
        """Удаление книги"""
        query = "DELETE FROM books WHERE id = %s"
        return self.execute_query(query, (book_id,))

    def search_books(self, search_term):
        """Поиск книг по названию или автору"""
        query = """
            SELECT * FROM books 
            WHERE LOWER(title) LIKE %s OR LOWER(author) LIKE %s
            ORDER BY title
        """
        search_pattern = f"%{search_term.lower()}%"
        return self.execute_query(query, (search_pattern, search_pattern), fetchall=True)

    # ============ МЕТОДЫ ДЛЯ ВЫДАЧ КНИГ ============

    def create_loan(self, book_id, user_id, due_date, notes=None):
        """Создание записи о выдаче книги"""
        # Проверяем доступность книги
        query = "SELECT available FROM books WHERE id = %s"
        book = self.execute_query(query, (book_id,), fetchone=True)

        if book and book['available'] > 0:
            # Уменьшаем количество доступных книг
            update_query = "UPDATE books SET available = available - 1 WHERE id = %s"
            self.execute_query(update_query, (book_id,))

            # Создаем запись о выдаче
            loan_query = """
                INSERT INTO loans (book_id, user_id, due_date, notes)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """
            return self.execute_query(loan_query, (book_id, user_id, due_date, notes), fetchone=True)
        return None

    def return_book(self, loan_id):
        """Возврат книги"""
        # Получаем информацию о выдаче
        query = "SELECT book_id FROM loans WHERE id = %s"
        loan = self.execute_query(query, (loan_id,), fetchone=True)

        if loan:
            # Увеличиваем количество доступных книг
            update_book = "UPDATE books SET available = available + 1 WHERE id = %s"
            self.execute_query(update_book, (loan['book_id'],))

            # Обновляем запись о выдаче
            update_loan = """
                UPDATE loans 
                SET return_date = CURRENT_DATE, status = 'returned' 
                WHERE id = %s
            """
            return self.execute_query(update_loan, (loan_id,))
        return 0

    def get_active_loans(self):
        """Получение активных выдач"""
        query = """
            SELECT l.*, b.title, b.author, u.full_name
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN users u ON l.user_id = u.id
            WHERE l.status = 'active'
            ORDER BY l.due_date
        """
        return self.execute_query(query, fetchall=True)

    def get_all_loans(self):
        """Получение всех выдач"""
        query = """
            SELECT l.*, b.title, b.author, u.full_name
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN users u ON l.user_id = u.id
            ORDER BY l.loan_date DESC
        """
        return self.execute_query(query, fetchall=True)

    def get_overdue_loans(self):
        """Получение просроченных выдач"""
        query = """
            SELECT l.*, b.title, b.author, u.full_name
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN users u ON l.user_id = u.id
            WHERE l.status = 'active' AND l.due_date < CURRENT_DATE
            ORDER BY l.due_date
        """
        return self.execute_query(query, fetchall=True)

    # ============ СТАТИСТИЧЕСКИЕ МЕТОДЫ ============

    def get_total_books_count(self):
        """Общее количество книг"""
        query = "SELECT COUNT(*) as count FROM books"
        result = self.execute_query(query, fetchone=True)
        return result['count'] if result else 0

    def get_available_books_count(self):
        """Количество доступных книг"""
        query = "SELECT SUM(available) as total FROM books"
        result = self.execute_query(query, fetchone=True)
        return result['total'] or 0

    def get_total_users_count(self):
        """Общее количество пользователей"""
        query = "SELECT COUNT(*) as count FROM users"
        result = self.execute_query(query, fetchone=True)
        return result['count'] if result else 0

    def get_admin_users_count(self):
        """Количество администраторов"""
        query = "SELECT COUNT(*) as count FROM users WHERE is_admin = TRUE"
        result = self.execute_query(query, fetchone=True)
        return result['count'] if result else 0

    def get_active_loans_count(self):
        """Количество активных выдач"""
        query = "SELECT COUNT(*) as count FROM loans WHERE status = 'active'"
        result = self.execute_query(query, fetchone=True)
        return result['count'] if result else 0

    def get_overdue_loans_count(self):
        """Количество просроченных выдач"""
        query = """
            SELECT COUNT(*) as count 
            FROM loans 
            WHERE status = 'active' AND due_date < CURRENT_DATE
        """
        result = self.execute_query(query, fetchone=True)
        return result['count'] if result else 0

    # ============ ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ============

    def get_available_books(self):
        """Получение доступных книг"""
        query = "SELECT * FROM books WHERE available > 0 ORDER BY title"
        return self.execute_query(query, fetchall=True)

    def get_users_for_loan(self):
        """Получение пользователей для выдачи (все кроме удаленных)"""
        query = "SELECT id, full_name FROM users ORDER BY full_name"
        return self.execute_query(query, fetchall=True)

    def close(self):
        """Закрытие соединения с БД"""
        if self.conn:
            self.conn.close()
