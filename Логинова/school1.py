import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2
from datetime import datetime
import hashlib

class SchoolDatabaseApp:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.current_user = None
        self.current_role = None
        
        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("Школьная информационная система")
        self.root.geometry("1000x700")
        
        # Настройка стилей
        self.setup_styles()
        
        # Показываем окно входа
        self.show_login_window()

        
    def setup_styles(self):
        """Настройка стилей для приложения"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Цвета
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }
        
    def connect_to_db(self):
        """Подключение к базе данных"""
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="school",
                user="school",
                password="1224"
            )
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных:\n{str(e)}")
            return False
    
    def show_login_window(self):
        """Окно входа в систему"""
        self.clear_window()
        
        # Создаем рамку для входа
        login_frame = ttk.Frame(self.root, padding="40")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Заголовок
        title_label = ttk.Label(login_frame, text="Школьная информационная система", 
                                font=("Arial", 20, "bold"), foreground=self.colors['primary'])
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Поле для логина
        ttk.Label(login_frame, text="Логин:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        self.login_entry = ttk.Entry(login_frame, width=30, font=("Arial", 12))
        self.login_entry.grid(row=1, column=1, pady=5, padx=10)
        self.login_entry.insert(0, "admin")  # Пример логина
        
        # Поле для пароля
        ttk.Label(login_frame, text="Пароль:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = ttk.Entry(login_frame, width=30, font=("Arial", 12), show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)
        self.password_entry.insert(0, "admin")  # Пример пароля
        
        # Кнопка входа
        login_btn = ttk.Button(login_frame, text="Войти", command=self.login, 
                               style="Accent.TButton")
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Информация для тестирования
        info_frame = ttk.LabelFrame(login_frame, text="Тестовые пользователи", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        info_text = """admin - администратор
