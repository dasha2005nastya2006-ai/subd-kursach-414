--Это код интерфейса для моей бд-Тороговой Организации (Магазин Гитар-Guitar Shop) --

-------------------------
-------------------------

import sys
import os
import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import datetime
from configparser import ConfigParser
import subprocess
import threading
import csv
import hashlib
import pandas as pd
------------------------------
------------------------------
class shop_system:
    def __init__(self, root):
        self.root = root
        self.root.title("Guitar Shop - Управление магазином гитар")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f8f9fa')
        self.conn = None
        self.cursor = None
        self.user_role = None
        self.current_user = None
        self.db_connection_params = None
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#34495e',
            'accent': '#e74c3c',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#c0392b',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }
        self.default_db_params = {
            'host': 'localhost',
            'port': '5432',
            'database': 'shop_system',
            'user': 'postgres',
            'password': ''
        }
        self.config_dir = os.path.expanduser("~/.shop_system_app")
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        self.config_file = os.path.join(self.config_dir, "config.ini")
        self.show_database_setup_screen()

    def show_database_setup_screen(self):
        self.clear_window()
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill=tk.BOTH, expand=True)
        title_frame = tk.Frame(main_container, bg=self.colors['light'])
        title_frame.pack(pady=(50, 30))
        tk.Label(title_frame, text="🎸", font=("Arial", 48), bg=self.colors['light']).pack()
        tk.Label(title_frame, text="Shop System",
                 font=("Arial", 28, "bold"),
                 bg=self.colors['light'],
                 fg=self.colors['dark']).pack(pady=10)
        tk.Label(title_frame, text="Настройка подключения к базе данных",
                 font=("Arial", 14),
                 bg=self.colors['light'],
                 fg=self.colors['dark']).pack()
        connection_frame = tk.Frame(main_container, bg='white', relief=tk.RAISED, bd=1)
        connection_frame.pack(padx=100, pady=20, fill=tk.BOTH, expand=True)
        saved_config = self.load_db_config()
        input_frame = tk.Frame(connection_frame, bg='white')
        input_frame.pack(pady=30, padx=50)
        tk.Label(input_frame, text="Хост сервера:", font=("Arial", 11),
                 bg='white', fg=self.colors['dark']).grid(row=0, column=0, padx=10, pady=15, sticky='e')
        self.host_var = tk.StringVar(value=saved_config.get('host', 'localhost'))
        host_entry = tk.Entry(input_frame, textvariable=self.host_var, width=30, font=("Arial", 11))
        host_entry.grid(row=0, column=1, padx=10, pady=15)
        tk.Label(input_frame, text="Порт:", font=("Arial", 11),
                 bg='white', fg=self.colors['dark']).grid(row=1, column=0, padx=10, pady=15, sticky='e')
        self.port_var = tk.StringVar(value=saved_config.get('port', '5432'))
        port_entry = tk.Entry(input_frame, textvariable=self.port_var, width=30, font=("Arial", 11))
        port_entry.grid(row=1, column=1, padx=10, pady=15)
        tk.Label(input_frame, text="База данных:", font=("Arial", 11),
                 bg='white', fg=self.colors['dark']).grid(row=2, column=0, padx=10, pady=15, sticky='e')
        self.db_var = tk.StringVar(value=saved_config.get('database', 'shop_system'))
        db_entry = tk.Entry(input_frame, textvariable=self.db_var, width=30, font=("Arial", 11))
        db_entry.grid(row=2, column=1, padx=10, pady=15)
        tk.Label(input_frame, text="Пользователь:", font=("Arial", 11),
                 bg='white', fg=self.colors['dark']).grid(row=3, column=0, padx=10, pady=15, sticky='e')
        self.user_var = tk.StringVar(value=saved_config.get('user', 'postgres'))
        user_entry = tk.Entry(input_frame, textvariable=self.user_var, width=30, font=("Arial", 11))
        user_entry.grid(row=3, column=1, padx=10, pady=15)
        tk.Label(input_frame, text="Пароль:", font=("Arial", 11),
                 bg='white', fg=self.colors['dark']).grid(row=4, column=0, padx=10, pady=15, sticky='e')
        self.password_var = tk.StringVar(value=saved_config.get('password', ''))
        password_entry = tk.Entry(input_frame, textvariable=self.password_var, width=30,
                                  font=("Arial", 11), show="*")
        password_entry.grid(row=4, column=1, padx=10, pady=15)
        button_frame = tk.Frame(connection_frame, bg='white')
        button_frame.pack(pady=20)
        connect_btn = tk.Button(button_frame, text="Подключиться",
                                command=self.connect_to_database,
                                bg=self.colors['success'], fg='white',
                                font=("Arial", 12, "bold"),
                                relief=tk.FLAT, padx=30, pady=10,
                                cursor="hand2")
        connect_btn.pack(side=tk.LEFT, padx=10)
        save_btn = tk.Button(button_frame, text="Сохранить настройки",
                             command=self.save_db_config,
                             bg=self.colors['primary'], fg='white',
                             font=("Arial", 12),
                             relief=tk.FLAT, padx=20, pady=10,
                             cursor="hand2")
        save_btn.pack(side=tk.LEFT, padx=10)
        info_frame = tk.Frame(main_container, bg=self.colors['light'])
        info_frame.pack(pady=20, padx=100, fill=tk.X)
        self.status_label = tk.Label(main_container, text="",
                                     font=("Arial", 10),
                                     bg=self.colors['light'], fg=self.colors['danger'])
        self.status_label.pack(pady=10)
        password_entry.focus_set()
        self.root.bind('<Return>', lambda event: self.connect_to_database())

    def load_db_config(self):
        config = ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file, encoding='utf-8')
            if 'database' in config:
                return dict(config['database'])
        return {}

    def save_db_config(self):
        config = ConfigParser()
        config['database'] = {
            'host': self.host_var.get(),
            'port': self.port_var.get(),
            'database': self.db_var.get(),
            'user': self.user_var.get()
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        messagebox.showinfo("Сохранено",
                            "Настройки подключения сохранены!\n\nПароль не сохраняется из соображений безопасности.")

    def connect_to_database(self):
        host = self.host_var.get()
        port = self.port_var.get()
        database = self.db_var.get()
        user = self.user_var.get()
        password = self.password_var.get()
        if not all([host, port, database, user, password]):
            self.status_label.config(text="Заполните все поля, включая пароль!")
            return
        self.db_connection_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        try:
            self.conn = psycopg2.connect(**self.db_connection_params)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'users');
            """)
            self.status_label.config(text="✓ Успешное подключение!", fg=self.colors['success'])
            self.root.after(1000, self.show_login_screen)
        except psycopg2.OperationalError as e:
            error_msg = str(e)
            if "password authentication failed" in error_msg:
                self.status_label.config(text="Ошибка: Неверный пароль!")
            elif "database \"shop_system\" does not exist" in error_msg:
                self.status_label.config(text="База данных не существует. Нажмите 'Создать БД'.")
            elif "connection refused" in error_msg:
                self.status_label.config(
                    text="Ошибка: Не удалось подключиться к серверу. Проверьте, запущен ли PostgreSQL.")
            else:
                self.status_label.config(text=f"Ошибка подключения: {error_msg}")
        except Exception as e:
            self.status_label.config(text=f"Ошибка: {str(e)}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def show_login_screen(self):
        self.clear_window()
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill=tk.BOTH, expand=True)
        left_frame = tk.Frame(main_container, bg=self.colors['primary'], width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False)
        title_label = tk.Label(left_frame, text="Guitar Shop Pro",
                               font=("Arial", 28, "bold"),
                               bg=self.colors['primary'],
                               fg='white')
        title_label.pack(pady=(100, 20))
        subtitle_label = tk.Label(left_frame, text="Управление магазином гитар",
                                  font=("Arial", 14),
                                  bg=self.colors['primary'],
                                  fg=self.colors['light'])
        subtitle_label.pack(pady=(0, 50))
        db_info = tk.Label(left_frame,
                           text=f"База: {self.db_connection_params['database']}\n"
                                f"Сервер: {self.db_connection_params['host']}:{self.db_connection_params['port']}",
                           font=("Arial", 10),
                           bg=self.colors['primary'],
                           fg=self.colors['light'],
                           justify=tk.LEFT)
        db_info.pack(pady=20)
        login_frame = tk.Frame(main_container, bg='white', relief=tk.RAISED, bd=0)
        login_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        form_title = tk.Label(login_frame, text="Вход в систему",
                              font=("Arial", 24, "bold"),
                              bg='white', fg=self.colors['dark'])
        form_title.pack(pady=(100, 50))
        input_frame = tk.Frame(login_frame, bg='white')
        input_frame.pack(pady=20)
        tk.Label(input_frame, text="Логин:", font=("Arial", 11),
                 bg='white', fg=self.colors['dark']).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.login_entry = tk.Entry(input_frame, width=30, font=("Arial", 11),
                                    bg='#f8f9fa', relief=tk.FLAT)
        self.login_entry.grid(row=0, column=1, padx=10, pady=10, ipady=8)
        tk.Label(input_frame, text="Пароль:", font=("Arial", 11),
                 bg='white', fg=self.colors['dark']).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.password_entry = tk.Entry(input_frame, width=30, font=("Arial", 11),
                                       bg='#f8f9fa', relief=tk.FLAT, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, ipady=8)
        login_button = tk.Button(login_frame, text="Войти",
                                 command=self.login,
                                 bg=self.colors['accent'],
                                 fg='white',
                                 font=("Arial", 12, "bold"),
                                 relief=tk.FLAT,
                                 padx=30, pady=10,
                                 cursor="hand2")
        login_button.pack(pady=30)
        back_button = tk.Button(login_frame, text="← Настройки БД",
                                command=self.show_database_setup_screen,
                                bg='black',
                                fg=self.colors['primary'],
                                font=("Arial", 10),
                                relief=tk.FLAT,
                                cursor="hand2")
        back_button.pack(pady=10)
        self.login_entry.focus_set()
        self.root.bind('<Return>', lambda event: self.login())

    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль!")
            return
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute("""
                SELECT user_id, username, role, full_name 
                FROM users 
                WHERE username = %s AND password_hash = %s
            """, (username, password_hash))
            user = self.cursor.fetchone()
            if user:
                self.current_user = {
                    'id': user[0],
                    'username': user[1],
                    'role': user[2],
                    'full_name': user[3]
                }
                self.user_role = user[2]
                self.show_main_interface()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка аутентификации: {str(e)}")

    def show_main_interface(self):
        self.clear_window()
        top_bar = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        logo_frame = tk.Frame(top_bar, bg=self.colors['primary'])
        logo_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(logo_frame, text="🎸", font=("Arial", 24),
                 bg=self.colors['primary'], fg='white').pack(side=tk.LEFT)
        tk.Label(logo_frame, text="Guitar Shop Pro", font=("Arial", 16, "bold"),
                 bg=self.colors['primary'], fg='white').pack(side=tk.LEFT, padx=10)
        user_frame = tk.Frame(top_bar, bg=self.colors['primary'])
        user_frame.pack(side=tk.RIGHT, padx=20)
        role_colors = {
            'admin': '#e74c3c',
            'seller': '#3498db',
            'accountant': '#2ecc71'
        }
        role_color = role_colors.get(self.user_role, self.colors['dark'])
        role_label = tk.Label(user_frame, text=self.user_role.upper(),
                              font=("Arial", 10, "bold"),
                              bg=role_color, fg='white',
                              padx=10, pady=3)
        role_label.pack(side=tk.RIGHT, padx=(10, 0))
        user_label = tk.Label(user_frame,
                              text=f"{self.current_user['full_name']}",
                              font=("Arial", 11),
                              bg=self.colors['primary'], fg='white')
        user_label.pack(side=tk.RIGHT)
        logout_btn = tk.Button(user_frame, text="Выйти",
                               command=self.logout,
                               bg='black', fg='white',
                               font=("Arial", 10),
                               relief=tk.FLAT,
                               cursor="hand2")
        logout_btn.pack(side=tk.RIGHT, padx=(20, 0))
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill=tk.BOTH, expand=True)
        self.sidebar = tk.Frame(main_container, bg=self.colors['secondary'], width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        self.content_area = tk.Frame(main_container, bg='white')
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.create_role_based_menu()
        self.show_dashboard()

    def create_role_based_menu(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()
        common_items = [
            ("📊 Дашборд", self.show_dashboard),
            ("👤 Профиль", self.show_profile)
        ]
        admin_items = [
            ("🏷 Категории", self.show_categories),
            ("🏭 Производители", self.show_manufacturers),
            ("🚚 Поставщики", self.show_suppliers),
            ("👥 Сотрудники", self.show_employees),
            ("📦 Товары", self.show_products),
            ("👥 Клиенты", self.show_clients),
            ("💰 Способы оплаты", self.show_payment_methods),
            ("📞 Способы связи", self.show_contact_methods),
            ("📋 Заказы", self.show_orders),
            ("📊 Отчеты", self.show_reports),
            ("⚙️ Администрирование", self.show_admin_panel)
        ]
        seller_items = [
            ("📦 Товары", self.show_products),
            ("👥 Клиенты", self.show_clients),
            ("🛒 Новый заказ", self.show_new_order),
            ("📋 Заказы", self.show_orders),
            ("💰 Касса", self.show_cash_register)
        ]
        accountant_items = [
            ("📊 Финансы", self.show_finance),
            ("📦 Товары", self.show_products),
            ("📋 Заказы", self.show_orders),
            ("📈 Отчеты", self.show_reports),
            ("💰 Способы оплаты", self.show_payment_methods)
        ]
        if self.user_role == 'admin':
            menu_items = common_items + admin_items
        elif self.user_role == 'seller':
            menu_items = common_items + seller_items
        elif self.user_role == 'accountant':
            menu_items = common_items + accountant_items
        else:
            menu_items = common_items
        for text, command in menu_items:
            btn = tk.Button(self.sidebar, text=text, command=command,
                            bg=self.colors['secondary'], fg='white',
                            font=("Arial", 11),
                            relief=tk.FLAT, anchor='w', padx=20,
                            cursor="hand2")
            btn.pack(fill=tk.X, pady=1, ipady=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['primary']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors['secondary']))

    def show_dashboard(self):
        self.clear_content()
        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(title_frame, text="Дашборд",
                 font=("Arial", 24, "bold"),
                 bg='white', fg=self.colors['dark']).pack(side=tk.LEFT)
        stats_frame = tk.Frame(self.content_area, bg='white')
        stats_frame.pack(fill=tk.X, padx=30, pady=10)
        try:
            if self.user_role == 'admin':
                self.show_admin_dashboard_stats(stats_frame)
            elif self.user_role == 'seller':
                self.show_seller_dashboard_stats(stats_frame)
            elif self.user_role == 'accountant':
                self.show_accountant_dashboard_stats(stats_frame)
        except Exception as e:
            tk.Label(self.content_area, text=f"Ошибка загрузки статистики: {str(e)}",
                     font=("Arial", 12), bg='white').pack(pady=50)

    def show_admin_dashboard_stats(self, parent):
        stats_data = []
        self.cursor.execute("SELECT COUNT(*) FROM product;")
        total_products = self.cursor.fetchone()[0]
        stats_data.append(("📦 Товаров", total_products, "#3498db"))
        self.cursor.execute("SELECT COUNT(*) FROM client;")
        total_clients = self.cursor.fetchone()[0]
        stats_data.append(("👥 Клиентов", total_clients, "#2ecc71"))
        self.cursor.execute("SELECT COALESCE(SUM(total_sum), 0) FROM orders;")
        total_revenue = self.cursor.fetchone()[0]
        stats_data.append(("💰 Выручка", f"₽{float(total_revenue):,.2f}", "#9b59b6"))
        self.cursor.execute("SELECT COUNT(*) FROM orders;")
        total_orders = self.cursor.fetchone()[0]
        stats_data.append(("📋 Заказов", total_orders, "#e74c3c"))
        self.cursor.execute("SELECT COUNT(*) FROM product WHERE stock < 10;")
        low_stock = self.cursor.fetchone()[0]
        stats_data.append(("⚠️ Мало на складе", low_stock, "#f39c12"))
        for i, (title, value, color) in enumerate(stats_data):
            stat_frame = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=0)
            stat_frame.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            tk.Label(stat_frame, text=title, bg=color, fg='white',
                     font=("Arial", 11)).pack(pady=(15, 5))
            tk.Label(stat_frame, text=str(value), bg=color, fg='white',
                     font=("Arial", 24, "bold")).pack(pady=(5, 15))
            parent.columnconfigure(i, weight=1, uniform="stats")
        recent_frame = tk.Frame(self.content_area, bg='white')
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        tk.Label(recent_frame, text="Последние заказы",
                 font=("Arial", 16, "bold"),
                 bg='white').pack(anchor='w', pady=(0, 10))
        self.cursor.execute("""
            SELECT o.order_id, c.name, o.date, o.total_sum
            FROM orders o
            JOIN client c ON o.client_id = c.client_id
            ORDER BY o.date DESC
            LIMIT 10;
        """)
        recent_orders = self.cursor.fetchall()
        if recent_orders:
            columns = ('ID', 'Клиент', 'Дата', 'Сумма')
            tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=8)
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            for order in recent_orders:
                order_list = list(order)
                order_list[3] = f"₽{float(order_list[3]):,.2f}"
                tree.insert('', tk.END, values=order_list)
            scrollbar = ttk.Scrollbar(recent_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_seller_dashboard_stats(self, parent):
        stats_data = []
        self.cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(total_sum), 0)
            FROM orders 
            WHERE DATE(date) = CURRENT_DATE;
        """)
        today_stats = self.cursor.fetchone()
        stats_data.append(("📅 Продаж сегодня", today_stats[0], "#3498db"))
        stats_data.append(("💰 Выручка сегодня", f"₽{float(today_stats[1]):,.2f}", "#2ecc71"))
        self.cursor.execute("SELECT COUNT(*) FROM product WHERE stock > 0;")
        in_stock = self.cursor.fetchone()[0]
        stats_data.append(("📦 В наличии", in_stock, "#9b59b6"))
        for i, (title, value, color) in enumerate(stats_data):
            stat_frame = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=0)
            stat_frame.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            tk.Label(stat_frame, text=title, bg=color, fg='white',
                     font=("Arial", 11)).pack(pady=(15, 5))
            tk.Label(stat_frame, text=str(value), bg=color, fg='white',
                     font=("Arial", 24, "bold")).pack(pady=(5, 15))
            parent.columnconfigure(i, weight=1, uniform="stats")

    def show_accountant_dashboard_stats(self, parent):
        stats_data = []
        self.cursor.execute("SELECT COALESCE(SUM(total_sum), 0) FROM orders;")
        total_revenue = self.cursor.fetchone()[0]
        stats_data.append(("💰 Общая выручка", f"₽{float(total_revenue):,.2f}", "#3498db"))
        self.cursor.execute("SELECT COALESCE(AVG(total_sum), 0) FROM orders;")
        avg_check = self.cursor.fetchone()[0]
        stats_data.append(("📊 Средний чек", f"₽{float(avg_check):,.2f}", "#2ecc71"))
        try:
            self.cursor.execute("""
                SELECT COALESCE(SUM(o.total_sum - (p.purch_price * oi.quantity)), 0)
                FROM orders o
                JOIN order_info oi ON o.order_id = oi.order_id
                JOIN product p ON oi.product_id = p.product_id""")
            profit = self.cursor.fetchone()[0]
        except Exception as e:
            print(f"Ошибка при расчете прибыли: {e}")
            try:
                self.cursor.execute("""
                    SELECT COALESCE(SUM(profit), 0) FROM (
                        SELECT o.total_sum - (p.purch_price * oi.quantity) as profit
                        FROM orders o, order_info oi, product p
                        WHERE o.order_id = oi.order_id 
                        AND oi.product_id = p.product_id) as profits""")
                profit = self.cursor.fetchone()[0]
            except Exception as e2:
                print(f"Альтернативный запрос тоже не сработал: {e2}")
                profit = 0

        stats_data.append(("💵 Прибыль", f"₽{float(profit):,.2f}", "#9b59b6"))

        # Отображаем статистику
        for i, (title, value, color) in enumerate(stats_data):
            stat_frame = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=0)
            stat_frame.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')

            tk.Label(stat_frame, text=title, bg=color, fg='white',
                     font=("Arial", 11)).pack(pady=(15, 5))
            tk.Label(stat_frame, text=str(value), bg=color, fg='white',
                     font=("Arial", 24, "bold")).pack(pady=(5, 15))

            parent.columnconfigure(i, weight=1, uniform="stats")

    def show_profile(self):
        self.clear_content()
        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(title_frame, text="Мой профиль",
                 font=("Arial", 24, "bold"),
                 bg='white', fg=self.colors['dark']).pack(side=tk.LEFT)
        profile_card = tk.Frame(self.content_area, bg='white', relief=tk.RAISED, bd=1)
        profile_card.pack(fill=tk.BOTH, padx=30, pady=20, expand=True)
        avatar_frame = tk.Frame(profile_card, bg='white')
        avatar_frame.pack(pady=30)
        role_icons = {
            'admin': '👑',
            'seller': '👔',
            'accountant': '💰'
        }
        icon = role_icons.get(self.user_role, '👤')
        tk.Label(avatar_frame, text=icon, font=("Arial", 48),
                 bg='white').pack()
        info_frame = tk.Frame(profile_card, bg='white')
        info_frame.pack(pady=10)
        tk.Label(info_frame, text=self.current_user['full_name'],
                 font=("Arial", 18, "bold"), bg='white').pack(pady=5)
        tk.Label(info_frame, text=f"Логин: {self.current_user['username']}",
                 font=("Arial", 12), bg='white').pack(pady=2)
        role_names = {
            'admin': 'Администратор',
            'seller': 'Продавец',
            'accountant': 'Бухгалтер'
        }
        tk.Label(info_frame, text=f"Роль: {role_names.get(self.user_role, self.user_role)}",
                 font=("Arial", 12), bg='white').pack(pady=2)

    def show_products(self):
        self.clear_content()
        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(title_frame, text="Товары",
                 font=("Arial", 24, "bold"),
                 bg='white', fg=self.colors['dark']).pack(side=tk.LEFT)
        control_frame = tk.Frame(self.content_area, bg='white')
        control_frame.pack(fill=tk.X, padx=30, pady=10)
        if self.user_role in ['admin', 'seller']:
            add_btn = tk.Button(control_frame, text="➕ Добавить товар",
                                command=self.add_product,
                                bg=self.colors['success'], fg='white',
                                font=("Arial", 11),
                                relief=tk.FLAT, padx=20, pady=8,
                                cursor="hand2")
            add_btn.pack(side=tk.LEFT, padx=5)
            if self.user_role == 'admin':
                delete_btn = tk.Button(control_frame, text="🗑️ Удалить товар",
                                       command=self.delete_product,
                                       bg=self.colors['danger'], fg='white',
                                       font=("Arial", 11),
                                       relief=tk.FLAT, padx=20, pady=8,
                                       cursor="hand2")
                delete_btn.pack(side=tk.LEFT, padx=5)
            refresh_btn = tk.Button(control_frame, text="🔄 Обновить",
                                    command=self.refresh_products,
                                    bg=self.colors['primary'], fg='white',
                                    font=("Arial", 11),
                                    relief=tk.FLAT, padx=20, pady=8,
                                    cursor="hand2")
            refresh_btn.pack(side=tk.LEFT, padx=5)
        filter_frame = tk.Frame(self.content_area, bg='white')
        filter_frame.pack(fill=tk.X, padx=30, pady=5)
        tk.Label(filter_frame, text="Фильтр по категории:", bg='white').pack(side=tk.LEFT, padx=5)
        self.cursor.execute("SELECT name FROM cat ORDER BY name;")
        categories = ['Все'] + [row[0] for row in self.cursor.fetchall()]
        filter_var = tk.StringVar(value='Все')
        filter_combo = ttk.Combobox(filter_frame, textvariable=filter_var,
                                    values=categories, width=20, state='readonly')
        filter_combo.pack(side=tk.LEFT, padx=5)
        table_frame = tk.Frame(self.content_area, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        columns = ('ID', 'Название', 'Категория', 'Производитель', 'Остаток', 'Закупка', 'Продажа')
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=120)
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscroll=scrollbar.set)
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def load_products(category_filter=None):
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)
            try:
                if category_filter and category_filter != 'Все':
                    self.cursor.execute("""
                        SELECT p.product_id, p.name, c.name as category, 
                               m.name as manufacturer, p.stock, 
                               p.purch_price, p.sale_price
                        FROM product p
                        LEFT JOIN cat c ON p.cat_id = c.cat_id
                        LEFT JOIN manufacturer m ON p.manufacturer_id = m.manufacturer_id
                        WHERE c.name = %s
                        ORDER BY p.product_id;
                    """, (category_filter,))
                else:
                    self.cursor.execute("""
                        SELECT p.product_id, p.name, c.name as category, 
                               m.name as manufacturer, p.stock, 
                               p.purch_price, p.sale_price
                        FROM product p
                        LEFT JOIN cat c ON p.cat_id = c.cat_id
                        LEFT JOIN manufacturer m ON p.manufacturer_id = m.manufacturer_id
                        ORDER BY p.product_id;
                    """)
                products = self.cursor.fetchall()
                for product in products:
                    product_list = list(product)
                    product_list[5] = f"₽{product_list[5]:,.2f}"
                    product_list[6] = f"₽{product_list[6]:,.2f}"
                    self.products_tree.insert('', tk.END, values=product_list)
                total_count = len(products)
                total_stock = sum(product[4] for product in products)
                tk.Label(title_frame, text=f"Всего: {total_count} товаров ({total_stock} шт.)",
                         font=("Arial", 11), bg='white', fg=self.colors['dark']).pack(side=tk.RIGHT, padx=20)
            except Exception as e:
                tk.Label(table_frame, text=f"Ошибка загрузки товаров: {str(e)}",
                         font=("Arial", 12), bg='white').pack(pady=50)

        load_products()

        def on_filter_change(*args):
            load_products(filter_var.get())

        filter_var.trace('w', on_filter_change)

    def delete_product(self):
        if not hasattr(self, 'products_tree'):
            messagebox.showwarning("Предупреждение", "Таблица товаров не загружена!")
            return
        selected_items = self.products_tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите товар для удаления!")
            return
        item = self.products_tree.item(selected_items[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        if not messagebox.askyesno("Подтверждение удаления",
                                   f"Вы уверены, что хотите удалить товар?\n\n"
                                   f"ID: {product_id}\n"
                                   f"Название: {product_name}\n\n"
                                   f"Это действие нельзя отменить!"):
            return
        try:
            self.cursor.execute("SELECT COUNT(*) FROM order_info WHERE product_id = %s;", (product_id,))
            order_count = self.cursor.fetchone()[0]
            if order_count > 0:
                if not messagebox.askyesno("Предупреждение",
                                           f"Этот товар используется в {order_count} заказах.\n"
                                           f"Удаление товара удалит его из всех заказов.\n"
                                           f"Продолжить?"):
                    return
                self.cursor.execute("DELETE FROM order_info WHERE product_id = %s;", (product_id,))
            self.cursor.execute("DELETE FROM product WHERE product_id = %s;", (product_id,))
            affected_rows = self.cursor.rowcount
            if affected_rows > 0:
                self.conn.commit()
                messagebox.showinfo("Успех", "Товар успешно удален!")
                self.products_tree.delete(selected_items[0])
            else:
                messagebox.showwarning("Предупреждение", "Товар не найден!")
        except psycopg2.Error as e:
            self.conn.rollback()
            error_msg = str(e)
            if "violates foreign key constraint" in error_msg:
                messagebox.showerror("Ошибка",
                                     "Нельзя удалить товар, так как он используется в других таблицах.")
            else:
                messagebox.showerror("Ошибка", f"Не удалось удалить товар: {error_msg}")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Ошибка", f"Не удалось удалить товар: {str(e)}")

    def refresh_products(self):
        for widget in self.content_area.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Treeview):
                        child.destroy()
                        self.show_products()
                        return

    def add_product(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить товар")
        dialog.geometry("500x600")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        tk.Label(dialog, text="Добавить товар",
                 font=("Arial", 16, "bold"),
                 bg='white').pack(pady=20)
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=30, pady=10)
        tk.Label(form_frame, text="Название:", bg='white').grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form_frame, width=40)
        name_entry.grid(row=0, column=1, pady=5)
        tk.Label(form_frame, text="Категория:", bg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.cursor.execute("SELECT cat_id, name FROM cat ORDER BY name;")
        categories = self.cursor.fetchall()
        self.cat_dict = {name: cat_id for cat_id, name in categories}
        cat_var = tk.StringVar()
        cat_combo = ttk.Combobox(form_frame, textvariable=cat_var, values=[name for _, name in categories])
        cat_combo.grid(row=1, column=1, pady=5)
        if categories:
            cat_combo.current(0)
        tk.Label(form_frame, text="Производитель:", bg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.cursor.execute("SELECT manufacturer_id, name FROM manufacturer ORDER BY name;")
        manufacturers = self.cursor.fetchall()
        self.man_dict = {name: man_id for man_id, name in manufacturers}
        man_var = tk.StringVar()
        man_combo = ttk.Combobox(form_frame, textvariable=man_var, values=[name for _, name in manufacturers])
        man_combo.grid(row=2, column=1, pady=5)
        if manufacturers:
            man_combo.current(0)
        tk.Label(form_frame, text="Поставщик:", bg='white').grid(row=3, column=0, sticky='w', pady=5)
        self.cursor.execute("SELECT supplier_id, name FROM supplier ORDER BY name;")
        suppliers = self.cursor.fetchall()
        self.sup_dict = {name: sup_id for sup_id, name in suppliers}
        sup_var = tk.StringVar()
        sup_combo = ttk.Combobox(form_frame, textvariable=sup_var, values=[name for _, name in suppliers])
        sup_combo.grid(row=3, column=1, pady=5)
        if suppliers:
            sup_combo.current(0)
        tk.Label(form_frame, text="Количество на складе:", bg='white').grid(row=4, column=0, sticky='w', pady=5)
        stock_entry = tk.Entry(form_frame, width=40)
        stock_entry.grid(row=4, column=1, pady=5)
        stock_entry.insert(0, "0")
        tk.Label(form_frame, text="Цена закупки (₽):", bg='white').grid(row=5, column=0, sticky='w', pady=5)
        purch_entry = tk.Entry(form_frame, width=40)
        purch_entry.grid(row=5, column=1, pady=5)
        tk.Label(form_frame, text="Цена продажи (₽):", bg='white').grid(row=6, column=0, sticky='w', pady=5)
        sale_entry = tk.Entry(form_frame, width=40)
        sale_entry.grid(row=6, column=1, pady=5)

        def save_product():
            try:
                name = name_entry.get().strip()
                category_name = cat_var.get()
                manufacturer_name = man_var.get()
                supplier_name = sup_var.get()
                stock_str = stock_entry.get().strip()
                purch_str = purch_entry.get().strip()
                sale_str = sale_entry.get().strip()
                if not name:
                    messagebox.showerror("Ошибка", "Введите название товара!")
                    return
                if not category_name:
                    messagebox.showerror("Ошибка", "Выберите категорию!")
                    return
                if not manufacturer_name:
                    messagebox.showerror("Ошибка", "Выберите производителя!")
                    return
                if not supplier_name:
                    messagebox.showerror("Ошибка", "Выберите поставщика!")
                    return
                if not stock_str:
                    messagebox.showerror("Ошибка", "Введите количество!")
                    return
                if not purch_str:
                    messagebox.showerror("Ошибка", "Введите цену закупки!")
                    return
                if not sale_str:
                    messagebox.showerror("Ошибка", "Введите цену продажи!")
                    return
                try:
                    stock = int(stock_str)
                    purch_price = float(purch_str)
                    sale_price = float(sale_str)
                except ValueError:
                    messagebox.showerror("Ошибка", "Некорректные числовые значения!")
                    return
                if stock < 0:
                    messagebox.showerror("Ошибка", "Количество не может быть отрицательным!")
                    return
                if purch_price <= 0 or sale_price <= 0:
                    messagebox.showerror("Ошибка", "Цены должны быть положительными!")
                    return
                cat_id = self.cat_dict.get(category_name)
                man_id = self.man_dict.get(manufacturer_name)
                sup_id = self.sup_dict.get(supplier_name)
                if not all([cat_id, man_id, sup_id]):
                    messagebox.showerror("Ошибка", "Некорректные значения категории, производителя или поставщика!")
                    return
                self.cursor.execute("""
                    SELECT COUNT(*) FROM product 
                    WHERE name = %s AND cat_id = %s AND manufacturer_id = %s
                """, (name, cat_id, man_id))
                exists = self.cursor.fetchone()[0]
                if exists > 0:
                    if messagebox.askyesno("Подтверждение",
                                           f"Товар '{name}' уже существует в этой категории.\n"
                                           f"Хотите обновить его количество и цены?"):
                        self.cursor.execute("""
                            UPDATE product 
                            SET stock = stock + %s, purch_price = %s, sale_price = %s, 
                                supplier_id = %s
                            WHERE name = %s AND cat_id = %s AND manufacturer_id = %s
                        """, (stock, purch_price, sale_price, sup_id, name, cat_id, man_id))
                        self.conn.commit()
                        messagebox.showinfo("Успех", "Товар обновлен!")
                        dialog.destroy()
                        self.refresh_products()
                        return
                    else:
                        return
                self.cursor.execute("""
                    INSERT INTO product 
                    (cat_id, manufacturer_id, supplier_id, name, stock, purch_price, sale_price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (cat_id, man_id, sup_id, name, stock, purch_price, sale_price))
                self.conn.commit()
                messagebox.showinfo("Успех", "Товар успешно добавлен!")
                dialog.destroy()
                self.refresh_products()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить товар: {str(e)}")
                self.conn.rollback()

        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Сохранить", command=save_product,
                  bg=self.colors['success'], fg='white',
                  font=("Arial", 12),
                  relief=tk.FLAT, padx=30, pady=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Отмена", command=dialog.destroy,
                  bg=self.colors['danger'], fg='white',
                  font=("Arial", 12),
                  relief=tk.FLAT, padx=30, pady=10).pack(side=tk.LEFT, padx=10)

    def delete_record(self, table_name, record_id, id_column='id'):
        try:
            if not messagebox.askyesno("Подтверждение удаления",
                                       f"Вы уверены, что хотите удалить запись с ID {record_id}?\n"
                                       f"Это действие нельзя отменить!"):
                return False
            if table_name == 'product':
                self.cursor.execute("SELECT COUNT(*) FROM order_info WHERE product_id = %s;", (record_id,))
                order_count = self.cursor.fetchone()[0]
                if order_count > 0:
                    if not messagebox.askyesno("Предупреждение",
                                               f"Этот товар используется в {order_count} заказах.\n"
                                               f"Удаление товара может нарушить целостность данных.\n"
                                               f"Продолжить?"):
                        return False
            if table_name == 'orders':
                self.cursor.execute("DELETE FROM order_info WHERE order_info_id = %s;", (record_id,))
            self.cursor.execute(f"""
                DELETE FROM {table_name} WHERE {id_column} = %s
            """, (record_id,))
            affected_rows = self.cursor.rowcount
            if affected_rows > 0:
                self.conn.commit()
                messagebox.showinfo("Успех", "Запись успешно удалена!")
                return True
            else:
                messagebox.showwarning("Предупреждение", "Запись не найдена!")
                return False
        except Exception as e:
            self.conn.rollback()
            error_msg = str(e)
            if "violates foreign key constraint" in error_msg:
                messagebox.showerror("Ошибка",
                                     "Нельзя удалить запись, так как она используется в других таблицах.")
            else:
                messagebox.showerror("Ошибка", f"Не удалось удалить запись: {error_msg}")
            return False

    def delete_selected_record(self, table_name, id_column):
        if table_name == 'product' and hasattr(self, 'products_tree'):
            tree = self.products_tree
        elif table_name == 'orders' and hasattr(self, 'orders_tree'):
            tree = self.orders_tree
        elif table_name == 'client' and hasattr(self, 'clients_tree'):
            tree = self.clients_tree
        else:
            messagebox.showwarning("Предупреждение", "Таблица не найдена!")
            return
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return
        item = tree.item(selected_items[0])
        record_id = item['values'][0]
        if self.delete_record(table_name, record_id, id_column):
            tree.delete(selected_items[0])

    def show_categories(self):
        self.show_simple_table("cat", "Категории товаров", ['cat_id', 'name'])

    def show_manufacturers(self):
        self.show_simple_table("manufacturer", "Производители", ['manufacturer_id', 'name', 'email', 'phone'])

    def show_suppliers(self):
        self.show_simple_table("supplier", "Поставщики", ['supplier_id', 'name', 'email', 'phone'])

    def show_employees(self):
        self.show_simple_table("employees", "Сотрудники", ['employees_id', 'surname', 'name', 'post_id', 'phone'])

    def show_clients(self):
        self.show_simple_table("client", "Клиенты", ['client_id', 'surname', 'name', 'phone', 'email'])

    def show_payment_methods(self):
        self.show_simple_table("pay_method", "Способы оплаты", ['pay_method_id', 'name'])

    def show_contact_methods(self):
        self.show_simple_table("contact_method", "Способы связи", ['contact_method_id', 'name'])

    def show_simple_table(self, table_name, title, columns):
        self.clear_content()
        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(title_frame, text=title,
                 font=("Arial", 24, "bold"),
                 bg='white', fg=self.colors['dark']).pack(side=tk.LEFT)
        control_frame = tk.Frame(self.content_area, bg='white')
        control_frame.pack(fill=tk.X, padx=30, pady=10)
        if self.user_role == 'admin':
            add_btn = tk.Button(control_frame, text=f"➕ Добавить",
                                command=lambda: self.add_simple_record(table_name, columns),
                                bg=self.colors['success'], fg='white',
                                font=("Arial", 11),
                                relief=tk.FLAT, padx=20, pady=8,
                                cursor="hand2")
            add_btn.pack(side=tk.LEFT, padx=5)
            delete_btn = tk.Button(control_frame, text="🗑️ Удалить выбранное",
                                   command=lambda: self.delete_simple_record(table_name, columns[0]),
                                   bg=self.colors['danger'], fg='white',
                                   font=("Arial", 11),
                                   relief=tk.FLAT, padx=20, pady=8,
                                   cursor="hand2")
            delete_btn.pack(side=tk.LEFT, padx=5)
        table_frame = tk.Frame(self.content_area, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        try:
            self.cursor.execute(f"SELECT * FROM {table_name} ORDER BY 1;")
            data = self.cursor.fetchall()
            tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            for row in data:
                tree.insert('', tk.END, values=row)
            scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            if table_name == 'cat':
                self.categories_tree = tree
            elif table_name == 'manufacturer':
                self.manufacturers_tree = tree
            elif table_name == 'supplier':
                self.suppliers_tree = tree
            elif table_name == 'client':
                self.clients_tree = tree
            elif table_name == 'employees':
                self.employees_tree = tree
        except Exception as e:
            tk.Label(table_frame, text=f"Ошибка загрузки данных: {str(e)}",
                     font=("Arial", 12), bg='white').pack(pady=50)

    def add_simple_record(self, table_name, columns):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Добавить в {table_name}")
        dialog.geometry("400x400")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        tk.Label(dialog, text=f"Добавить в {table_name}",
                 font=("Arial", 16, "bold"),
                 bg='white').pack(pady=20)
        entries = []
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=30, pady=10)
        for i, col in enumerate(columns[1:]):
            tk.Label(form_frame, text=f"{col}:", bg='white').grid(row=i, column=0, sticky='w', pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            entries.append(entry)

        def save_record():
            try:
                values = [entry.get() for entry in entries]
                placeholders = ', '.join(['%s'] * len(values))
                columns_str = ', '.join(columns[1:])
                self.cursor.execute(f"""
                    INSERT INTO {table_name} ({columns_str})
                    VALUES ({placeholders})
                """, values)
                self.conn.commit()
                messagebox.showinfo("Успех", "Запись добавлена!")
                dialog.destroy()
                if table_name == 'cat':
                    self.show_categories()
                elif table_name == 'manufacturer':
                    self.show_manufacturers()
                elif table_name == 'supplier':
                    self.show_suppliers()
                elif table_name == 'client':
                    self.show_clients()
                elif table_name == 'employees':
                    self.show_employees()
                elif table_name == 'pay_method':
                    self.show_payment_methods()
                elif table_name == 'contact_method':
                    self.show_contact_methods()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить запись: {str(e)}")

        tk.Button(dialog, text="Сохранить", command=save_record,
                  bg=self.colors['success'], fg='white',
                  font=("Arial", 12),
                  relief=tk.FLAT, padx=30, pady=10).pack(pady=20)

    def delete_simple_record(self, table_name, id_column):
        """Удаляет запись из простой таблицы"""
        # Определяем, из какого дерева удалять
        tree = None

        if table_name == 'cat' and hasattr(self, 'categories_tree'):
            tree = self.categories_tree
        elif table_name == 'manufacturer' and hasattr(self, 'manufacturers_tree'):
            tree = self.manufacturers_tree
        elif table_name == 'supplier' and hasattr(self, 'suppliers_tree'):
            tree = self.suppliers_tree
        elif table_name == 'client' and hasattr(self, 'clients_tree'):
            tree = self.clients_tree
        elif table_name == 'employees' and hasattr(self, 'employees_tree'):
            tree = self.employees_tree
        elif table_name == 'pay_method':
            # Ищем Treeview для pay_method в текущем контенте
            tree = self.find_treeview_in_content('pay_method')
        elif table_name == 'contact_method':
            # Ищем Treeview для contact_method в текущем контенте
            tree = self.find_treeview_in_content('contact_method')

        if not tree:
            messagebox.showwarning("Предупреждение", "Таблица не загружена или не найдена!")
            return

        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return

        item = tree.item(selected_items[0])
        record_id = item['values'][0]

        # Определяем правильное имя столбца ID
        id_column_mapping = {
            'cat': 'cat_id',
            'manufacturer': 'manufacturer_id',
            'supplier': 'supplier_id',
            'client': 'client_id',
            'employees': 'employees_id',
            'pay_method': 'pay_method_id',
            'contact_method': 'contact_method_id'
        }

        actual_id_column = id_column_mapping.get(table_name, id_column)

        # Выполняем удаление
        if self.delete_record(table_name, record_id, actual_id_column):
            # Обновляем таблицу
            tree.delete(selected_items[0])

    def show_new_order(self):
        if self.user_role != 'seller':
            messagebox.showwarning("Доступ запрещен", "Эта функция доступна только продавцам!")
            return
        self.clear_content()
        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(title_frame, text="Новый заказ",
                 font=("Arial", 24, "bold"),
                 bg='white', fg=self.colors['dark']).pack(side=tk.LEFT)
        main_frame = tk.Frame(self.content_area, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        left_frame = tk.LabelFrame(main_frame, text="Товары", font=("Arial", 12, "bold"), bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.cursor.execute("""
            SELECT p.product_id, p.name, c.name as category, p.stock, p.sale_price
            FROM product p
            LEFT JOIN cat c ON p.cat_id = c.cat_id
            WHERE p.stock > 0
            ORDER BY p.name;
        """)
        products = self.cursor.fetchall()
        columns = ('ID', 'Название', 'Категория', 'Остаток', 'Цена')
        self.products_tree_order = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.products_tree_order.heading(col, text=col)
            self.products_tree_order.column(col, width=100)
        for product in products:
            product_list = list(product)
            product_list[4] = f"₽{product_list[4]:,.2f}"
            self.products_tree_order.insert('', tk.END, values=product_list)
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.products_tree_order.yview)
        self.products_tree_order.configure(yscroll=scrollbar.set)
        self.products_tree_order.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        add_to_cart_btn = tk.Button(left_frame, text="➕ Добавить в заказ",
                                    command=self.add_to_cart,
                                    bg=self.colors['success'], fg='white',
                                    font=("Arial", 11),
                                    relief=tk.FLAT, pady=5)
        add_to_cart_btn.pack(fill=tk.X, pady=5)
        right_frame = tk.LabelFrame(main_frame, text="Корзина", font=("Arial", 12, "bold"), bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        cart_columns = ('Товар', 'Кол-во', 'Цена', 'Сумма')
        self.cart_tree = ttk.Treeview(right_frame, columns=cart_columns, show='headings', height=15)
        for col in cart_columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100)
        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cart_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscroll=cart_scrollbar.set)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        remove_from_cart_btn = tk.Button(right_frame, text="🗑️ Удалить из корзины",
                                         command=self.remove_from_cart,
                                         bg=self.colors['danger'], fg='white',
                                         font=("Arial", 11),
                                         relief=tk.FLAT, pady=5)
        remove_from_cart_btn.pack(fill=tk.X, pady=5)
        total_frame = tk.Frame(right_frame, bg='white')
        total_frame.pack(fill=tk.X, pady=10)
        self.total_label = tk.Label(total_frame, text="Итого: ₽0.00",
                                    font=("Arial", 14, "bold"),
                                    bg='white', fg=self.colors['dark'])
        self.total_label.pack()
        client_frame = tk.LabelFrame(main_frame, text="Информация о клиенте",
                                     font=("Arial", 12, "bold"), bg='white')
        client_frame.pack(fill=tk.X, pady=20)
        tk.Label(client_frame, text="Имя:", bg='white').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.client_name_entry = tk.Entry(client_frame, width=30)
        self.client_name_entry.grid(row=0, column=1, pady=5)
        tk.Label(client_frame, text="Телефон:", bg='white').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.client_phone_entry = tk.Entry(client_frame, width=30)
        self.client_phone_entry.grid(row=1, column=1, pady=5)
        checkout_btn = tk.Button(main_frame, text="✅ Оформить заказ",
                                 command=self.process_order,
                                 bg=self.colors['accent'], fg='white',
                                 font=("Arial", 14, "bold"),
                                 relief=tk.FLAT, padx=40, pady=15,
                                 cursor="hand2")
        checkout_btn.pack(pady=20)
        self.cart_items = []

    def add_to_cart(self):
        selected = self.products_tree_order.selection()
        if not selected:
            messagebox.showwarning("Выбор товара", "Выберите товар из списка!")
            return
        item = self.products_tree_order.item(selected[0])
        product_data = item['values']
        dialog = tk.Toplevel(self.root)
        dialog.title("Количество")
        dialog.geometry("300x150")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        tk.Label(dialog, text=f"Товар: {product_data[1]}",
                 font=("Arial", 11), bg='white').pack(pady=10)
        tk.Label(dialog, text="Количество:", bg='white').pack(pady=5)
        qty_entry = tk.Entry(dialog, width=10)
        qty_entry.pack(pady=5)
        qty_entry.insert(0, "1")

        def add_item():
            try:
                qty = int(qty_entry.get())
                if qty <= 0:
                    messagebox.showerror("Ошибка", "Количество должно быть больше 0!")
                    return
                stock = int(product_data[3])
                if qty > stock:
                    messagebox.showerror("Ошибка", f"На складе только {stock} шт.!")
                    return
                price = float(product_data[4].replace('₽', '').replace(',', ''))
                total = price * qty
                cart_item = {
                    'product_id': product_data[0],
                    'name': product_data[1],
                    'quantity': qty,
                    'price': price,
                    'total': total
                }
                self.cart_items.append(cart_item)
                self.cart_tree.insert('', tk.END, values=(
                    cart_item['name'],
                    cart_item['quantity'],
                    f"₽{cart_item['price']:,.2f}",
                    f"₽{cart_item['total']:,.2f}"
                ))
                self.update_cart_total()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное количество!")

        tk.Button(dialog, text="Добавить", command=add_item,
                  bg=self.colors['success'], fg='white').pack(pady=10)

    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Выбор товара", "Выберите товар из корзины!")
            return
        item = self.cart_tree.item(selected[0])
        item_name = item['values'][0]
        if messagebox.askyesno("Удаление", f"Удалить '{item_name}' из корзины?"):
            item_index = None
            for i, cart_item in enumerate(self.cart_items):
                if cart_item['name'] == item_name:
                    item_index = i
                    break
            if item_index is not None:
                del self.cart_items[item_index]
            self.cart_tree.delete(selected[0])
            self.update_cart_total()

    def update_cart_total(self):
        total = sum(item['total'] for item in self.cart_items)
        self.total_label.config(text=f"Итого: ₽{total:,.2f}")

    def find_or_create_client(self, name, phone):
        try:
            if phone:
                self.cursor.execute("""
                    SELECT client_id FROM client 
                    WHERE phone = %s
                    LIMIT 1;
                """, (phone,))
                client = self.cursor.fetchone()
                if client:
                    return client[0]
            self.cursor.execute("""
                SELECT client_id FROM client 
                WHERE name = %s
                LIMIT 1;
            """, (name,))
            client = self.cursor.fetchone()
            if client:
                return client[0]
            self.cursor.execute("""
                INSERT INTO client (name, phone)
                VALUES (%s, %s)
                RETURNING client_id;
            """, (name, phone))
            return self.cursor.fetchone()[0]
        except Exception as e:
            raise Exception(f"Ошибка при работе с клиентом: {str(e)}")

    def process_order(self):
        if not self.cart_items:
            messagebox.showwarning("Корзина пуста", "Добавьте товары в корзину!")
            return
        client_name = self.client_name_entry.get().strip()
        if not client_name:
            messagebox.showerror("Ошибка", "Введите имя клиента!")
            return
        try:
            client_phone = self.client_phone_entry.get().strip()
            self.cursor.execute("""
                INSERT INTO client (name, phone)
                VALUES (%s, %s)
                RETURNING client_id;
            """, (client_name, client_phone))
            client_id = self.cursor.fetchone()[0]
            total_sum = sum(item['total'] for item in self.cart_items)
            self.cursor.execute("""
                INSERT INTO orders (client_id, pay_method_id, date, total_sum)
                VALUES (%s, 1, NOW(), %s)
                RETURNING order_id;
            """, (client_id, total_sum))
            order_id = self.cursor.fetchone()[0]
            for item in self.cart_items:
                self.cursor.execute("""
                    INSERT INTO order_info (order_id, product_id, quantity)
                    VALUES (%s, %s, %s);
                """, (order_id, item['product_id'], item['quantity']))
                self.cursor.execute("""
                    UPDATE product 
                    SET stock = stock - %s 
                    WHERE product_id = %s;
                """, (item['quantity'], item['product_id']))
            self.conn.commit()
            messagebox.showinfo("Успех",
                                f"Заказ успешно оформлен!\n"
                                f"Номер заказа: {order_id}\n"
                                f"Клиент: {client_name}\n"
                                f"Сумма: ₽{total_sum:,.2f}")
            self.cart_items = []
            for item in self.cart_tree.get_children():
                self.cart_tree.delete(item)
            self.update_cart_total()
            self.client_name_entry.delete(0, tk.END)
            self.client_phone_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось оформить заказ: {str(e)}")
            self.conn.rollback()

    def show_orders(self):
        self.clear_content()
        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(title_frame, text="Заказы",
                 font=("Arial", 24, "bold"),
                 bg='white', fg=self.colors['dark']).pack(side=tk.LEFT)
        control_frame = tk.Frame(self.content_area, bg='white')
        control_frame.pack(fill=tk.X, padx=30, pady=10)
        refresh_btn = tk.Button(control_frame, text="🔄 Обновить",
                                command=self.refresh_products,
                                bg=self.colors['primary'], fg='white',
                                font=("Arial", 11),
                                relief=tk.FLAT, padx=20, pady=8,
                                cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=5)
        if self.user_role in ['admin', 'seller']:
            delete_btn = tk.Button(control_frame, text="🗑️ Удалить выбранный заказ",
                                   command=lambda: self.delete_selected_record('orders', 'order_id'),
                                   bg=self.colors['danger'], fg='white',
                                   font=("Arial", 11),
                                   relief=tk.FLAT, padx=20, pady=8,
                                   cursor="hand2")
            delete_btn.pack(side=tk.LEFT, padx=5)
        table_frame = tk.Frame(self.content_area, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        self.load_orders_table(table_frame)
    def load_orders_table(self, parent):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM orders;")
            order_count = self.cursor.fetchone()[0]
            if order_count == 0:
                no_orders_label = tk.Label(parent,
                                           text="Нет заказов. Создайте первый заказ через раздел '🛒 Новый заказ'.",
                                           font=("Arial", 14), bg='white', fg='blue')
                no_orders_label.pack(pady=50)
                return
            try:
                self.cursor.execute("""
                    SELECT o.order_id, 
                           COALESCE(c.surname || ' ', '') || c.name as client, 
                           o.date, 
                           o.total_sum,
                           (SELECT STRING_AGG(p.name || ' (x' || oi.quantity || ')', ', ')
                            FROM order_info oi
                            JOIN product p ON oi.product_id = p.product_id
                            WHERE oi.order_id = o.order_id) as products
                    FROM orders o
                    LEFT JOIN client c ON o.client_id = c.client_id
                    ORDER BY o.date DESC;
                """)
            except Exception as join_error:
                print(f"Ошибка JOIN запроса: {join_error}")
                self.cursor.execute("""
                    SELECT o.order_id, 
                           'Клиент #' || o.client_id as client,
                           o.date, 
                           o.total_sum,
                           (SELECT STRING_AGG(p.name || ' (x' || oi.quantity || ')', ', ')
                            FROM order_info oi
                            JOIN product p ON oi.product_id = p.product_id
                            WHERE oi.order_id = o.order_id) as products
                    FROM orders o
                    ORDER BY o.date DESC;
                """)
            orders = self.cursor.fetchall()
            columns = ('ID', 'Клиент', 'Дата', 'Сумма', 'Товары')
            self.orders_tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
            column_widths = [50, 150, 150, 100, 300]
            for i, col in enumerate(columns):
                self.orders_tree.heading(col, text=col)
                self.orders_tree.column(col, width=column_widths[i])
            for order in orders:
                order_list = list(order)
                order_list[2] = order_list[2].strftime('%Y-%m-%d %H:%M') if order_list[2] else 'Нет даты'
                order_list[3] = f"₽{float(order_list[3] or 0):,.2f}"
                if order_list[4] and len(str(order_list[4])) > 100:
                    order_list[4] = str(order_list[4])[:100] + "..."
                elif not order_list[4]:
                    order_list[4] = "Нет товаров"
                self.orders_tree.insert('', tk.END, values=order_list)
            scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.orders_tree.yview)
            self.orders_tree.configure(yscroll=scrollbar.set)
            self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        except Exception as e:
            print(f"Полная ошибка загрузки заказов: {e}")
            try:
                self.cursor.execute("SELECT order_id, date, total_sum FROM orders ORDER BY date DESC;")
                simple_orders = self.cursor.fetchall()
                if simple_orders:
                    columns = ('ID', 'Дата', 'Сумма')
                    self.orders_tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
                    for col in columns:
                        self.orders_tree.heading(col, text=col)
                        self.orders_tree.column(col, width=150)
                    for order in simple_orders:
                        order_list = list(order)
                        order_list[1] = order_list[1].strftime('%Y-%m-%d %H:%M') if order_list[1] else 'Нет даты'
                        order_list[2] = f"₽{float(order_list[2] or 0):,.2f}"
                        self.orders_tree.insert('', tk.END, values=order_list)
                    scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.orders_tree.yview)
                    self.orders_tree.configure(yscroll=scrollbar.set)
                    self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                else:
                    no_orders_label = tk.Label(parent,
                                               text="Нет заказов в базе данных.",
                                               font=("Arial", 14), bg='white', fg='red')
                    no_orders_label.pack(pady=50)

            except Exception as e2:
                error_label = tk.Label(parent,
                                       text=f"Критическая ошибка загрузки заказов: {str(e2)}",
                                       font=("Arial", 12), bg='white', fg='red')
                error_label.pack(pady=50)

    def show_cash_register(self):
        if self.user_role != 'seller':
            messagebox.showwarning("Доступ запрещен", "Эта функция доступна только продавцам!")
            return
        self.clear_content()
        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(title_frame, text="Касса",
                 font=("Arial", 24, "bold"),
                 bg='white', fg=self.colors['dark']).pack(side=tk.LEFT)
        stats_frame = tk.Frame(self.content_area, bg='white')
        stats_frame.pack(fill=tk.X, padx=30, pady=10)
        try:
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as orders_count,
                    COALESCE(SUM(total_sum), 0) as total_sum,
                    COALESCE(AVG(total_sum), 0) as avg_sum
                FROM orders 
                WHERE DATE(date) = CURRENT_DATE;
            """)
            today_stats = self.cursor.fetchone()
            stats_data = [
                ("📅 Заказов сегодня", today_stats[0], "#3498db"),
                ("💰 Выручка сегодня", f"₽{float(today_stats[1]):,.2f}", "#2ecc71"),
                ("📊 Средний чек", f"₽{float(today_stats[2]):,.2f}", "#9b59b6")
            ]
            for i, (title, value, color) in enumerate(stats_data):
                stat_frame = tk.Frame(stats_frame, bg=color, relief=tk.RAISED, bd=0)
                stat_frame.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
                tk.Label(stat_frame, text=title, bg=color, fg='white',
                         font=("Arial", 11)).pack(pady=(15, 5))
                tk.Label(stat_frame, text=str(value), bg=color, fg='white',
                         font=("Arial", 20, "bold")).pack(pady=(5, 15))
                stats_frame.columnconfigure(i, weight=1, uniform="cash_stats")
        except Exception as e:
            tk.Label(stats_frame, text=f"Ошибка загрузки статистики: {str(e)}",
                     font=("Arial", 12), bg='white').pack()

    def show_finance(self):
        if self.user_role != 'accountant':
            messagebox.showwarning("Доступ запрещен", "Эта функция доступна только бухгалтерам!")
            return
        self.clear_content()
        # Заголовок
        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(title_frame, text="Финансы",
                 font=("Arial", 24, "bold"),
                 bg='white', fg=self.colors['dark']).pack(side=tk.LEFT)
        notebook = ttk.Notebook(self.content_area)
        notebook.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        stats_tab = ttk.Frame(notebook)
        notebook.add(stats_tab, text="Общая статистика")
        self.show_finance_stats(stats_tab)
        orders_tab = ttk.Frame(notebook)
        notebook.add(orders_tab, text="Отчет по заказам")
        self.show_finance_orders(orders_tab)
        export_tab = ttk.Frame(notebook)
        notebook.add(export_tab, text="Экспорт в Excel")
        self.show_excel_export(export_tab)

    def show_finance_stats(self, parent):
        try:
            self.cursor.execute("""
                SELECT 
                    EXTRACT(YEAR FROM date) as year,
                    EXTRACT(MONTH FROM date) as month,
                    COUNT(*) as orders_count,
                    SUM(total_sum) as revenue
                FROM orders
                GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
                ORDER BY year DESC, month DESC
                LIMIT 6;
            """)
            monthly_stats = self.cursor.fetchall()
            try:
                self.cursor.execute("""
                    SELECT 
                        COALESCE(SUM(o.total_sum), 0) as revenue,
                        COALESCE(SUM(p.purch_price * oi.quantity), 0) as cost,
                        COALESCE(SUM(o.total_sum - (p.purch_price * oi.quantity)), 0) as profit
                    FROM orders o, order_info oi, product p
                    WHERE o.order_id = oi.order_id 
                    AND oi.product_id = p.product_id
                """)
                profit_stats = self.cursor.fetchone()
            except Exception as e:
                print(f"Ошибка при расчете прибыли в финансах: {e}")
                profit_stats = (0, 0, 0)
            report_text = "ФИНАНСОВЫЙ ОТЧЕТ\n"
            report_text += "=" * 50 + "\n\n"
            if profit_stats and profit_stats[0]:
                report_text += f"Общая выручка: ₽{profit_stats[0]:,.2f}\n"
                report_text += f"Себестоимость: ₽{profit_stats[1]:,.2f}\n"
                report_text += f"Прибыль: ₽{profit_stats[2]:,.2f}\n\n"
            report_text += "Выручка по месяцам:\n"
            report_text += "-" * 40 + "\n"
            for year, month, count, revenue in monthly_stats:
                report_text += f"{int(year)}-{int(month):02d}: {count} зак. = ₽{revenue:,.2f}\n"
            text_widget = scrolledtext.ScrolledText(parent, width=80, height=30, font=("Consolas", 10))
            text_widget.insert(1.0, report_text)
            text_widget.config(state=tk.DISABLED)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        except Exception as e:
            error_label = tk.Label(parent, text=f"Ошибка загрузки статистики: {str(e)}",
                                   font=("Arial", 12))
            error_label.pack(pady=50)

    def show_finance_orders(self, parent):
        try:
            self.cursor.execute("""
                SELECT o.order_id, 
                       COALESCE(c.surname || ' ', '') || c.name as client, 
                       o.date, 
                       o.total_sum,
                       (SELECT STRING_AGG(p.name || ' (x' || oi.quantity || ')', ', ')
                        FROM order_info oi
                        JOIN product p ON oi.product_id = p.product_id
                        WHERE oi.order_id = o.order_id) as products,
                       pm.name as payment_method
                FROM orders o
                JOIN client c ON o.client_id = c.client_id
                LEFT JOIN pay_method pm ON o.pay_method_id = pm.pay_method_id
                ORDER BY o.date DESC
                LIMIT 50;
            """)
            orders = self.cursor.fetchall()
            if orders:
                columns = ('ID', 'Клиент', 'Дата', 'Сумма', 'Товары', 'Оплата')
                tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=120)
                for order in orders:
                    order_list = list(order)
                    order_list[2] = order_list[2].strftime('%Y-%m-%d %H:%M')
                    order_list[3] = f"₽{float(order_list[3]):,.2f}"
                    if order_list[4] and len(order_list[4]) > 50:
                        order_list[4] = order_list[4][:50] + "..."
                    tree.insert('', tk.END, values=order_list)
                scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                info_label = tk.Label(parent,
                                      text="Нет данных о заказах\nСоздайте несколько заказов через раздел 'Новый заказ'",
                                      font=("Arial", 14), fg='blue')
                info_label.pack(pady=50)
        except Exception as e:
            try:
                self.cursor.execute("""
                    SELECT o.order_id, 
                           COALESCE(c.surname || ' ', '') || c.name as client, 
                           o.date, 
                           o.total_sum,
                           pm.name as payment_method
                    FROM orders o
                    JOIN client c ON o.client_id = c.client_id
                    LEFT JOIN pay_method pm ON o.pay_method_id = pm.pay_method_id
                    ORDER BY o.date DESC
                    LIMIT 50;
                """)
                orders = self.cursor.fetchall()
                if orders:
                    columns = ('ID', 'Клиент', 'Дата', 'Сумма', 'Оплата')
                    tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
                    for col in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=120)
                    for order in orders:
                        order_list = list(order)
                        order_list[2] = order_list[2].strftime('%Y-%m-%d %H:%M')
                        order_list[3] = f"₽{float(order_list[3]):,.2f}"
                        tree.insert('', tk.END, values=order_list)
                    scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
                    tree.configure(yscroll=scrollbar.set)
                    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            except Exception as e2:
                error_label = tk.Label(parent, text=f"Ошибка загрузки заказов: {str(e2)}",
                                       font=("Arial", 12), fg='red')
                error_label.pack(pady=50)

    def show_excel_export(self, parent):
        export_frame = tk.Frame(parent, bg='white')
        export_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(export_frame, text="Экспорт данных в Excel",
                 font=("Arial", 18, "bold"),
                 bg='white').pack(pady=20)
        export_options = [
            ("📊 Экспорт продаж", self.export_sales_to_excel),
            ("💰 Экспорт финансов", self.export_finance_to_excel),
            ("📦 Экспорт товаров", self.export_products_to_excel),
            ("👥 Экспорт клиентов", self.export_clients_to_excel),
            ("📋 Экспорт заказов", self.export_orders_to_excel)
        ]
        for i, (text, command) in enumerate(export_options):
            btn = tk.Button(export_frame, text=text, command=command,
                            bg=self.colors['primary'], fg='white',
                            font=("Arial", 12),
                            relief=tk.FLAT, padx=30, pady=15,
                            cursor="hand2")
            btn.pack(pady=10, fill=tk.X)

    def export_sales_to_excel(self):
        try:
            self.cursor.execute("""
                SELECT DATE(date) as sale_date,
                       COUNT(*) as orders_count,
                       SUM(total_sum) as total_revenue
                FROM orders
                GROUP BY DATE(date)
                ORDER BY sale_date DESC;
            """)
            sales_data = self.cursor.fetchall()
            if not sales_data:
                messagebox.showinfo("Информация", "Нет данных для экспорта!")
                return
            df = pd.DataFrame(sales_data, columns=['Дата', 'Количество заказов', 'Выручка'])
            df['Дата'] = pd.to_datetime(df['Дата']).dt.strftime('%Y-%m-%d')
            df['Выручка'] = df['Выручка'].apply(lambda x: f"₽{x:,.2f}")
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"sales_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            if filename:
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Продажи', index=False)
                    worksheet = writer.sheets['Продажи']
                    worksheet.column_dimensions['A'].width = 15
                    worksheet.column_dimensions['B'].width = 20
                    worksheet.column_dimensions['C'].width = 20
                messagebox.showinfo("Успех", f"Данные экспортированы в:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def export_finance_to_excel(self):
        try:
            self.cursor.execute("""
                SELECT 
                    EXTRACT(YEAR FROM date) as year,
                    EXTRACT(MONTH FROM date) as month,
                    COUNT(*) as orders_count,
                    SUM(total_sum) as revenue
                FROM orders
                WHERE date >= CURRENT_DATE - INTERVAL '12 months'
                GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
                ORDER BY year, month;
            """)
            finance_data = self.cursor.fetchall()
            if not finance_data:
                messagebox.showinfo("Информация", "Нет данных для экспорта!")
                return
            df = pd.DataFrame(finance_data, columns=['Год', 'Месяц', 'Количество заказов', 'Выручка'])
            df['Месяц_название'] = df['Месяц'].apply(lambda x: [
                'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
            ][int(x) - 1])
            df['Период'] = df['Год'].astype(int).astype(str) + '-' + df['Месяц'].astype(int).astype(str).str.zfill(2)
            df['Выручка'] = df['Выручка'].apply(lambda x: f"₽{x:,.2f}")
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"finance_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            if filename:
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df[['Период', 'Месяц_название', 'Количество заказов', 'Выручка']].to_excel(
                        writer, sheet_name='Финансы', index=False)
                    worksheet = writer.sheets['Финансы']
                    worksheet.column_dimensions['A'].width = 12
                    worksheet.column_dimensions['B'].width = 15
                    worksheet.column_dimensions['C'].width = 20
                    worksheet.column_dimensions['D'].width = 20
                messagebox.showinfo("Успех", f"Данные экспортированы в:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def export_products_to_excel(self):
        try:
            self.cursor.execute("""
                SELECT p.product_id, p.name, c.name as category, 
                       m.name as manufacturer, p.stock, 
                       p.purch_price, p.sale_price
                FROM product p
                LEFT JOIN cat c ON p.cat_id = c.cat_id
                LEFT JOIN manufacturer m ON p.manufacturer_id = m.manufacturer_id
                ORDER BY p.product_id;
            """)
            products_data = self.cursor.fetchall()
            if not products_data:
                messagebox.showinfo("Информация", "Нет данных для экспорта!")
                return
            df = pd.DataFrame(products_data, columns=[
                'ID', 'Название', 'Категория', 'Производитель',
                'Остаток', 'Цена закупки', 'Цена продажи'
            ])
            df['Цена закупки'] = df['Цена закупки'].apply(lambda x: f"₽{x:,.2f}")
            df['Цена продажи'] = df['Цена продажи'].apply(lambda x: f"₽{x:,.2f}")
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"products_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            if filename:
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Товары', index=False)
                    worksheet = writer.sheets['Товары']
                    for col in worksheet.columns:
                        max_length = 0
                        column = col[0].column_letter
                        for cell in col:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column].width = adjusted_width
                messagebox.showinfo("Успех", f"Данные экспортированы в:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def export_clients_to_excel(self):
        try:
            self.cursor.execute("""
                SELECT c.client_id, c.surname, c.name, c.phone, c.email,
                       COUNT(o.order_id) as orders_count,
                       COALESCE(SUM(o.total_sum), 0) as total_spent
                FROM client c
                LEFT JOIN orders o ON c.client_id = o.client_id
                GROUP BY c.client_id, c.surname, c.name, c.phone, c.email
                ORDER BY total_spent DESC;
            """)
            clients_data = self.cursor.fetchall()
            if not clients_data:
                messagebox.showinfo("Информация", "Нет данных для экспорта!")
                return
            df = pd.DataFrame(clients_data, columns=[
                'ID', 'Фамилия', 'Имя', 'Телефон', 'Email',
                'Количество заказов', 'Всего потрачено'
            ])
            df['Всего потрачено'] = df['Всего потрачено'].apply(lambda x: f"₽{x:,.2f}")
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"clients_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            if filename:
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Клиенты', index=False)
                    worksheet = writer.sheets['Клиенты']
                    for i, col in enumerate(df.columns):
                        column_letter = chr(65 + i)
                        worksheet.column_dimensions[column_letter].width = 20
                messagebox.showinfo("Успех", f"Данные экспортированы в:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def export_orders_to_excel(self):
        try:
            self.cursor.execute("""
                SELECT o.order_id, 
                       COALESCE(c.surname || ' ', '') || c.name as client, 
                       o.date, 
                       o.total_sum,
                       pm.name as payment_method
                FROM orders o
                JOIN client c ON o.client_id = c.client_id
                LEFT JOIN pay_method pm ON o.pay_method_id = pm.pay_method_id
                WHERE o.date >= CURRENT_DATE - INTERVAL '30 days'
                ORDER BY o.date DESC;
            """)
            orders_data = self.cursor.fetchall()
            if not orders_data:
                messagebox.showinfo("Информация", "Нет данных для экспорта!")
                return
            df = pd.DataFrame(orders_data, columns=[
                'ID', 'Клиент', 'Дата', 'Сумма', 'Способ оплаты'
            ])
            df['Дата'] = pd.to_datetime(df['Дата']).dt.strftime('%Y-%m-%d %H:%M')
            df['Сумма'] = df['Сумма'].apply(lambda x: f"₽{x:,.2f}")
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"orders_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            if filename:
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Заказы', index=False)
                    worksheet = writer.sheets['Заказы']
                    worksheet.column_dimensions['A'].width = 10
                    worksheet.column_dimensions['B'].width = 25
                    worksheet.column_dimensions['C'].width = 20
                    worksheet.column_dimensions['D'].width = 15
                    worksheet.column_dimensions['E'].width = 20
                messagebox.showinfo("Успех", f"Данные экспортированы в:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def show_reports(self):
        self.clear_content()
        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(title_frame, text="Отчеты",
                 font=("Arial", 24, "bold"),
                 bg='white', fg=self.colors['dark']).pack(side=tk.LEFT)
        reports_frame = tk.Frame(self.content_area, bg='white')
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        if self.user_role == 'admin':
            reports = [
                ("📊 Отчет по продажам", self.generate_sales_report),
                ("📦 Отчет по товарам", self.generate_products_report),
                ("👥 Отчет по клиентам", self.generate_clients_report),
                ("💰 Финансовый отчет", self.generate_financial_report),
                ("📋 Экспорт в Excel", self.show_excel_export_tab)
            ]
        elif self.user_role == 'accountant':
            reports = [
                ("📊 Отчет по продажам", self.generate_sales_report),
                ("💰 Финансовый отчет", self.generate_financial_report),
                ("📦 Отчет по остаткам", self.generate_stock_report),
                ("📋 Экспорт в Excel", self.show_excel_export_tab)
            ]
        else:
            reports = [
                ("📊 Отчет по продажам", self.generate_sales_report),
                ("📦 Отчет по остаткам", self.generate_stock_report)
            ]
        for i, (text, command) in enumerate(reports):
            btn = tk.Button(reports_frame, text=text, command=command,
                            bg=self.colors['primary'], fg='white',
                            font=("Arial", 12),
                            relief=tk.FLAT, padx=30, pady=20,
                            cursor="hand2")
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky='nsew')
            reports_frame.columnconfigure(i % 2, weight=1)
            reports_frame.rowconfigure(i // 2, weight=1)

    def show_excel_export_tab(self):
        self.show_finance()

    def generate_sales_report(self):
        try:
            self.cursor.execute("""
                SELECT DATE(date) as sale_date,
                       COUNT(*) as orders_count,
                       SUM(total_sum) as total_revenue
                FROM orders
                GROUP BY DATE(date)
                ORDER BY sale_date DESC
                LIMIT 30;
            """)
            sales_data = self.cursor.fetchall()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"sales_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Дата', 'Количество заказов', 'Выручка'])
                    for row in sales_data:
                        writer.writerow([row[0], row[1], f"₽{row[2]:,.2f}"])
                messagebox.showinfo("Успех", f"Отчет сохранен:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {str(e)}")

    def generate_products_report(self):
        try:
            self.cursor.execute("""
                SELECT p.name, c.name as category, 
                       p.stock, p.purch_price, p.sale_price
                FROM product p
                LEFT JOIN cat c ON p.cat_id = c.cat_id
                ORDER BY p.name;
            """)
            products_data = self.cursor.fetchall()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"products_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Название', 'Категория', 'Остаток', 'Цена закупки', 'Цена продажи'])
                    for row in products_data:
                        writer.writerow([row[0], row[1], row[2], row[3], row[4]])
                messagebox.showinfo("Успех", f"Отчет сохранен:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {str(e)}")

    def generate_clients_report(self):
        try:
            self.cursor.execute("""
                SELECT c.name, c.phone, c.email,
                       COUNT(o.order_id) as orders_count,
                       SUM(o.total_sum) as total_spent
                FROM client c
                LEFT JOIN orders o ON c.client_id = o.client_id
                GROUP BY c.client_id, c.name, c.phone, c.email
                ORDER BY total_spent DESC NULLS LAST;
            """)
            clients_data = self.cursor.fetchall()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"clients_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Имя', 'Телефон', 'Email', 'Количество заказов', 'Всего потрачено'])
                    for row in clients_data:
                        writer.writerow([row[0], row[1] or '', row[2] or '', row[3] or 0, row[4] or 0])
                messagebox.showinfo("Успех", f"Отчет сохранен:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {str(e)}")

    def generate_financial_report(self):
        try:
            self.cursor.execute("""
                SELECT EXTRACT(MONTH FROM date) as month,
                       COUNT(*) as orders_count,
                       SUM(total_sum) as revenue
                FROM orders
                GROUP BY EXTRACT(MONTH FROM date)
                ORDER BY month;
            """)
            financial_data = self.cursor.fetchall()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"financial_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Месяц', 'Количество заказов', 'Выручка'])
                    for row in financial_data:
                        writer.writerow([f"Месяц {int(row[0])}", row[1], row[2]])
                messagebox.showinfo("Успех", f"Отчет сохранен:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {str(e)}")

    def generate_stock_report(self):
        try:
            self.cursor.execute("""
                SELECT p.name, c.name as category, 
                       p.stock, p.sale_price,
                       CASE 
                           WHEN p.stock = 0 THEN 'Нет в наличии'
                           WHEN p.stock < 5 THEN 'Мало'
                           ELSE 'Достаточно'
                       END as status
                FROM product p
                LEFT JOIN cat c ON p.cat_id = c.cat_id
                ORDER BY p.stock, p.name;
            """)
            stock_data = self.cursor.fetchall()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"stock_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Название', 'Категория', 'Остаток', 'Цена', 'Статус'])
                    for row in stock_data:
                        writer.writerow([row[0], row[1], row[2], row[3], row[4]])
                messagebox.showinfo("Успех", f"Отчет сохранен:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {str(e)}")

    def show_admin_panel(self):
        if self.user_role != 'admin':
            messagebox.showwarning("Доступ запрещен", "Эта функция доступна только администраторам!")
            return
        self.clear_content()
        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(title_frame, text="Администрирование",
                 font=("Arial", 24, "bold"),
                 bg='white', fg=self.colors['dark']).pack(side=tk.LEFT)
        tools_frame = tk.Frame(self.content_area, bg='white')
        tools_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        admin_tools = [
            ("👥 Управление пользователями", self.manage_users),
            ("📊 Системная информация", self.system_info),
            ("📋 Просмотр всех заказов", self.show_all_orders_admin),
        ]
        for i, (text, command) in enumerate(admin_tools):
            btn = tk.Button(tools_frame, text=text, command=command,
                            bg=self.colors['primary'], fg='white',
                            font=("Arial", 12),
                            relief=tk.FLAT, padx=30, pady=20,
                            cursor="hand2")
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky='nsew')
            tools_frame.columnconfigure(i % 2, weight=1)
            tools_frame.rowconfigure(i // 2, weight=1)

    def show_all_orders_admin(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Все заказы - Администратор")
        dialog.geometry("1200x700")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        tk.Label(dialog, text="Все заказы",
                 font=("Arial", 18, "bold"),
                 bg='white').pack(pady=20)
        control_frame = tk.Frame(dialog, bg='white')
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        refresh_btn = tk.Button(control_frame, text="🔄 Обновить",
                                command=lambda: self.refresh_admin_orders(table_frame),
                                bg=self.colors['primary'], fg='white',
                                font=("Arial", 11),
                                relief=tk.FLAT, padx=20, pady=8,
                                cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=5)
        delete_btn = tk.Button(control_frame, text="🗑️ Удалить выбранный",
                               command=lambda: self.delete_admin_order(table_frame),
                               bg=self.colors['danger'], fg='white',
                               font=("Arial", 11),
                               relief=tk.FLAT, padx=20, pady=8,
                               cursor="hand2")
        delete_btn.pack(side=tk.LEFT, padx=5)
        table_frame = tk.Frame(dialog, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.load_admin_orders_table(table_frame)

    def load_admin_orders_table(self, parent):
        try:
            self.cursor.execute("""
                SELECT o.order_id, 
                       COALESCE(c.surname || ' ', '') || c.name as client,
                       c.phone as client_phone,
                       o.date, 
                       o.total_sum,
                       pm.name as payment_method
                FROM orders o
                JOIN client c ON o.client_id = c.client_id
                LEFT JOIN pay_method pm ON o.pay_method_id = pm.pay_method_id
                ORDER BY o.date DESC;
            """)
            orders = self.cursor.fetchall()
            columns = ('ID', 'Клиент', 'Телефон', 'Дата', 'Сумма', 'Оплата')
            tree = ttk.Treeview(parent, columns=columns, show='headings', height=25)
            column_widths = [50, 150, 120, 150, 100, 100]
            for i, col in enumerate(columns):
                tree.heading(col, text=col)
                tree.column(col, width=column_widths[i])
            for order in orders:
                order_list = list(order)
                order_list[3] = order_list[3].strftime('%Y-%m-%d %H:%M')
                order_list[4] = f"₽{float(order_list[4]):,.2f}"
                tree.insert('', tk.END, values=order_list)
            scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.admin_orders_tree = tree
        except Exception as e:
            error_label = tk.Label(parent, text=f"Ошибка загрузки заказов: {str(e)}",
                                   font=("Arial", 12), bg='white', fg='red')
            error_label.pack(pady=50)

    def refresh_admin_orders(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()
        self.load_admin_orders_table(parent)

    def delete_admin_order(self, parent):
        if not hasattr(self, 'admin_orders_tree'):
            messagebox.showwarning("Предупреждение", "Таблица не загружена!")
            return
        selected_items = self.admin_orders_tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите заказ для удаления!")
            return
        item = self.admin_orders_tree.item(selected_items[0])
        order_id = item['values'][0]
        client_name = item['values'][1]
        if messagebox.askyesno("Подтверждение удаления",
                               f"Вы уверены, что хотите удалить заказ №{order_id}?\n"
                               f"Клиент: {client_name}\n\n"
                               f"Это действие нельзя отменить!"):
            if self.delete_record('orders', order_id, 'order_id'):
                self.admin_orders_tree.delete(selected_items[0])

    def manage_users(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Управление пользователями")
        dialog.geometry("800x500")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        tk.Label(dialog, text="Управление пользователями",
                 font=("Arial", 18, "bold"),
                 bg='white').pack(pady=20)
        table_frame = tk.Frame(dialog, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        try:
            self.cursor.execute("""
                SELECT user_id, username, role, full_name, created_at
                FROM users
                ORDER BY user_id;
            """)
            users = self.cursor.fetchall()
            columns = ('ID', 'Логин', 'Роль', 'Полное имя', 'Создан')
            tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)
            for user in users:
                user_list = list(user)
                user_list[4] = user_list[4].strftime('%Y-%m-%d %H:%M')
                tree.insert('', tk.END, values=user_list)
            scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        except Exception as e:
            tk.Label(table_frame, text=f"Ошибка загрузки пользователей: {str(e)}",
                     font=("Arial", 12), bg='white').pack(pady=50)

    def system_info(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Системная информация")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        info_text = f"""
        гитар шоп йомайо))

        ====================

        Пользователь: {self.current_user['full_name']}
        Роль: {self.user_role}

        База данных: {self.db_connection_params['database']}
        Сервер: {self.db_connection_params['host']}:{self.db_connection_params['port']}

        Python: {sys.version.split()[0]}
        """
        text_widget = scrolledtext.ScrolledText(dialog, width=50, height=20, font=("Consolas", 10))
        text_widget.insert(1.0, info_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(padx=20, pady=20)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def logout(self):
        if self.conn:
            try:
                self.cursor.close()
                self.conn.close()
            except:
                pass
        self.conn = None
        self.cursor = None
        self.user_role = None
        self.current_user = None
        self.show_database_setup_screen()

    def find_treeview_in_content(self, table_name):
        try:
            for widget in self.content_area.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Treeview):
                            items = child.get_children()
                            if items:
                                first_item = child.item(items[0])
                                values = first_item['values']
                                if values and len(values) > 0:
                                    if values[0] > 0:
                                        return child
            return None
        except:
            return None


def main():
    root = tk.Tk()
    app = shop_system(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        import psycopg2
        import pandas as pd
        from openpyxl import Workbook
    except ImportError as e:
        print("Ошибка: Не установлены необходимые библиотеки")
        print("Установите их с помощью команд:")
        print("pip install psycopg2-binary pandas openpyxl")
        print(f"Текущая ошибка: {e}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    main()