i.petrov - учитель (Иван Петров)
alex.ivanov - ученик (Алексей Иванов)
s.ivanov - родитель (Сергей Иванов)
Пароль: admin (для всех тестовых пользователей)"""
        
        ttk.Label(info_frame, text=info_text, justify="left").pack()
        
    def login(self):
        """Авторизация пользователя"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Ошибка", "Введите логин и пароль")
            return
        
        if not self.connect_to_db():
            return
        
        try:
            # В реальном приложении нужно использовать хеширование паролей
            # Для демонстрации сравниваем напрямую
            self.cursor.execute("""
                SELECT user_id, user_type, related_id, password_hash 
                FROM users 
                WHERE username = %s AND is_active = TRUE
            """, (username,))
            
            user = self.cursor.fetchone()
            
            if user:
                # В демо-версии пропускаем проверку хеша
                # if check_password_hash(user[3], password):
                if True:  # Для демо всегда True
                    self.current_user = {
                        'user_id': user[0],
                        'username': username,
                        'user_type': user[1],
                        'related_id': user[2]
                    }
                    self.current_role = user[1]
                    self.show_main_window()
                else:
                    messagebox.showerror("Ошибка", "Неверный пароль")
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при авторизации:\n{str(e)}")
    
    def show_main_window(self):
        """Главное окно приложения после входа"""
        self.clear_window()
        
        # Создаем верхнюю панель
        self.create_top_bar()
        
        # Создаем основную область
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Показываем вид для текущей роли
        if self.current_role == 'admin':
            self.show_admin_view()
        elif self.current_role == 'teacher':
            self.show_teacher_view()
        elif self.current_role == 'student':
            self.show_student_view()
        elif self.current_role == 'parent':
            self.show_parent_view()
    
    def create_top_bar(self):
        """Создание верхней панели навигации"""
        top_bar = ttk.Frame(self.root, height=60)
        top_bar.pack(fill="x", padx=20, pady=10)
        
        # Информация о пользователе
        user_info = f"{self.current_user['username']} ({self.current_role})"
        user_label = ttk.Label(top_bar, text=user_info, font=("Arial", 12, "bold"))
        user_label.pack(side="left")
        
        # Кнопка выхода
        logout_btn = ttk.Button(top_bar, text="Выйти", command=self.logout)
        logout_btn.pack(side="right")
        
        # Кнопка обновления
        refresh_btn = ttk.Button(top_bar, text="Обновить", command=self.refresh_data)
        refresh_btn.pack(side="right", padx=10)
    
    def show_admin_view(self):
        """Вид для администратора"""
        # Создаем Notebook для вкладок
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Вкладка: Пользователи
        users_frame = ttk.Frame(notebook)
        notebook.add(users_frame, text="Пользователи")
        self.create_users_tab(users_frame)
        
        # Вкладка: Ученики
        students_frame = ttk.Frame(notebook)
        notebook.add(students_frame, text="Ученики")
        self.create_students_tab(students_frame)
        
        # Вкладка: Учителя
        teachers_frame = ttk.Frame(notebook)
        notebook.add(teachers_frame, text="Учителя")
        self.create_teachers_tab(teachers_frame)
        
        # Вкладка: Классы
        classes_frame = ttk.Frame(notebook)
        notebook.add(classes_frame, text="Классы")
        self.create_classes_tab(classes_frame)
        
        # Вкладка: Статистика
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Статистика")
        self.create_stats_tab(stats_frame)
    
    def show_teacher_view(self):
        """Вид для учителя"""
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Вкладка: Мои классы
        my_classes_frame = ttk.Frame(notebook)
        notebook.add(my_classes_frame, text="Мои классы")
        self.create_teacher_classes_tab(my_classes_frame)
        
        # Вкладка: Журнал оценок
        grades_frame = ttk.Frame(notebook)
        notebook.add(grades_frame, text="Журнал оценок")
        self.create_teacher_grades_tab(grades_frame)
        
        # Вкладка: Домашние задания
        homework_frame = ttk.Frame(notebook)
        notebook.add(homework_frame, text="Домашние задания")
        self.create_homework_tab(homework_frame)
        
        # Вкладка: Расписание
        schedule_frame = ttk.Frame(notebook)
        notebook.add(schedule_frame, text="Расписание")
        self.create_teacher_schedule_tab(schedule_frame)
    
    def show_student_view(self):
        """Вид для ученика"""
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Вкладка: Мои оценки
        grades_frame = ttk.Frame(notebook)
        notebook.add(grades_frame, text="Мои оценки")
        self.create_student_grades_tab(grades_frame)
        
        # Вкладка: Расписание
        schedule_frame = ttk.Frame(notebook)
        notebook.add(schedule_frame, text="Расписание")
        self.create_student_schedule_tab(schedule_frame)
        
        # Вкладка: Домашние задания
        homework_frame = ttk.Frame(notebook)
        notebook.add(homework_frame, text="Домашние задания")
        self.create_student_homework_tab(homework_frame)
        
        # Вкладка: Посещаемость
        attendance_frame = ttk.Frame(notebook)
        notebook.add(attendance_frame, text="Посещаемость")
        self.create_student_attendance_tab(attendance_frame)
    
    def show_parent_view(self):
        """Вид для родителя"""
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Вкладка: Дети
        children_frame = ttk.Frame(notebook)
        notebook.add(children_frame, text="Мои дети")
        self.create_parent_children_tab(children_frame)
        
        # Вкладка: Успеваемость
        performance_frame = ttk.Frame(notebook)
        notebook.add(performance_frame, text="Успеваемость")
        self.create_parent_performance_tab(performance_frame)
        
        # Вкладка: Посещаемость
        attendance_frame = ttk.Frame(notebook)
        notebook.add(attendance_frame, text="Посещаемость")
        self.create_parent_attendance_tab(attendance_frame)
        
        # Вкладка: Уведомления
        notifications_frame = ttk.Frame(notebook)
        notebook.add(notifications_frame, text="Уведомления")
        self.create_notifications_tab(notifications_frame)
    
    # ============= АДМИНИСТРАТОР =============
    
    def create_users_tab(self, parent):
        """Вкладка управления пользователями для администратора"""
        # Панель инструментов
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill="x", pady=5)
        
        ttk.Button(toolbar, text="Добавить пользователя", 
                  command=self.add_user).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Редактировать", 
                  command=self.edit_user).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Удалить", 
                  command=self.delete_user).pack(side="left", padx=5)
        
        # Таблица пользователей
        columns = ("ID", "Логин", "Тип", "Связанный ID", "Активен", "Последний вход")
        self.users_tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.load_users_data()
    
    def create_students_tab(self, parent):
        """Вкладка управления учениками"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill="x", pady=5)
        
        ttk.Button(toolbar, text="Добавить ученика", 
                  command=self.add_student).pack(side="left", padx=5)
        
        columns = ("ID", "Фамилия", "Имя", "Класс", "Дата рождения", "Год поступления")
        self.students_tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        self.students_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.load_students_data()
    
    def create_teachers_tab(self, parent):
        """Вкладка управления учителями"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill="x", pady=5)
        
        ttk.Button(toolbar, text="Добавить учителя", 
                  command=self.add_teacher).pack(side="left", padx=5)
        
        columns = ("ID", "Фамилия", "Имя", "Дата рождения", "Квалификация", "Дата найма")
        self.teachers_tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.teachers_tree.heading(col, text=col)
            self.teachers_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.teachers_tree.yview)
        self.teachers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.teachers_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.load_teachers_data()
    
    def create_classes_tab(self, parent):
        """Вкладка управления классами"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill="x", pady=5)
        
        ttk.Button(toolbar, text="Добавить класс", 
                  command=self.add_class).pack(side="left", padx=5)
        
        columns = ("ID", "Класс", "Классный руководитель", "Учебный год")
        self.classes_tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.classes_tree.heading(col, text=col)
            self.classes_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.classes_tree.yview)
        self.classes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.classes_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.load_classes_data()
    
    def create_stats_tab(self, parent):
        """Вкладка со статистикой"""
        stats_text = tk.Text(parent, wrap="word", height=20, font=("Arial", 10))
        stats_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        try:
            # Статистика по пользователям
            self.cursor.execute("""
                SELECT user_type, COUNT(*) 
                FROM users 
                GROUP BY user_type
            """)
            user_stats = self.cursor.fetchall()
            
            # Статистика по классам
            self.cursor.execute("""
                SELECT class_name, COUNT(s.student_id) 
                FROM classes c
                LEFT JOIN students s ON c.class_id = s.class_id
                GROUP BY c.class_id, c.class_name
            """)
            class_stats = self.cursor.fetchall()
            
            # Статистика по оценкам
            self.cursor.execute("""
                SELECT 
                    AVG(grade_value) as avg_grade,
                    MIN(grade_value) as min_grade,
                    MAX(grade_value) as max_grade,
                    COUNT(*) as total_grades
                FROM grades
            """)
            grade_stats = self.cursor.fetchone()
            
            stats_text.insert("end", "=== СТАТИСТИКА ШКОЛЫ ===\n\n")
            stats_text.insert("end", "1. Пользователи по типам:\n")
            for user_type, count in user_stats:
                stats_text.insert("end", f"   {user_type}: {count}\n")
            
            stats_text.insert("end", "\n2. Количество учеников по классам:\n")
            for class_name, count in class_stats:
                stats_text.insert("end", f"   {class_name}: {count}\n")
            
            stats_text.insert("end", "\n3. Статистика оценок:\n")
            if grade_stats:
                stats_text.insert("end", f"   Средний балл: {grade_stats[0]:.2f}\n")
                stats_text.insert("end", f"   Минимальная оценка: {grade_stats[1]}\n")
                stats_text.insert("end", f"   Максимальная оценка: {grade_stats[2]}\n")
                stats_text.insert("end", f"   Всего оценок: {grade_stats[3]}\n")
            
            stats_text.config(state="disabled")
            
        except Exception as e:
            stats_text.insert("end", f"Ошибка при загрузке статистики: {str(e)}")
    
    # ============= УЧИТЕЛЬ =============
    
    def create_teacher_classes_tab(self, parent):
        """Вкладка 'Мои классы' для учителя"""
        try:
            # Получаем информацию о классах, где учитель является классным руководителем
            self.cursor.execute("""
                SELECT c.class_id, c.class_name, COUNT(s.student_id) as student_count
                FROM classes c
                LEFT JOIN students s ON c.class_id = s.class_id
                WHERE c.class_teacher_id = %s
                GROUP BY c.class_id, c.class_name
            """, (self.current_user['related_id'],))
            
            classes = self.cursor.fetchall()
            
            for i, (class_id, class_name, student_count) in enumerate(classes):
                class_frame = ttk.LabelFrame(parent, text=f"Класс: {class_name}", padding="10")
                class_frame.pack(fill="x", padx=10, pady=5)
                
                ttk.Label(class_frame, text=f"Количество учеников: {student_count}").pack(anchor="w")
                
                # Получаем список учеников класса
                self.cursor.execute("""
                    SELECT student_id, first_name, last_name, birth_date
                    FROM students
                    WHERE class_id = %s
                    ORDER BY last_name, first_name
                """, (class_id,))
                
                students = self.cursor.fetchall()
                
                tree_frame = ttk.Frame(class_frame)
                tree_frame.pack(fill="x", pady=5)
                
                columns = ("ID", "Фамилия", "Имя", "Дата рождения")
                tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=min(len(students), 10))
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=100)
                
                for student in students:
                    tree.insert("", "end", values=student)
                
                scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                
                tree.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
    
    def create_teacher_grades_tab(self, parent):
        """Вкладка 'Журнал оценок' для учителя"""
        # Выбор класса и предмета
        selection_frame = ttk.Frame(parent)
        selection_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(selection_frame, text="Класс:").pack(side="left", padx=5)
        self.class_combo = ttk.Combobox(selection_frame, width=15)
        self.class_combo.pack(side="left", padx=5)
        
        ttk.Label(selection_frame, text="Предмет:").pack(side="left", padx=5)
        self.subject_combo = ttk.Combobox(selection_frame, width=20)
        self.subject_combo.pack(side="left", padx=5)
        
        ttk.Button(selection_frame, text="Загрузить", 
                  command=self.load_grades_for_class).pack(side="left", padx=10)
        
        ttk.Button(selection_frame, text="Добавить оценку", 
                  command=self.add_grade).pack(side="left", padx=5)
        
        # Загружаем классы и предметы
        self.load_teacher_classes_and_subjects()
        
        # Таблица оценок
        self.grades_frame = ttk.Frame(parent)
        self.grades_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_homework_tab(self, parent):
        """Вкладка 'Домашние задания' для учителя"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(toolbar, text="Добавить задание", 
                  command=self.add_homework).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Проверить задания", 
                  command=self.review_homework).pack(side="left", padx=5)
        
        # Таблица заданий
        columns = ("ID", "Предмет", "Класс", "Задание", "Срок", "Сдано", "Проверено")
        self.homework_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.homework_tree.heading(col, text=col)
            self.homework_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.homework_tree.yview)
        self.homework_tree.configure(yscrollcommand=scrollbar.set)
        
        self.homework_tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        self.load_teacher_homework()
    
    def create_teacher_schedule_tab(self, parent):
        """Вкладка 'Расписание' для учителя"""
        try:
            # Получаем расписание учителя
            self.cursor.execute("""
                SELECT 
                    s.day_of_week,
                    s.lesson_number,
                    c.class_name,
                    sub.subject_name,
                    s.room_number
                FROM schedule s
                JOIN classes c ON s.class_id = c.class_id
                JOIN subjects sub ON s.subject_id = sub.subject_id
                WHERE s.teacher_id = %s AND s.is_active = TRUE
                ORDER BY s.day_of_week, s.lesson_number
            """, (self.current_user['related_id'],))
            
            schedule = self.cursor.fetchall()
            
            days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
            
            text = tk.Text(parent, wrap="word", height=20, font=("Arial", 10))
            text.pack(fill="both", expand=True, padx=10, pady=10)
            
            current_day = None
            for day_num, lesson_num, class_name, subject_name, room in schedule:
                if day_num != current_day:
                    text.insert("end", f"\n=== {days[day_num-1]} ===\n")
                    current_day = day_num
                
                text.insert("end", f"  {lesson_num}. {subject_name} - {class_name} (каб. {room})\n")
            
            text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить расписание: {str(e)}")
    
    # ============= УЧЕНИК =============
    
    def create_student_grades_tab(self, parent):
        """Вкладка 'Мои оценки' для ученика"""
        try:
            # Получаем оценки ученика
            self.cursor.execute("""
                SELECT 
                    sub.subject_name,
                    g.grade_value,
                    g.grade_date,
                    g.grade_type,
                    g.lesson_topic,
                    t.first_name || ' ' || t.last_name as teacher_name
                FROM grades g
                JOIN subjects sub ON g.subject_id = sub.subject_id
                LEFT JOIN teachers t ON g.teacher_id = t.teacher_id
                WHERE g.student_id = %s
                ORDER BY g.grade_date DESC
            """, (self.current_user['related_id'],))
            
            grades = self.cursor.fetchall()
            
            # Создаем таблицу
            columns = ("Предмет", "Оценка", "Дата", "Тип", "Тема", "Учитель")
            tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)
            
            for grade in grades:
                tree.insert("", "end", values=grade)
            
            scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")
            
            # Средние оценки
            self.cursor.execute("""
                SELECT 
                    sub.subject_name,
                    AVG(g.grade_value)::DECIMAL(3,2) as avg_grade
                FROM grades g
                JOIN subjects sub ON g.subject_id = sub.subject_id
                WHERE g.student_id = %s
                GROUP BY sub.subject_name
            """, (self.current_user['related_id'],))
            
            averages = self.cursor.fetchall()
            
            avg_frame = ttk.LabelFrame(parent, text="Средние баллы", padding="10")
            avg_frame.pack(fill="x", padx=10, pady=10)
            
            for subject, avg in averages:
                ttk.Label(avg_frame, text=f"{subject}: {avg}").pack(anchor="w")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить оценки: {str(e)}")
    
    def create_student_schedule_tab(self, parent):
        """Вкладка 'Расписание' для ученика"""
        try:
            # Получаем класс ученика
            self.cursor.execute("""
                SELECT class_id FROM students WHERE student_id = %s
            """, (self.current_user['related_id'],))
            
            class_id = self.cursor.fetchone()[0]
            
            # Получаем расписание
            self.cursor.execute("""
                SELECT 
                    s.day_of_week,
                    s.lesson_number,
                    sub.subject_name,
                    t.first_name || ' ' || t.last_name as teacher_name,
                    s.room_number
                FROM schedule s
                JOIN subjects sub ON s.subject_id = sub.subject_id
                LEFT JOIN teachers t ON s.teacher_id = t.teacher_id
                WHERE s.class_id = %s AND s.is_active = TRUE
                ORDER BY s.day_of_week, s.lesson_number
            """, (class_id,))
            
            schedule = self.cursor.fetchall()
            
            days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
            
            text = tk.Text(parent, wrap="word", height=20, font=("Arial", 10))
            text.pack(fill="both", expand=True, padx=10, pady=10)
            
            current_day = None
            for day_num, lesson_num, subject_name, teacher_name, room in schedule:
                if day_num != current_day:
                    text.insert("end", f"\n=== {days[day_num-1]} ===\n")
                    current_day = day_num
                
                text.insert("end", f"  {lesson_num}. {subject_name}")
                if teacher_name:
                    text.insert("end", f" - {teacher_name}")
                if room:
                    text.insert("end", f" (каб. {room})")
                text.insert("end", "\n")
            
            text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить расписание: {str(e)}")
    
    def create_student_homework_tab(self, parent):
        """Вкладка 'Домашние задания' для ученика"""
        try:
            toolbar = ttk.Frame(parent)
            toolbar.pack(fill="x", padx=10, pady=10)
            
            ttk.Button(toolbar, text="Сдать задание", 
                      command=self.submit_homework).pack(side="left", padx=5)
            
            # Получаем домашние задания
            self.cursor.execute("""
                SELECT 
                    h.homework_id,
                    sub.subject_name,
                    h.assignment_text,
                    h.due_date,
                    hs.grade,
                    hs.is_submitted
                FROM homeworks h
                JOIN schedule sch ON h.schedule_id = sch.schedule_id
                JOIN subjects sub ON sch.subject_id = sub.subject_id
                LEFT JOIN homework_submissions hs ON h.homework_id = hs.homework_id 
                    AND hs.student_id = %s
                WHERE sch.class_id = (SELECT class_id FROM students WHERE student_id = %s)
                    AND h.due_date >= CURRENT_DATE
                ORDER BY h.due_date
            """, (self.current_user['related_id'], self.current_user['related_id']))
            
            homeworks = self.cursor.fetchall()
            
            # Таблица заданий
            columns = ("ID", "Предмет", "Задание", "Срок", "Оценка", "Статус")
            tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)
            
            for hw in homeworks:
                status = "Сдано" if hw[5] else "Не сдано"
                grade = hw[4] if hw[4] else "-"
                tree.insert("", "end", values=(hw[0], hw[1], hw[2][:50] + "...", hw[3], grade, status))
            
            scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить задания: {str(e)}")
    
    def create_student_attendance_tab(self, parent):
        """Вкладка 'Посещаемость' для ученика"""
        try:
            # Получаем посещаемость ученика
            self.cursor.execute("""
                SELECT 
                    a.attendance_date,
                    sub.subject_name,
                    a.status,
                    a.reason
                FROM attendance a
                JOIN schedule sch ON a.schedule_id = sch.schedule_id
                JOIN subjects sub ON sch.subject_id = sub.subject_id
                WHERE a.student_id = %s
                ORDER BY a.attendance_date DESC
                LIMIT 20
            """, (self.current_user['related_id'],))
            
            attendance = self.cursor.fetchall()
            
            # Создаем таблицу
            columns = ("Дата", "Предмет", "Статус", "Причина")
            tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)
            
            for record in attendance:
                tree.insert("", "end", values=record)
            
            scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")
            
            # Статистика посещаемости
            self.cursor.execute("""
                SELECT 
                    COUNT(CASE WHEN status = 'присутствовал' THEN 1 END) as present,
                    COUNT(CASE WHEN status = 'отсутствовал' THEN 1 END) as absent,
                    COUNT(CASE WHEN status = 'болел' THEN 1 END) as sick,
                    COUNT(CASE WHEN status = 'опоздал' THEN 1 END) as late,
                    COUNT(*) as total
                FROM attendance
                WHERE student_id = %s
            """, (self.current_user['related_id'],))
            
            stats = self.cursor.fetchone()
            
            if stats:
                stats_frame = ttk.LabelFrame(parent, text="Статистика посещаемости", padding="10")
                stats_frame.pack(fill="x", padx=10, pady=10)
                
                ttk.Label(stats_frame, text=f"Присутствовал: {stats[0]}").pack(anchor="w")
                ttk.Label(stats_frame, text=f"Отсутствовал: {stats[1]}").pack(anchor="w")
                ttk.Label(stats_frame, text=f"Болел: {stats[2]}").pack(anchor="w")
                ttk.Label(stats_frame, text=f"Опоздал: {stats[3]}").pack(anchor="w")
                
                if stats[4] > 0:
                    percentage = (stats[0] / stats[4]) * 100
                    ttk.Label(stats_frame, text=f"Процент посещаемости: {percentage:.1f}%").pack(anchor="w")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить посещаемость: {str(e)}")
    
    # ============= РОДИТЕЛЬ =============
    
    def create_parent_children_tab(self, parent):
        """Вкладка 'Мои дети' для родителя"""
        try:
            # Получаем детей родителя
            self.cursor.execute("""
                SELECT 
                    s.student_id,
                    s.first_name || ' ' || s.last_name as child_name,
                    c.class_name,
                    t.first_name || ' ' || t.last_name as class_teacher,
                    s.birth_date
                FROM parents p
                JOIN students s ON p.student_id = s.student_id
                JOIN classes c ON s.class_id = c.class_id
                JOIN teachers t ON c.class_teacher_id = t.teacher_id
                WHERE p.parent_id = %s
            """, (self.current_user['related_id'],))
            
            children = self.cursor.fetchall()
            
            for i, (student_id, child_name, class_name, teacher, birth_date) in enumerate(children):
                child_frame = ttk.LabelFrame(parent, text=child_name, padding="10")
                child_frame.pack(fill="x", padx=10, pady=5)
                
                ttk.Label(child_frame, text=f"Класс: {class_name}").pack(anchor="w")
                ttk.Label(child_frame, text=f"Классный руководитель: {teacher}").pack(anchor="w")
                ttk.Label(child_frame, text=f"Дата рождения: {birth_date}").pack(anchor="w")
                
                # Кнопка для просмотра успеваемости
                ttk.Button(child_frame, text="Просмотреть успеваемость",
                          command=lambda sid=student_id: self.show_child_grades(sid)).pack(anchor="w", pady=5)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные о детях: {str(e)}")
    
    def create_parent_performance_tab(self, parent):
        """Вкладка 'Успеваемость' для родителя"""
        try:
            # Получаем детей
            self.cursor.execute("""
                SELECT s.student_id, s.first_name || ' ' || s.last_name as child_name
                FROM parents p
                JOIN students s ON p.student_id = s.student_id
                WHERE p.parent_id = %s
            """, (self.current_user['related_id'],))
            
            children = self.cursor.fetchall()
            
            if not children:
                ttk.Label(parent, text="Нет данных о детях").pack(pady=20)
                return
            
            # Выбор ребенка
            selection_frame = ttk.Frame(parent)
            selection_frame.pack(fill="x", padx=10, pady=10)
            
            ttk.Label(selection_frame, text="Ребенок:").pack(side="left", padx=5)
            self.child_combo = ttk.Combobox(selection_frame, width=30)
            self.child_combo['values'] = [f"{name} (ID: {sid})" for sid, name in children]
            if children:
                self.child_combo.set(f"{children[0][1]} (ID: {children[0][0]})")
            self.child_combo.pack(side="left", padx=5)
            
            ttk.Button(selection_frame, text="Показать успеваемость",
                      command=self.show_child_performance).pack(side="left", padx=10)
            
            # Область для отображения успеваемости
            self.performance_text = tk.Text(parent, wrap="word", height=20, font=("Arial", 10))
            self.performance_text.pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
    
    def create_parent_attendance_tab(self, parent):
        """Вкладка 'Посещаемость' для родителя"""
        try:
            # Получаем детей
            self.cursor.execute("""
                SELECT s.student_id, s.first_name || ' ' || s.last_name as child_name
                FROM parents p
                JOIN students s ON p.student_id = s.student_id
                WHERE p.parent_id = %s
            """, (self.current_user['related_id'],))
            
            children = self.cursor.fetchall()
            
            if not children:
                ttk.Label(parent, text="Нет данных о детях").pack(pady=20)
                return
            
            # Выбор ребенка
            selection_frame = ttk.Frame(parent)
            selection_frame.pack(fill="x", padx=10, pady=10)
            
            ttk.Label(selection_frame, text="Ребенок:").pack(side="left", padx=5)
            self.attendance_child_combo = ttk.Combobox(selection_frame, width=30)
            self.attendance_child_combo['values'] = [f"{name} (ID: {sid})" for sid, name in children]
            if children:
                self.attendance_child_combo.set(f"{children[0][1]} (ID: {children[0][0]})")
            self.attendance_child_combo.pack(side="left", padx=5)
            
            ttk.Button(selection_frame, text="Показать посещаемость",
                      command=self.show_child_attendance).pack(side="left", padx=10)
            
            # Область для отображения посещаемости
            self.attendance_text = tk.Text(parent, wrap="word", height=20, font=("Arial", 10))
            self.attendance_text.pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
    
    def create_notifications_tab(self, parent):
        """Вкладка 'Уведомления' для родителя"""
        try:
            # Получаем уведомления
            self.cursor.execute("""
                SELECT 
                    n.title,
                    n.message,
                    n.notification_type,
                    n.created_at,
                    n.is_read
                FROM notifications n
                JOIN users u ON n.user_id = u.user_id
                WHERE u.username = %s OR u.related_id = %s
                ORDER BY n.created_at DESC
            """, (self.current_user['username'], self.current_user['related_id']))
            
            notifications = self.cursor.fetchall()
            
            # Таблица уведомлений
            columns = ("Заголовок", "Тип", "Дата", "Прочитано")
            tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            for notif in notifications:
                read_status = "Да" if notif[4] else "Нет"
                tree.insert("", "end", values=(notif[0], notif[2], notif[3], read_status))
            
            scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")
            
            # Двойной клик для просмотра сообщения
            tree.bind("<Double-1>", lambda e: self.show_notification_message(tree))
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить уведомления: {str(e)}")
    
    # ============= ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ =============
    
    def load_users_data(self):
        """Загрузка данных пользователей"""
        try:
            self.cursor.execute("""
                SELECT user_id, username, user_type, related_id, is_active, last_login
                FROM users
                ORDER BY user_id
            """)
            
            # Очищаем существующие данные
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Добавляем новые данные
            for user in self.cursor.fetchall():
                is_active = "Да" if user[4] else "Нет"
                last_login = user[5].strftime("%Y-%m-%d %H:%M") if user[5] else "-"
                self.users_tree.insert("", "end", values=(user[0], user[1], user[2], 
                                                         user[3] if user[3] else "-", 
                                                         is_active, last_login))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей: {str(e)}")
    
    def load_students_data(self):
        """Загрузка данных учеников"""
        try:
            self.cursor.execute("""
                SELECT s.student_id, s.last_name, s.first_name, c.class_name, 
                       s.birth_date, s.admission_year
                FROM students s
                LEFT JOIN classes c ON s.class_id = c.class_id
                ORDER BY c.class_name, s.last_name, s.first_name
            """)
            
            for item in self.students_tree.get_children():
                self.students_tree.delete(item)
            
            for student in self.cursor.fetchall():
                self.students_tree.insert("", "end", values=student)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить учеников: {str(e)}")
    
    def load_teachers_data(self):
        """Загрузка данных учителей"""
        try:
            self.cursor.execute("""
                SELECT teacher_id, last_name, first_name, birth_date, 
                       qualification, employment_date
                FROM teachers
                ORDER BY last_name, first_name
            """)
            
            for item in self.teachers_tree.get_children():
                self.teachers_tree.delete(item)
            
            for teacher in self.cursor.fetchall():
                self.teachers_tree.insert("", "end", values=teacher)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить учителей: {str(e)}")
    
    def load_classes_data(self):
        """Загрузка данных классов"""
        try:
            self.cursor.execute("""
                SELECT c.class_id, c.class_name, 
                       t.first_name || ' ' || t.last_name as teacher_name,
                       c.academic_year
                FROM classes c
                LEFT JOIN teachers t ON c.class_teacher_id = t.teacher_id
                ORDER BY c.class_name
            """)
            
            for item in self.classes_tree.get_children():
                self.classes_tree.delete(item)
            
            for class_info in self.cursor.fetchall():
                self.classes_tree.insert("", "end", values=class_info)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить классы: {str(e)}")
    
    def load_teacher_classes_and_subjects(self):
        """Загрузка классов и предметов для учителя"""
        try:
            # Классы, в которых преподает учитель
            self.cursor.execute("""
                SELECT DISTINCT c.class_id, c.class_name
                FROM schedule s
                JOIN classes c ON s.class_id = c.class_id
                WHERE s.teacher_id = %s
                ORDER BY c.class_name
            """, (self.current_user['related_id'],))
            
            classes = self.cursor.fetchall()
            self.class_combo['values'] = [f"{name} (ID: {cid})" for cid, name in classes]
            if classes:
                self.class_combo.set(f"{classes[0][1]} (ID: {classes[0][0]})")
            
            # Предметы, которые преподает учитель
            self.cursor.execute("""
                SELECT DISTINCT sub.subject_id, sub.subject_name
                FROM teacher_subjects ts
                JOIN subjects sub ON ts.subject_id = sub.subject_id
                WHERE ts.teacher_id = %s
                ORDER BY sub.subject_name
            """, (self.current_user['related_id'],))
            
            subjects = self.cursor.fetchall()
            self.subject_combo['values'] = [f"{name} (ID: {sid})" for sid, name in subjects]
            if subjects:
                self.subject_combo.set(f"{subjects[0][1]} (ID: {subjects[0][0]})")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
    
    def load_grades_for_class(self):
        """Загрузка оценок для выбранного класса и предмета"""
        try:
            # Извлекаем ID из строки в комбобоксе
            class_str = self.class_combo.get()
            subject_str = self.subject_combo.get()
            
            if not class_str or not subject_str:
                messagebox.showwarning("Ошибка", "Выберите класс и предмет")
                return
            
            class_id = int(class_str.split("(ID: ")[1].rstrip(")"))
            subject_id = int(subject_str.split("(ID: ")[1].rstrip(")"))
            
            # Очищаем предыдущие данные
            for widget in self.grades_frame.winfo_children():
                widget.destroy()
            
            # Получаем учеников класса
            self.cursor.execute("""
                SELECT student_id, first_name, last_name
                FROM students
                WHERE class_id = %s
                ORDER BY last_name, first_name
            """, (class_id,))
            
            students = self.cursor.fetchall()
            
            if not students:
                ttk.Label(self.grades_frame, text="В классе нет учеников").pack(pady=20)
                return
            
            # Создаем таблицу с оценками
            columns = ["Ученик"] + [f"Оценка {i+1}" for i in range(10)] + ["Средний"]
            
            tree = ttk.Treeview(self.grades_frame, columns=columns, show="headings", height=min(len(students), 20))
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=80)
            
            for student_id, first_name, last_name in students:
                # Получаем оценки ученика по предмету
                self.cursor.execute("""
                    SELECT grade_value, grade_date
                    FROM grades
                    WHERE student_id = %s AND subject_id = %s
                    ORDER BY grade_date
                    LIMIT 10
                """, (student_id, subject_id))
                
                grades = self.cursor.fetchall()
                
                # Рассчитываем средний балл
                self.cursor.execute("""
                    SELECT AVG(grade_value)::DECIMAL(3,2)
                    FROM grades
                    WHERE student_id = %s AND subject_id = %s
                """, (student_id, subject_id))
                
                avg_result = self.cursor.fetchone()
                avg_grade = avg_result[0] if avg_result[0] else "-"
                
                # Формируем строку для таблицы
                values = [f"{last_name} {first_name}"]
                for i in range(10):
                    if i < len(grades):
                        values.append(str(grades[i][0]))
                    else:
                        values.append("")
                values.append(str(avg_grade))
                
                tree.insert("", "end", values=values)
            
            scrollbar = ttk.Scrollbar(self.grades_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить оценки: {str(e)}")
    
    def load_teacher_homework(self):
        """Загрузка домашних заданий для учителя"""
        try:
            self.cursor.execute("""
                SELECT 
                    h.homework_id,
                    sub.subject_name,
                    c.class_name,
                    h.assignment_text,
                    h.due_date,
                    COUNT(hs.submission_id) as submitted_count,
                    COUNT(CASE WHEN hs.grade IS NOT NULL THEN 1 END) as graded_count
                FROM homeworks h
                JOIN schedule sch ON h.schedule_id = sch.schedule_id
                JOIN classes c ON sch.class_id = c.class_id
                JOIN subjects sub ON sch.subject_id = sub.subject_id
                LEFT JOIN homework_submissions hs ON h.homework_id = hs.homework_id
                WHERE h.teacher_id = %s
                GROUP BY h.homework_id, sub.subject_name, c.class_name, h.assignment_text, h.due_date
                ORDER BY h.due_date
            """, (self.current_user['related_id'],))
            
            homeworks = self.cursor.fetchall()
            
            for item in self.homework_tree.get_children():
                self.homework_tree.delete(item)
            
            for hw in homeworks:
                self.homework_tree.insert("", "end", values=(
                    hw[0], hw[1], hw[2], hw[3][:50] + "...", hw[4], hw[5], hw[6]
                ))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить задания: {str(e)}")
    
    def show_child_grades(self, student_id):
        """Показать успеваемость ребенка"""
        try:
            # Создаем новое окно
            child_window = tk.Toplevel(self.root)
            child_window.title("Успеваемость ученика")
            child_window.geometry("800x600")
            
            # Получаем информацию об ученике
            self.cursor.execute("""
                SELECT first_name || ' ' || last_name, class_id
                FROM students WHERE student_id = %s
            """, (student_id,))
            
            student_info = self.cursor.fetchone()
            child_window.title(f"Успеваемость: {student_info[0]}")
            
            # Получаем оценки
            self.cursor.execute("""
                SELECT 
                    sub.subject_name,
                    g.grade_value,
                    g.grade_date,
                    g.grade_type,
                    g.lesson_topic
                FROM grades g
                JOIN subjects sub ON g.subject_id = sub.subject_id
                WHERE g.student_id = %s
                ORDER BY g.grade_date DESC
            """, (student_id,))
            
            grades = self.cursor.fetchall()
            
            # Создаем таблицу
            columns = ("Предмет", "Оценка", "Дата", "Тип", "Тема")
            tree = ttk.Treeview(child_window, columns=columns, show="headings", height=20)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)
            
            for grade in grades:
                tree.insert("", "end", values=grade)
            
            scrollbar = ttk.Scrollbar(child_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить успеваемость: {str(e)}")
    
    def show_child_performance(self):
        """Показать успеваемость выбранного ребенка"""
        try:
            # Извлекаем ID ученика
            child_str = self.child_combo.get()
            if not child_str:
                return
            
            student_id = int(child_str.split("(ID: ")[1].rstrip(")"))
            
            # Очищаем текстовое поле
            self.performance_text.delete(1.0, tk.END)
            
            # Получаем оценки по предметам
            self.cursor.execute("""
                SELECT 
                    sub.subject_name,
                    AVG(g.grade_value)::DECIMAL(3,2) as average_grade,
                    COUNT(g.grade_id) as grades_count,
                    MIN(g.grade_value) as min_grade,
                    MAX(g.grade_value) as max_grade
                FROM grades g
                JOIN subjects sub ON g.subject_id = sub.subject_id
                WHERE g.student_id = %s
                GROUP BY sub.subject_name
                ORDER BY sub.subject_name
            """, (student_id,))
            
            subjects = self.cursor.fetchall()
            
            self.performance_text.insert("end", "=== УСПЕВАЕМОСТЬ ===\n\n")
            
            if subjects:
                for subject, avg, count, min_g, max_g in subjects:
                    self.performance_text.insert("end", f"Предмет: {subject}\n")
                    self.performance_text.insert("end", f"  Средний балл: {avg}\n")
                    self.performance_text.insert("end", f"  Количество оценок: {count}\n")
                    self.performance_text.insert("end", f"  Минимальная оценка: {min_g}\n")
                    self.performance_text.insert("end", f"  Максимальная оценка: {max_g}\n\n")
            else:
                self.performance_text.insert("end", "Нет данных об оценках\n")
            
            # Получаем четвертные оценки
            self.cursor.execute("""
                SELECT 
                    sub.subject_name,
                    tg.term_number,
                    tg.grade_value,
                    tg.academic_year
                FROM term_grades tg
                JOIN subjects sub ON tg.subject_id = sub.subject_id
                WHERE tg.student_id = %s
                ORDER BY tg.academic_year DESC, tg.term_number, sub.subject_name
            """, (student_id,))
            
            term_grades = self.cursor.fetchall()
            
            if term_grades:
                self.performance_text.insert("end", "\n=== ЧЕТВЕРТНЫЕ ОЦЕНКИ ===\n\n")
                
                current_year = None
                current_term = None
                
                for subject, term, grade, year in term_grades:
                    if year != current_year:
                        self.performance_text.insert("end", f"\nУчебный год: {year}\n")
                        current_year = year
                        current_term = None
                    
                    if term != current_term:
                        self.performance_text.insert("end", f"  {term}-я четверть:\n")
                        current_term = term
                    
                    self.performance_text.insert("end", f"    {subject}: {grade}\n")
            
            self.performance_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить успеваемость: {str(e)}")
    
    def show_child_attendance(self):
        """Показать посещаемость выбранного ребенка"""
        try:
            # Извлекаем ID ученика
            child_str = self.attendance_child_combo.get()
            if not child_str:
                return
            
            student_id = int(child_str.split("(ID: ")[1].rstrip(")"))
            
            # Очищаем текстовое поле
            self.attendance_text.delete(1.0, tk.END)
            
            # Получаем статистику посещаемости
            self.cursor.execute("""
                SELECT 
                    COUNT(CASE WHEN status = 'присутствовал' THEN 1 END) as present,
                    COUNT(CASE WHEN status = 'отсутствовал' THEN 1 END) as absent,
                    COUNT(CASE WHEN status = 'болел' THEN 1 END) as sick,
                    COUNT(CASE WHEN status = 'опоздал' THEN 1 END) as late,
                    COUNT(*) as total
                FROM attendance
                WHERE student_id = %s
            """, (student_id,))
            
            stats = self.cursor.fetchone()
            
            self.attendance_text.insert("end", "=== СТАТИСТИКА ПОСЕЩАЕМОСТИ ===\n\n")
            
            if stats:
                self.attendance_text.insert("end", f"Всего уроков: {stats[4]}\n")
                self.attendance_text.insert("end", f"Присутствовал: {stats[0]}\n")
                self.attendance_text.insert("end", f"Отсутствовал: {stats[1]}\n")
                self.attendance_text.insert("end", f"Болел: {stats[2]}\n")
                self.attendance_text.insert("end", f"Опоздал: {stats[3]}\n")
                
                if stats[4] > 0:
                    percentage = (stats[0] / stats[4]) * 100
                    self.attendance_text.insert("end", f"\nПроцент посещаемости: {percentage:.1f}%\n")
            
            # Последние пропуски
            self.cursor.execute("""
                SELECT 
                    a.attendance_date,
                    sub.subject_name,
                    a.status,
                    a.reason
                FROM attendance a
                JOIN schedule sch ON a.schedule_id = sch.schedule_id
                JOIN subjects sub ON sch.subject_id = sub.subject_id
                WHERE a.student_id = %s AND a.status != 'присутствовал'
                ORDER BY a.attendance_date DESC
                LIMIT 10
            """, (student_id,))
            
            absences = self.cursor.fetchall()
            
            if absences:
                self.attendance_text.insert("end", "\n=== ПОСЛЕДНИЕ ПРОПУСКИ ===\n\n")
                
                for date, subject, status, reason in absences:
                    self.attendance_text.insert("end", f"Дата: {date}\n")
                    self.attendance_text.insert("end", f"Предмет: {subject}\n")
                    self.attendance_text.insert("end", f"Статус: {status}\n")
                    if reason:
                        self.attendance_text.insert("end", f"Причина: {reason}\n")
                    self.attendance_text.insert("end", "---\n")
            
            self.attendance_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить посещаемость: {str(e)}")
    
    def show_notification_message(self, tree):
        """Показать полный текст уведомления"""
        selection = tree.selection()
        if not selection:
            return
        
        item = tree.item(selection[0])
        title = item['values'][0]
        
        # В реальном приложении нужно получать полное сообщение из БД
        messagebox.showinfo(title, "Полный текст уведомления будет здесь")
    
    # ============= ДИАЛОГИ ДОБАВЛЕНИЯ/РЕДАКТИРОВАНИЯ =============
    
    def add_user(self):
        """Диалог добавления пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("400x300")
        
        # Поля формы
        ttk.Label(dialog, text="Логин:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        username_entry = ttk.Entry(dialog, width=30)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Пароль:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        password_entry = ttk.Entry(dialog, width=30, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Тип:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        user_type_combo = ttk.Combobox(dialog, values=["admin", "teacher", "student", "parent"], width=27)
        user_type_combo.grid(row=2, column=1, padx=5, pady=5)
        user_type_combo.set("student")
        
        ttk.Label(dialog, text="Связанный ID:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        related_id_entry = ttk.Entry(dialog, width=30)
        related_id_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            user_type = user_type_combo.get()
            related_id = related_id_entry.get()
            
            if not username or not password or not user_type:
                messagebox.showwarning("Ошибка", "Заполните обязательные поля")
                return
            
            try:
                related_id_int = int(related_id) if related_id else None
                
                # В реальном приложении нужно хешировать пароль
                password_hash = "demo_hash"  # Заменить на реальное хеширование
                
                self.cursor.execute("""
                    INSERT INTO users (username, password_hash, user_type, related_id, is_active)
                    VALUES (%s, %s, %s, %s, TRUE)
                """, (username, password_hash, user_type, related_id_int))
                
                self.conn.commit()
                messagebox.showinfo("Успех", "Пользователь добавлен")
                dialog.destroy()
                self.load_users_data()
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить пользователя:\n{str(e)}")
                self.conn.rollback()
        
        # Кнопки
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Сохранить", command=save_user).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side="left", padx=5)
    
    def edit_user(self):
        """Редактирование пользователя"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите пользователя для редактирования")
            return
        
        # В реальном приложении нужно реализовать редактирование
        messagebox.showinfo("Информация", "Редактирование пользователей будет реализовано в полной версии")
    
    def delete_user(self):
        """Удаление пользователя"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите пользователя для удаления")
            return
        
        item = self.users_tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            try:
                self.cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                self.conn.commit()
                messagebox.showinfo("Успех", "Пользователь удален")
                self.load_users_data()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить пользователя:\n{str(e)}")
                self.conn.rollback()
    
    def add_student(self):
        """Диалог добавления ученика"""
        messagebox.showinfo("Информация", "Добавление учеников будет реализовано в полной версии")
    
    def add_teacher(self):
        """Диалог добавления учителя"""
        messagebox.showinfo("Информация", "Добавление учителей будет реализовано в полной версии")
    
    def add_class(self):
        """Диалог добавления класса"""
        messagebox.showinfo("Информация", "Добавление классов будет реализовано в полной версии")
    
    def add_grade(self):
        """Диалог добавления оценки"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить оценку")
        dialog.geometry("400x300")
        
        # Поля формы
        ttk.Label(dialog, text="Ученик:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        # Получаем список учеников
        try:
            self.cursor.execute("""
                SELECT student_id, first_name || ' ' || last_name as name
                FROM students
                ORDER BY last_name, first_name
            """)
            students = self.cursor.fetchall()
            student_names = [f"{name} (ID: {sid})" for sid, name in students]
        except:
            student_names = []
        
        student_combo = ttk.Combobox(dialog, values=student_names, width=30)
        student_combo.grid(row=0, column=1, padx=5, pady=5)
        if student_names:
            student_combo.set(student_names[0])
        
        ttk.Label(dialog, text="Предмет:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        # Получаем список предметов
        try:
            self.cursor.execute("SELECT subject_id, subject_name FROM subjects ORDER BY subject_name")
            subjects = self.cursor.fetchall()
            subject_names = [f"{name} (ID: {sid})" for sid, name in subjects]
        except:
            subject_names = []
        
        subject_combo = ttk.Combobox(dialog, values=subject_names, width=30)
        subject_combo.grid(row=1, column=1, padx=5, pady=5)
        if subject_names:
            subject_combo.set(subject_names[0])
        
        ttk.Label(dialog, text="Оценка:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        grade_combo = ttk.Combobox(dialog, values=["5", "4", "3", "2", "1"], width=10)
        grade_combo.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        grade_combo.set("5")
        
        ttk.Label(dialog, text="Тип:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        type_combo = ttk.Combobox(dialog, values=["текущая", "контрольная", "четвертная", "полугодовая", "годовая", "экзамен"], width=20)
        type_combo.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        type_combo.set("текущая")
        
        ttk.Label(dialog, text="Тема урока:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        topic_entry = ttk.Entry(dialog, width=30)
        topic_entry.grid(row=4, column=1, padx=5, pady=5)
        
        def save_grade():
            student_str = student_combo.get()
            subject_str = subject_combo.get()
            grade_value = grade_combo.get()
            grade_type = type_combo.get()
            topic = topic_entry.get()
            
            if not student_str or not subject_str or not grade_value:
                messagebox.showwarning("Ошибка", "Заполните обязательные поля")
                return
            
            try:
                student_id = int(student_str.split("(ID: ")[1].rstrip(")"))
                subject_id = int(subject_str.split("(ID: ")[1].rstrip(")"))
                
                self.cursor.execute("""
                    INSERT INTO grades (student_id, subject_id, teacher_id, grade_value, grade_type, lesson_topic, grade_date)
                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
                """, (student_id, subject_id, self.current_user['related_id'], int(grade_value), grade_type, topic))
                
                self.conn.commit()
                messagebox.showinfo("Успех", "Оценка добавлена")
                dialog.destroy()
                self.load_grades_for_class()
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить оценку:\n{str(e)}")
                self.conn.rollback()
        
        # Кнопки
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Сохранить", command=save_grade).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side="left", padx=5)
    
    def add_homework(self):
        """Диалог добавления домашнего задания"""
        messagebox.showinfo("Информация", "Добавление домашних заданий будет реализовано в полной версии")
    
    def review_homework(self):
        """Проверка домашних заданий"""
        selection = self.homework_tree.selection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите задание для проверки")
            return
        
        messagebox.showinfo("Информация", "Проверка заданий будет реализована в полной версии")
    
    def submit_homework(self):
        """Сдача домашнего задания"""
        messagebox.showinfo("Информация", "Сдача заданий будет реализована в полной версии")
    
    # ============= ОСНОВНЫЕ МЕТОДЫ =============
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.current_role = None
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.show_login_window()
    
    def refresh_data(self):
        """Обновление данных"""
        if self.current_role == 'admin':
            self.show_admin_view()
        elif self.current_role == 'teacher':
            self.show_teacher_view()
        elif self.current_role == 'student':
            self.show_student_view()
        elif self.current_role == 'parent':
            self.show_parent_view()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

# Запуск приложения
if __name__ == "__main__":
    app = SchoolDatabaseApp()
    app.run()