import tkinter as tk
from tkinter import ttk, messagebox

import fields
import psycopg2
from datetime import datetime

import row


class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Риэлторское агентство - Управление базой данных")
        self.root.geometry("1200x700")

        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Устанавливаем размеры окна в зависимости от разрешения экрана
        if screen_width >= 1920 and screen_height >= 1080:  # Full HD и выше
            window_width = int(screen_width * 0.8)
            window_height = int(screen_height * 0.8)
        elif screen_width >= 1366 and screen_height >= 768:  # HD
            window_width = int(screen_width * 0.85)
            window_height = int(screen_height * 0.85)
        else:  # Низкое разрешение
            window_width = int(screen_width * 0.9)
            window_height = int(screen_height * 0.9)

        # Центрируем окно
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Минимальный размер окна
        self.root.minsize(800, 600)

        # Параметры подключения к БД
        self.conn_params = {
            'dbname': 'agency',
            'user': 'postgres',
            'password': '07072006',
            'host': 'localhost',
            'port': '5432'
        }

        self.conn = None
        self.connect_db()

        # Переменные для адаптивности
        self.font_size = self.calculate_font_size(window_width)
        self.padding = self.calculate_padding(window_width)
        self.button_width = self.calculate_button_width(window_width)

        self.create_widgets()
        self.load_employees()

        # Привязываем обработчик изменения размера окна
        self.root.bind('<Configure>', self.on_window_resize)

    def calculate_font_size(self, window_width):
        """Рассчитать размер шрифта в зависимости от ширины окна"""
        if window_width >= 1600:
            return 12
        elif window_width >= 1200:
            return 11
        elif window_width >= 900:
            return 10
        else:
            return 9

    def calculate_padding(self, window_width):
        """Рассчитать отступы в зависимости от ширины окна"""
        if window_width >= 1600:
            return 15
        elif window_width >= 1200:
            return 12
        elif window_width >= 900:
            return 10
        else:
            return 8

    def calculate_button_width(self, window_width):
        """Рассчитать ширину кнопок в зависимости от ширины окна"""
        if window_width >= 1600:
            return 25
        elif window_width >= 1200:
            return 22
        elif window_width >= 900:
            return 20
        else:
            return 18

    def on_window_resize(self, event):
        """Обработчик изменения размера окна"""
        if event.widget == self.root:
            # Обновляем размеры и перерисовываем интерфейс
            self.update_ui_sizes()

    def update_ui_sizes(self):
        """Обновить размеры элементов интерфейса"""
        window_width = self.root.winfo_width()

        # Обновляем размеры
        self.font_size = self.calculate_font_size(window_width)
        self.padding = self.calculate_padding(window_width)
        self.button_width = self.calculate_button_width(window_width)

        # Обновляем стили
        self.update_styles()

        # Обновляем размеры виджетов
        self.update_widget_sizes()

    def update_styles(self):
        """Обновить стили элементов"""
        style = ttk.Style()

        # Настраиваем стили для кнопок
        style.configure('TButton',
                        font=('Arial', self.font_size),
                        padding=self.padding // 2)

        style.configure('TLabel',
                        font=('Arial', self.font_size))

        style.configure('Treeview.Heading',
                        font=('Arial', self.font_size, 'bold'))

        style.configure('Treeview',
                        font=('Arial', self.font_size - 1 if self.font_size > 9 else 9))

        style.configure('Title.TLabel',
                        font=('Arial', self.font_size + 2, 'bold'))

    def update_widget_sizes(self):
        """Обновить размеры виджетов"""
        # Обновляем размеры кнопок
        for widget in self.buttons_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.configure(width=self.button_width)

        # Обновляем размеры колонок в Treeview
        if hasattr(self, 'tree'):
            self.adjust_treeview_columns()

    def connect_db(self):
        """Подключение к базе данных"""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("Подключение к БД успешно")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться к БД:\n{str(e)}")
            self.root.destroy()

    def execute_query(self, query, params=None, fetch=False):
        """Выполнение SQL запроса"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                else:
                    self.conn.commit()
                    return cur.rowcount
        except Exception as e:
            messagebox.showerror("Ошибка запроса", str(e))
            return None

    def create_widgets(self):
        """Создание адаптивных виджетов"""
        # Основной контейнер
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Настраиваем веса для адаптивности
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(1, weight=1)

        # Заголовок
        self.title_label = ttk.Label(
            self.main_container,
            text="📊 Управление базой данных риэлторского агентства",
            style='Title.TLabel'
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, self.padding))

        # Фрейм для кнопок навигации
        self.buttons_frame = ttk.Frame(self.main_container)
        self.buttons_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=(0, self.padding))

        # Список кнопок навигации
        self.nav_buttons = [
            ("👥 Сотрудники", self.show_employees),
            ("👤 Клиенты", self.show_clients),
            ("🏠 Объекты", self.show_properties),
            ("💰 Сделки", self.show_deals),
            ("👁️ Просмотры", self.show_viewings),
            ("🔧 Услуги", self.show_services),
            ("📈 Отчеты", self.show_reports),
        ]

        for i, (text, command) in enumerate(self.nav_buttons):
            btn = ttk.Button(
                self.buttons_frame,
                text=text,
                command=command,
                width=self.button_width
            )
            btn.pack(pady=5, fill=tk.X)

        # Фрейм для отображения данных
        self.data_container = ttk.Frame(self.main_container)
        self.data_container.grid(row=1, column=1, sticky=tk.NSEW)

        # Настраиваем веса внутри контейнера данных
        self.data_container.columnconfigure(0, weight=1)
        self.data_container.rowconfigure(0, weight=1)

        # Treeview для отображения таблиц
        self.tree_frame = ttk.Frame(self.data_container)
        self.tree_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)

        # Создаем Treeview с полосой прокрутки
        self.create_treeview()

        # Панель управления
        self.control_frame = ttk.Frame(self.main_container)
        self.control_frame.grid(row=2, column=0, columnspan=2, pady=(self.padding, 0), sticky=tk.EW)

        # Кнопки управления
        control_buttons = [
            ("➕ Добавить", self.add_record),
            ("✏️ Редактировать", self.edit_record),  # НОВАЯ КНОПКА
            ("🗑️ Удалить", self.delete_record),
            ("🔄 Обновить", self.refresh_data),
            ("🔍 Поиск", self.search_dialog),
        ]

        for i, (text, command) in enumerate(control_buttons):
            btn = ttk.Button(
                self.control_frame,
                text=text,
                command=command,
                width=self.button_width - 5
            )
            btn.pack(side=tk.LEFT, padx=5)
        # Статус бар
        self.status_frame = ttk.Frame(self.main_container)
        self.status_frame.grid(row=3, column=0, columnspan=2, pady=(self.padding, 0), sticky=tk.EW)

        self.status_var = tk.StringVar(value="Готово")
        self.status_label = ttk.Label(
            self.status_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Arial', self.font_size - 1)
        )
        self.status_label.pack(fill=tk.X, ipady=2)

        # Информация о записях
        self.info_var = tk.StringVar(value="")
        self.info_label = ttk.Label(
            self.status_frame,
            textvariable=self.info_var,
            relief=tk.SUNKEN,
            anchor=tk.E,
            font=('Arial', self.font_size - 1)
        )
        self.info_label.pack(fill=tk.X, ipady=2)

        # Применяем стили
        self.update_styles()

        # Текущая таблица
        self.current_table = "employees"

    def edit_record(self):
        """Редактировать выбранную запись"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите запись для редактирования")
            return

        item = self.tree.item(selection[0])
        values = item['values']
        record_id = values[0]

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Редактировать запись в {self.current_table}")

        # Адаптивный размер
        dialog_width = min(500, self.root.winfo_width() - 100)
        dialog_height = min(600, self.root.winfo_height() - 100)
        dialog.geometry(f"{dialog_width}x{dialog_height}")

        # Центрируем
        dialog.transient(self.root)
        dialog.grab_set()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog_height) // 2
        dialog.geometry(f"+{x}+{y}")

        if self.current_table == "employees":
            self.edit_employee_dialog(dialog, record_id, values)
        elif self.current_table == "clients":
            self.edit_client_dialog(dialog, record_id, values)
        elif self.current_table == "properties":
            self.edit_property_dialog(dialog, record_id, values)
        elif self.current_table == "deals":
            self.edit_deal_dialog(dialog, record_id, values)
        elif self.current_table == "viewings":
            self.edit_viewing_dialog(dialog, record_id, values)
        elif self.current_table == "services":
            self.edit_service_dialog(dialog, record_id, values)
        else:
            messagebox.showinfo("Информация", "Редактирование недоступно для текущей таблицы")
            dialog.destroy()

    def edit_employee_dialog(self, dialog, employee_id, values):
        """Редактирование сотрудника"""
        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Редактирование сотрудника",
                  font=('Arial', self.font_size, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Поля формы
        ttk.Label(main_frame, text="Имя:*", foreground='red').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        first_name_var = tk.StringVar(value=values[1])
        first_name_entry = ttk.Entry(main_frame, width=30, textvariable=first_name_var)
        first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Фамилия:*", foreground='red').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        last_name_var = tk.StringVar(value=values[2])
        last_name_entry = ttk.Entry(main_frame, width=30, textvariable=last_name_var)
        last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Телефон:*", foreground='red').grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        phone_var = tk.StringVar(value=values[3])
        phone_entry = ttk.Entry(main_frame, width=30, textvariable=phone_var)
        phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Email:*", foreground='red').grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        email_var = tk.StringVar(value=values[4])
        email_entry = ttk.Entry(main_frame, width=30, textvariable=email_var)
        email_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Дата найма:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        hire_date_var = tk.StringVar(value=values[5])
        hire_date_entry = ttk.Entry(main_frame, width=30, textvariable=hire_date_var)
        hire_date_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Комиссия (%):*", foreground='red').grid(row=6, column=0, padx=5, pady=5,
                                                                            sticky=tk.W)
        commission_var = tk.StringVar(value=values[6])
        commission_entry = ttk.Entry(main_frame, width=30, textvariable=commission_var)
        commission_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        # Активен (преобразуем "Да"/"Нет" в True/False)
        is_active = values[7] == "Да" if isinstance(values[7], str) else bool(values[7])
        active_var = tk.BooleanVar(value=is_active)
        ttk.Checkbutton(main_frame, text="Активен", variable=active_var).grid(
            row=7, column=1, padx=5, pady=5, sticky=tk.W
        )

        def save():
            """Сохранение изменений"""
            # Проверка обязательных полей
            if not all([first_name_var.get().strip(), last_name_var.get().strip(),
                        phone_var.get().strip(), email_var.get().strip(), commission_var.get().strip()]):
                messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                return

            try:
                data = (
                    first_name_var.get().strip(),
                    last_name_var.get().strip(),
                    phone_var.get().strip(),
                    email_var.get().strip(),
                    hire_date_var.get().strip(),
                    float(commission_var.get().strip()),
                    active_var.get(),
                    employee_id
                )

                query = """
                UPDATE employees 
                SET first_name = %s,
                    last_name = %s,
                    phone = %s,
                    email = %s,
                    hire_date = %s,
                    commission_rate = %s,
                    is_active = %s
                WHERE id = %s
                """

                result = self.execute_query(query, data)
                if result is not None:
                    self.refresh_data()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Данные сотрудника обновлены")
                else:
                    messagebox.showerror("Ошибка", "Не удалось обновить данные")

            except ValueError:
                messagebox.showerror("Ошибка", "Комиссия должна быть числом")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении:\n{str(e)}")

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=10)

        first_name_entry.focus_set()

        def edit_client_dialog(self, dialog, client_id, values):
            """Редактирование клиента"""
            main_frame = ttk.Frame(dialog, padding=15)
            main_frame.pack(fill=tk.BOTH, expand=True)

            ttk.Label(main_frame, text="Редактирование клиента",
                      font=('Arial', self.font_size, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))

            # Поля формы
            ttk.Label(main_frame, text="Имя:*", foreground='red').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
            first_name_var = tk.StringVar(value=values[1])
            first_name_entry = ttk.Entry(main_frame, width=30, textvariable=first_name_var)
            first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

            ttk.Label(main_frame, text="Фамилия:*", foreground='red').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
            last_name_var = tk.StringVar(value=values[2])
            last_name_entry = ttk.Entry(main_frame, width=30, textvariable=last_name_var)
            last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

            ttk.Label(main_frame, text="Телефон:*", foreground='red').grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
            phone_var = tk.StringVar(value=values[3])
            phone_entry = ttk.Entry(main_frame, width=30, textvariable=phone_var)
            phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

            ttk.Label(main_frame, text="Email:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
            email_var = tk.StringVar(value=values[4] if values[4] else "")
            email_entry = ttk.Entry(main_frame, width=30, textvariable=email_var)
            email_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

            ttk.Label(main_frame, text="Тип клиента:*", foreground='red').grid(row=5, column=0, padx=5, pady=5,
                                                                               sticky=tk.W)
            client_type_var = tk.StringVar(value=values[5])
            client_type_combo = ttk.Combobox(main_frame, textvariable=client_type_var,
                                             values=["buyer", "seller", "both"], state="readonly")
            client_type_combo.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

            ttk.Label(main_frame, text="Дата регистрации:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
            reg_date_var = tk.StringVar(value=values[6])
            reg_date_entry = ttk.Entry(main_frame, width=30, textvariable=reg_date_var)
            reg_date_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

            def save():
                """Сохранение изменений"""
                if not all([first_name_var.get().strip(), last_name_var.get().strip(), phone_var.get().strip()]):
                    messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                    return

                # Проверка email
                email = email_var.get().strip()
                if email and '@' not in email:
                    if not messagebox.askyesno("Предупреждение",
                                               "Email может быть некорректным. Продолжить сохранение?"):
                        return

                data = (
                    first_name_var.get().strip(),
                    last_name_var.get().strip(),
                    phone_var.get().strip(),
                    email if email else None,
                    client_type_var.get(),
                    reg_date_var.get().strip(),
                    client_id
                )

                query = """
                UPDATE clients 
                SET first_name = %s,
                    last_name = %s,
                    phone = %s,
                    email = %s,
                    client_type = %s,
                    registration_date = %s
                WHERE id = %s
                """

                result = self.execute_query(query, data)
                if result is not None:
                    self.refresh_data()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Данные клиента обновлены")
                else:
                    messagebox.showerror("Ошибка", "Не удалось обновить данные")

            # Кнопки
            button_frame = ttk.Frame(main_frame)
            button_frame.grid(row=7, column=0, columnspan=2, pady=20)

            ttk.Button(button_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=10)
            ttk.Button(button_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=10)

            first_name_entry.focus_set()

            def edit_property_dialog(self, dialog, property_id, values):
                """Редактирование объекта недвижимости"""
                # Получаем списки для выпадающих списков
                clients = self.execute_query("SELECT id, first_name || ' ' || last_name FROM clients", fetch=True)
                employees = self.execute_query(
                    "SELECT id, first_name || ' ' || last_name FROM employees WHERE is_active = true", fetch=True)

                main_frame = ttk.Frame(dialog, padding=15)
                main_frame.pack(fill=tk.BOTH, expand=True)

                ttk.Label(main_frame, text="Редактирование объекта",
                          font=('Arial', self.font_size, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))

                # Преобразуем цену обратно из форматированной строки
                price_str = values[6]
                if isinstance(price_str, str) and "руб." in price_str:
                    try:
                        price_value = float(price_str.replace("руб.", "").replace(",", "").strip())
                    except:
                        price_value = 0.0
                else:
                    price_value = float(price_str) if price_str else 0.0

                # Поля формы
                ttk.Label(main_frame, text="Адрес:*", foreground='red').grid(row=1, column=0, padx=5, pady=5,
                                                                             sticky=tk.W)
                address_var = tk.StringVar(value=values[1])
                address_entry = ttk.Entry(main_frame, width=30, textvariable=address_var)
                address_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

                ttk.Label(main_frame, text="Город:*", foreground='red').grid(row=2, column=0, padx=5, pady=5,
                                                                             sticky=tk.W)
                city_var = tk.StringVar(value=values[2])
                city_entry = ttk.Entry(main_frame, width=30, textvariable=city_var)
                city_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

                ttk.Label(main_frame, text="Тип:*", foreground='red').grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
                type_var = tk.StringVar(value=values[3])
                type_combo = ttk.Combobox(main_frame, textvariable=type_var,
                                          values=["apartment", "house", "commercial", "land"], state="readonly")
                type_combo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

                ttk.Label(main_frame, text="Комнат:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
                rooms_var = tk.StringVar(value=str(values[4]) if values[4] else "")
                rooms_entry = ttk.Entry(main_frame, width=30, textvariable=rooms_var)
                rooms_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

                ttk.Label(main_frame, text="Площадь (м²):*", foreground='red').grid(row=5, column=0, padx=5, pady=5,
                                                                                    sticky=tk.W)
                area_var = tk.StringVar(value=str(values[5]))
                area_entry = ttk.Entry(main_frame, width=30, textvariable=area_var)
                area_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

                ttk.Label(main_frame, text="Цена:*", foreground='red').grid(row=6, column=0, padx=5, pady=5,
                                                                            sticky=tk.W)
                price_var = tk.StringVar(value=str(price_value))
                price_entry = ttk.Entry(main_frame, width=30, textvariable=price_var)
                price_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

                ttk.Label(main_frame, text="Статус:*", foreground='red').grid(row=7, column=0, padx=5, pady=5,
                                                                              sticky=tk.W)
                status_var = tk.StringVar(value=values[7])
                status_combo = ttk.Combobox(main_frame, textvariable=status_var,
                                            values=["active", "sold", "rented", "archived"], state="readonly")
                status_combo.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

                # Получаем текущих владельца и агента
                current_owner_id = self.execute_query(
                    "SELECT owner_id FROM properties WHERE id = %s",
                    (property_id,), fetch=True
                )
                current_agent_id = self.execute_query(
                    "SELECT agent_id FROM properties WHERE id = %s",
                    (property_id,), fetch=True
                )

                ttk.Label(main_frame, text="Владелец:").grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
                owner_var = tk.StringVar()
                owner_combo = ttk.Combobox(main_frame, textvariable=owner_var, state="readonly", width=27)
                owner_values = []
                if clients:
                    for c_id, c_name in clients:
                        owner_values.append(f"{c_id} - {c_name}")
                        if current_owner_id and c_id == current_owner_id[0][0]:
                            owner_var.set(f"{c_id} - {c_name}")
                owner_combo['values'] = owner_values
                owner_combo.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)

                ttk.Label(main_frame, text="Агент:").grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
                agent_var = tk.StringVar()
                agent_combo = ttk.Combobox(main_frame, textvariable=agent_var, state="readonly", width=27)
                agent_values = []
                if employees:
                    for e_id, e_name in employees:
                        agent_values.append(f"{e_id} - {e_name}")
                        if current_agent_id and e_id == current_agent_id[0][0]:
                            agent_var.set(f"{e_id} - {e_name}")
                agent_combo['values'] = agent_values
                agent_combo.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)

                def save():
                    """Сохранение изменений"""
                    if not all([address_var.get().strip(), city_var.get().strip(),
                                area_var.get().strip(), price_var.get().strip()]):
                        messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                        return

                    try:
                        # Преобразуем данные
                        rooms = int(rooms_var.get()) if rooms_var.get().strip() else None
                        area = float(area_var.get())
                        price = float(price_var.get())

                        owner = owner_var.get()
                        agent = agent_var.get()
                        owner_id = int(owner.split(" - ")[0]) if owner else None
                        agent_id = int(agent.split(" - ")[0]) if agent else None

                        data = (
                            address_var.get().strip(),
                            city_var.get().strip(),
                            type_var.get(),
                            rooms,
                            area,
                            price,
                            status_var.get(),
                            owner_id,
                            agent_id,
                            property_id
                        )

                        query = """
                        UPDATE properties 
                        SET address = %s,
                            city = %s,
                            property_type = %s,
                            rooms = %s,
                            total_area = %s,
                            price = %s,
                            status = %s,
                            owner_id = %s,
                            agent_id = %s
                        WHERE id = %s
                        """

                        result = self.execute_query(query, data)
                        if result is not None:
                            self.refresh_data()
                            dialog.destroy()
                            messagebox.showinfo("Успех", "Данные объекта обновлены")
                        else:
                            messagebox.showerror("Ошибка", "Не удалось обновить данные")

                    except ValueError as e:
                        messagebox.showerror("Ошибка", "Проверьте правильность числовых значений")
                    except Exception as e:
                        messagebox.showerror("Ошибка", f"Ошибка при обновлении:\n{str(e)}")

                # Кнопки
                button_frame = ttk.Frame(main_frame)
                button_frame.grid(row=10, column=0, columnspan=2, pady=20)

                ttk.Button(button_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=10)
                ttk.Button(button_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=10)

                address_entry.focus_set()

                def edit_deal_dialog(self, dialog, deal_id, values):
                    """Редактирование сделки"""
                    # Получаем данные для выпадающих списков
                    properties = self.execute_query("SELECT id, address FROM properties", fetch=True)
                    clients = self.execute_query("SELECT id, first_name || ' ' || last_name FROM clients", fetch=True)
                    employees = self.execute_query(
                        "SELECT id, first_name || ' ' || last_name FROM employees WHERE is_active = true", fetch=True)

                    # Получаем полные данные сделки из БД
                    deal_data = self.execute_query(
                        """SELECT property_id, buyer_id, seller_id, agent_id, deal_date, 
                                  deal_price, commission_amount, deal_type 
                           FROM deals WHERE id = %s""",
                        (deal_id,), fetch=True
                    )

                    if not deal_data:
                        messagebox.showerror("Ошибка", "Сделка не найдена")
                        dialog.destroy()
                        return

                    deal = deal_data[0]

                    main_frame = ttk.Frame(dialog, padding=15)
                    main_frame.pack(fill=tk.BOTH, expand=True)

                    ttk.Label(main_frame, text="Редактирование сделки",
                              font=('Arial', self.font_size, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))

                    # Вспомогательная функция для поиска значения в списке
                    def find_in_list(items, target_id):
                        for item_id, item_name in items:
                            if item_id == target_id:
                                return f"{item_id} - {item_name}"
                        return ""

                    # Поля формы
                    ttk.Label(main_frame, text="Объект:*", foreground='red').grid(row=1, column=0, padx=5, pady=5,
                                                                                  sticky=tk.W)
                    property_var = tk.StringVar(value=find_in_list(properties, deal[0]))
                    property_combo = ttk.Combobox(main_frame, textvariable=property_var, state="readonly", width=30)
                    if properties:
                        property_combo["values"] = [f"{p[0]} - {p[1]}" for p in properties]
                    property_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

                    ttk.Label(main_frame, text="Покупатель:*", foreground='red').grid(row=2, column=0, padx=5, pady=5,
                                                                                      sticky=tk.W)
                    buyer_var = tk.StringVar(value=find_in_list(clients, deal[1]))
                    buyer_combo = ttk.Combobox(main_frame, textvariable=buyer_var, state="readonly", width=30)
                    if clients:
                        buyer_combo["values"] = [f"{c[0]} - {c[1]}" for c in clients]
                    buyer_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

                    ttk.Label(main_frame, text="Продавец:*", foreground='red').grid(row=3, column=0, padx=5, pady=5,
                                                                                    sticky=tk.W)
                    seller_var = tk.StringVar(value=find_in_list(clients, deal[2]))
                    seller_combo = ttk.Combobox(main_frame, textvariable=seller_var, state="readonly", width=30)
                    if clients:
                        seller_combo["values"] = [f"{c[0]} - {c[1]}" for c in clients]
                    seller_combo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

                    ttk.Label(main_frame, text="Агент:*", foreground='red').grid(row=4, column=0, padx=5, pady=5,
                                                                                 sticky=tk.W)
                    agent_var = tk.StringVar(value=find_in_list(employees, deal[3]))
                    agent_combo = ttk.Combobox(main_frame, textvariable=agent_var, state="readonly", width=30)
                    if employees:
                        agent_combo["values"] = [f"{e[0]} - {e[1]}" for e in employees]
                    agent_combo.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

                    ttk.Label(main_frame, text="Дата сделки:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
                    date_var = tk.StringVar(value=str(deal[4]))
                    date_entry = ttk.Entry(main_frame, width=30, textvariable=date_var)
                    date_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

                    ttk.Label(main_frame, text="Цена сделки:*", foreground='red').grid(row=6, column=0, padx=5, pady=5,
                                                                                       sticky=tk.W)
                    price_var = tk.StringVar(value=str(deal[5]))
                    price_entry = ttk.Entry(main_frame, width=30, textvariable=price_var)
                    price_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

                    ttk.Label(main_frame, text="Комиссия:*", foreground='red').grid(row=7, column=0, padx=5, pady=5,
                                                                                    sticky=tk.W)
                    commission_var = tk.StringVar(value=str(deal[6]))
                    commission_entry = ttk.Entry(main_frame, width=30, textvariable=commission_var)
                    commission_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

                    ttk.Label(main_frame, text="Тип сделки:*", foreground='red').grid(row=8, column=0, padx=5, pady=5,
                                                                                      sticky=tk.W)
                    deal_type_var = tk.StringVar(value=deal[7])
                    deal_type_combo = ttk.Combobox(main_frame, textvariable=deal_type_var,
                                                   values=["sale", "rent"], state="readonly")
                    deal_type_combo.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)

                    def save():
                        """Сохранение изменений"""
                        if not all([property_var.get(), buyer_var.get(), seller_var.get(),
                                    agent_var.get(), price_var.get().strip(), commission_var.get().strip()]):
                            messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                            return

                        try:
                            # Преобразуем данные
                            property_id = int(property_var.get().split(" - ")[0])
                            buyer_id = int(buyer_var.get().split(" - ")[0])
                            seller_id = int(seller_var.get().split(" - ")[0])
                            agent_id = int(agent_var.get().split(" - ")[0])
                            price = float(price_var.get())
                            commission = float(commission_var.get())

                            data = (
                                property_id,
                                buyer_id,
                                seller_id,
                                agent_id,
                                date_var.get().strip(),
                                price,
                                commission,
                                deal_type_var.get(),
                                deal_id
                            )

                            query = """
                            UPDATE deals 
                            SET property_id = %s,
                                buyer_id = %s,
                                seller_id = %s,
                                agent_id = %s,
                                deal_date = %s,
                                deal_price = %s,
                                commission_amount = %s,
                                deal_type = %s
                            WHERE id = %s
                            """

                            result = self.execute_query(query, data)
                            if result is not None:
                                self.refresh_data()
                                dialog.destroy()
                                messagebox.showinfo("Успех", "Данные сделки обновлены")
                            else:
                                messagebox.showerror("Ошибка", "Не удалось обновить данные")

                        except ValueError as e:
                            messagebox.showerror("Ошибка", "Проверьте правильность числовых значений")
                        except Exception as e:
                            messagebox.showerror("Ошибка", f"Ошибка при обновлении:\n{str(e)}")

                    # Кнопки
                    button_frame = ttk.Frame(main_frame)
                    button_frame.grid(row=9, column=0, columnspan=2, pady=20)

                    ttk.Button(button_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=10)
                    ttk.Button(button_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT,
                                                                                                   padx=10)

                    property_combo.focus_set()

    def edit_viewing_dialog(self, dialog, viewing_id, values):
        """Редактирование просмотра"""
        # Получаем полные данные из БД
        viewing_data = self.execute_query(
            """SELECT property_id, client_id, agent_id, viewing_date, 
                      status, client_feedback 
               FROM viewings WHERE id = %s""",
            (viewing_id,), fetch=True
        )

        if not viewing_data:
            messagebox.showerror("Ошибка", "Просмотр не найден")
            dialog.destroy()
            return

        viewing = viewing_data[0]

        # Получаем списки для выпадающих списков
        properties = self.execute_query("SELECT id, address FROM properties", fetch=True)
        clients = self.execute_query("SELECT id, first_name || ' ' || last_name FROM clients", fetch=True)
        employees = self.execute_query(
            "SELECT id, first_name || ' ' || last_name FROM employees WHERE is_active = true", fetch=True)

        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Редактирование просмотра",
                  font=('Arial', self.font_size, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        def find_in_list(items, target_id):
            for item_id, item_name in items:
                if item_id == target_id:
                    return f"{item_id} - {item_name}"
            return ""

        # Поля формы
        ttk.Label(main_frame, text="Объект:*", foreground='red').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        property_var = tk.StringVar(value=find_in_list(properties, viewing[0]))
        property_combo = ttk.Combobox(main_frame, textvariable=property_var, state="readonly", width=30)
        if properties:
            property_combo["values"] = [f"{p[0]} - {p[1]}" for p in properties]
        property_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Клиент:*", foreground='red').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        client_var = tk.StringVar(value=find_in_list(clients, viewing[1]))
        client_combo = ttk.Combobox(main_frame, textvariable=client_var, state="readonly", width=30)
        if clients:
            client_combo["values"] = [f"{c[0]} - {c[1]}" for c in clients]
        client_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Агент:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        agent_var = tk.StringVar(value=find_in_list(employees, viewing[2]) if viewing[2] else "")
        agent_combo = ttk.Combobox(main_frame, textvariable=agent_var, state="readonly", width=30)
        if employees:
            agent_combo["values"] = [f"{e[0]} - {e[1]}" for e in employees]
        agent_combo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        # Парсим дату и время
        viewing_datetime = viewing[3]
        if isinstance(viewing_datetime, str):
            try:
                dt = datetime.strptime(viewing_datetime, "%Y-%m-%d %H:%M:%S")
                date_str = dt.strftime("%Y-%m-%d")
                time_str = dt.strftime("%H:%M")
            except:
                date_str = ""
                time_str = ""
        else:
            date_str = viewing_datetime.strftime("%Y-%m-%d")
            time_str = viewing_datetime.strftime("%H:%M")

        ttk.Label(main_frame, text="Дата:*", foreground='red').grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        date_var = tk.StringVar(value=date_str)
        date_entry = ttk.Entry(main_frame, width=30, textvariable=date_var)
        date_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Время:*", foreground='red').grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        time_var = tk.StringVar(value=time_str)
        time_entry = ttk.Entry(main_frame, width=30, textvariable=time_var)
        time_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Статус:*", foreground='red').grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        status_var = tk.StringVar(value=viewing[4])
        status_combo = ttk.Combobox(main_frame, textvariable=status_var,
                                    values=["scheduled", "completed", "cancelled"], state="readonly")
        status_combo.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Отзыв клиента:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        feedback_text = tk.Text(main_frame, height=4, width=30)
        feedback_text.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        feedback_text.insert("1.0", viewing[5] if viewing[5] else "")

        def save():
            """Сохранение изменений"""
            if not all([property_var.get(), client_var.get(),
                        date_var.get().strip(), time_var.get().strip()]):
                messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                return

            # Проверка даты и времени
            try:
                datetime_str = f"{date_var.get().strip()} {time_var.get().strip()}"
                viewing_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

                # Проверка на прошедшее время (если статус не "completed")
                if status_var.get() != "completed":
                    current_datetime = datetime.now()
                    if viewing_datetime < current_datetime:
                        messagebox.showerror("Ошибка", "Нельзя выбрать прошедшее время для будущих просмотров")
                        return
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты или времени")
                return

            try:
                property_id = int(property_var.get().split(" - ")[0])
                client_id = int(client_var.get().split(" - ")[0])
                agent_id = int(agent_var.get().split(" - ")[0]) if agent_var.get() else None

                data = (
                    property_id,
                    client_id,
                    agent_id,
                    datetime_str,
                    status_var.get(),
                    feedback_text.get("1.0", "end-1c").strip(),
                    viewing_id
                )

                query = """
                UPDATE viewings 
                SET property_id = %s,
                    client_id = %s,
                    agent_id = %s,
                    viewing_date = %s,
                    status = %s,
                    client_feedback = %s
                WHERE id = %s
                """

                result = self.execute_query(query, data)
                if result is not None:
                    self.refresh_data()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Данные просмотра обновлены")
                else:
                    messagebox.showerror("Ошибка", "Не удалось обновить данные")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении:\n{str(e)}")

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=10)

        property_combo.focus_set()

    def edit_service_dialog(self, dialog, service_id, values):
        """Редактирование услуги"""
        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Редактирование услуги",
                  font=('Arial', self.font_size, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Преобразуем цену из строки
        price_str = values[3]
        if isinstance(price_str, str) and "руб." in price_str:
            try:
                price_value = float(price_str.replace("руб.", "").replace(",", "").strip())
            except:
                price_value = 0.0
        else:
            price_value = float(price_str) if price_str else 0.0

        # Поля формы
        ttk.Label(main_frame, text="Название услуги:*", foreground='red').grid(row=1, column=0, padx=5, pady=5,
                                                                               sticky=tk.W)
        name_var = tk.StringVar(value=values[1])
        name_entry = ttk.Entry(main_frame, width=30, textvariable=name_var)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Описание:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        desc_var = tk.StringVar(value=values[2])
        desc_entry = ttk.Entry(main_frame, width=30, textvariable=desc_var)
        desc_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Цена:*", foreground='red').grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        price_var = tk.StringVar(value=str(price_value))
        price_entry = ttk.Entry(main_frame, width=30, textvariable=price_var)
        price_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Срок (дней):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        duration_var = tk.StringVar(value=str(values[4]) if values[4] != "-" else "")
        duration_entry = ttk.Entry(main_frame, width=30, textvariable=duration_var)
        duration_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        def save():
            """Сохранение изменений"""
            if not name_var.get().strip():
                messagebox.showerror("Ошибка", "Введите название услуги")
                return

            try:
                # Преобразуем данные
                price = float(price_var.get()) if price_var.get().strip() else None
                duration = int(duration_var.get()) if duration_var.get().strip() else None

                data = (
                    name_var.get().strip(),
                    desc_var.get().strip(),
                    price,
                    duration,
                    service_id
                )

                query = """
                UPDATE services 
                SET service_name = %s,
                    description = %s,
                    standard_price = %s,
                    duration_days = %s
                WHERE id = %s
                """

                result = self.execute_query(query, data)
                if result is not None:
                    self.refresh_data()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Данные услуги обновлены")
                else:
                    messagebox.showerror("Ошибка", "Не удалось обновить данные")

            except ValueError:
                messagebox.showerror("Ошибка", "Цена и срок должны быть числами")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении:\n{str(e)}")

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=10)

        name_entry.focus_set()


    def create_treeview(self):
        """Создать Treeview с адаптивными колонками"""
        # Создаем Treeview и Scrollbar
        self.tree = ttk.Treeview(self.tree_frame, show='headings')

        # Вертикальная прокрутка
        v_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        # Горизонтальная прокрутка
        h_scrollbar = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky=tk.EW)
        self.tree.configure(xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=tk.NSEW)

        # Настраиваем адаптивность Treeview
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)

    def adjust_treeview_columns(self):
        """Настроить ширину колонок Treeview в зависимости от размера окна"""
        if not hasattr(self, 'tree') or not self.tree['columns']:
            return

        window_width = self.root.winfo_width()
        num_columns = len(self.tree['columns'])

        # Рассчитываем базовую ширину колонки
        if window_width >= 1400:
            base_width = 150
        elif window_width >= 1000:
            base_width = 120
        elif window_width >= 800:
            base_width = 100
        else:
            base_width = 80

        # Устанавливаем ширину для каждой колонки
        for col in self.tree['columns']:
            self.tree.column(col, width=base_width, minwidth=base_width // 2)

    def show_employees(self):
        """Показать таблицу сотрудников"""
        self.current_table = "employees"

        # Удаляем фрейм с отчетами, если он существует
        if hasattr(self, 'report_frame'):
            self.report_frame.destroy()
            delattr(self, 'report_frame')

        # Показываем Treeview
        self.tree_frame.grid()

        self.tree["columns"] = ("ID", "Имя", "Фамилия", "Телефон", "Email", "Дата найма", "Комиссия %", "Активен")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Очищаем старые данные
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Настраиваем ширину колонок
        self.adjust_treeview_columns()

        # Загружаем данные
        self.load_employees()
        self.status_var.set("Таблица: Сотрудники")
        self.update_record_count()

    def load_employees(self):
        """Загрузить данные сотрудников"""
        query = """
        SELECT id, first_name, last_name, phone, email, hire_date, 
               commission_rate, is_active 
        FROM employees 
        ORDER BY id
        """

        rows = self.execute_query(query, fetch=True)
        if rows:
            for row in rows:
                # Форматируем булево значение
                formatted_row = list(row)
                formatted_row[-1] = "Да" if row[-1] else "Нет"
                self.tree.insert("", tk.END, values=formatted_row)

        self.update_record_count()

    def show_clients(self):
        """Показать таблицу клиентов"""
        self.current_table = "clients"

        # Удаляем фрейм с отчетами, если он существует
        if hasattr(self, 'report_frame'):
            self.report_frame.destroy()
            delattr(self, 'report_frame')

        # Показываем Treeview
        self.tree_frame.grid()

        self.tree["columns"] = ("ID", "Имя", "Фамилия", "Телефон", "Email", "Тип", "Дата регистрации")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.adjust_treeview_columns()

        query = """
           SELECT id, first_name, last_name, phone, email, client_type, registration_date
           FROM clients 
           ORDER BY id
           """

        rows = self.execute_query(query, fetch=True)
        if rows:
            for row in rows:
                self.tree.insert("", tk.END, values=row)

        self.status_var.set("Таблица: Клиенты")
        self.update_record_count()

    def show_properties(self):
        """Показать таблицу объектов"""
        self.current_table = "properties"

        # Удаляем фрейм с отчетами, если он существует
        if hasattr(self, 'report_frame'):
            self.report_frame.destroy()
            delattr(self, 'report_frame')

        # Показываем Treeview
        self.tree_frame.grid()

        self.tree["columns"] = ("ID", "Адрес", "Город", "Тип", "Комнат", "Площадь", "Цена", "Статус")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.adjust_treeview_columns()

        query = """
           SELECT id, address, city, property_type, rooms, total_area, price, status
           FROM properties 
           ORDER BY id
           """

        rows = self.execute_query(query, fetch=True)
        if rows:
            for row in rows:
                formatted_row = list(row)
                # Форматируем цену
                formatted_row[6] = f"{row[6]:,.2f} руб."
                self.tree.insert("", tk.END, values=formatted_row)

        self.status_var.set("Таблица: Объекты недвижимости")
        self.update_record_count()

    def show_deals(self):
        """Показать таблицу сделок"""
        self.current_table = "deals"

        # Удаляем фрейм с отчетами, если он существует
        if hasattr(self, 'report_frame'):
            self.report_frame.destroy()
            delattr(self, 'report_frame')

        # Показываем Treeview
        self.tree_frame.grid()

        self.tree["columns"] = ("ID", "Объект", "Покупатель", "Агент", "Дата", "Цена", "Комиссия", "Тип")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.adjust_treeview_columns()

        query = """
           SELECT d.id, p.address, 
                  buyer.first_name || ' ' || buyer.last_name as buyer_name,
                  e.first_name || ' ' || e.last_name as agent_name,
                  d.deal_date, d.deal_price, d.commission_amount, d.deal_type
           FROM deals d
           JOIN properties p ON d.property_id = p.id
           JOIN clients buyer ON d.buyer_id = buyer.id
           JOIN employees e ON d.agent_id = e.id
           ORDER BY d.deal_date DESC
           """

        rows = self.execute_query(query, fetch=True)
        if rows:
            for row in rows:
                formatted_row = list(row)
                formatted_row[5] = f"{row[5]:,.2f} руб."
                formatted_row[6] = f"{row[6]:,.2f} руб."
                self.tree.insert("", tk.END, values=formatted_row)

        self.status_var.set("Таблица: Сделки")
        self.update_record_count()

    def show_viewings(self):
        """Показать таблицу просмотров"""
        self.current_table = "viewings"

        # Удаляем фрейм с отчетами, если он существует
        if hasattr(self, 'report_frame'):
            self.report_frame.destroy()
            delattr(self, 'report_frame')

        # Показываем Treeview
        self.tree_frame.grid()

        self.tree["columns"] = ("ID", "Объект", "Клиент", "Дата", "Статус", "Отзыв")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.adjust_treeview_columns()

        query = """
           SELECT v.id, p.address, 
                  c.first_name || ' ' || c.last_name as client_name,
                  v.viewing_date, v.status, 
                  COALESCE(LEFT(v.client_feedback, 30) || '...', 'Нет отзыва')
           FROM viewings v
           JOIN properties p ON v.property_id = p.id
           JOIN clients c ON v.client_id = c.id
           ORDER BY v.viewing_date DESC
           """

        rows = self.execute_query(query, fetch=True)
        if rows:
            for row in rows:
                self.tree.insert("", tk.END, values=row)

        self.status_var.set("Таблица: Просмотры объектов")
        self.update_record_count()

    def show_services(self):
        """Показать таблицу услуг"""
        self.current_table = "services"

        # Удаляем фрейм с отчетами, если он существует
        if hasattr(self, 'report_frame'):
            self.report_frame.destroy()
            delattr(self, 'report_frame')

        # Показываем Treeview
        self.tree_frame.grid()

        self.tree["columns"] = ("ID", "Название", "Описание", "Цена", "Срок")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.adjust_treeview_columns()

        query = """
           SELECT id, service_name, 
                  COALESCE(LEFT(description, 50) || '...', 'Нет описания'), 
                  standard_price, duration_days
           FROM services 
           ORDER BY id
           """

        rows = self.execute_query(query, fetch=True)
        if rows:
            for row in rows:
                formatted_row = list(row)
                formatted_row[3] = f"{row[3]:,.2f} руб." if row[3] else "-"
                self.tree.insert("", tk.END, values=formatted_row)

        self.status_var.set("Таблица: Услуги")
        self.update_record_count()

    def show_reports(self):
        """Показать отчеты"""
        self.current_table = "reports"

        # Очищаем tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Скрываем Treeview
        self.tree_frame.grid_remove()

        # Создаем текстовый виджет для отчетов
        if hasattr(self, 'report_text'):
            self.report_text.destroy()

        self.report_frame = ttk.Frame(self.data_container)
        self.report_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.report_frame.columnconfigure(0, weight=1)
        self.report_frame.rowconfigure(0, weight=1)

        self.report_text = tk.Text(
            self.report_frame,
            wrap=tk.WORD,
            font=('Courier', self.font_size - 1)
        )
        self.report_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.report_text, command=self.report_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.report_text.configure(yscrollcommand=scrollbar.set)

        # Генерируем отчеты
        reports = self.generate_reports()
        self.report_text.insert(tk.END, reports)
        self.report_text.config(state=tk.DISABLED)

        self.status_var.set("Отчеты")
        self.info_var.set("")

    def show_employees(self):
        """Показать таблицу сотрудников"""
        self.current_table = "employees"

        # Удаляем фрейм с отчетами, если он существует
        if hasattr(self, 'report_frame'):
            self.report_frame.destroy()
            delattr(self, 'report_frame')

        # Показываем Treeview
        self.tree_frame.grid()

        self.tree["columns"] = ("ID", "Имя", "Фамилия", "Телефон", "Email", "Дата найма", "Комиссия %", "Активен")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Очищаем старые данные
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Настраиваем ширину колонок
        self.adjust_treeview_columns()

        # Загружаем данные
        self.load_employees()
        self.status_var.set("Таблица: Сотрудники")
        self.update_record_count()

    def generate_reports(self):
        """Генерация отчетов"""
        reports = "=" * 60 + "\n"
        reports += "ОТЧЕТЫ РИЭЛТОРСКОГО АГЕНТСТВА\n"
        reports += "=" * 60 + "\n\n"

        # 1. Статистика по агентам
        query1 = """
        SELECT e.first_name || ' ' || e.last_name as agent,
               COUNT(d.id) as deals_count,
               COALESCE(SUM(d.commission_amount), 0) as total_commission
        FROM employees e
        LEFT JOIN deals d ON e.id = d.agent_id
        WHERE e.is_active = true
        GROUP BY e.id
        ORDER BY total_commission DESC
        """

        rows1 = self.execute_query(query1, fetch=True)
        if rows1:
            reports += "1. СТАТИСТИКА ПО АГЕНТАМ:\n"
            reports += "-" * 40 + "\n"
            for row in rows1:
                reports += f"Агент: {row[0]}\n"
                reports += f"  Сделок: {row[1]}\n"
                reports += f"  Комиссия: {row[2]:,.2f} руб.\n"
            reports += "\n"

        # 2. Статистика по объектам
        query2 = """
        SELECT property_type, 
               COUNT(*) as total,
               SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active,
               SUM(CASE WHEN status = 'sold' THEN 1 ELSE 0 END) as sold,
               AVG(price) as avg_price
        FROM properties
        GROUP BY property_type
        """

        rows2 = self.execute_query(query2, fetch=True)
        if rows2:
            reports += "2. СТАТИСТИКА ПО ОБЪЕКТАМ:\n"
            reports += "-" * 40 + "\n"
            for row in rows2:
                type_name = {'apartment': 'Квартиры', 'house': 'Дома',
                             'commercial': 'Коммерческие', 'land': 'Земля'}.get(row[0], row[0])
                reports += f"{type_name}:\n"
                reports += f"  Всего: {row[1]}, Активных: {row[2]}, Продано: {row[3]}\n"
                reports += f"  Средняя цена: {row[4]:,.2f} руб.\n"
            reports += "\n"

        # 3. Доходы от услуг
        query3 = """
        SELECT s.service_name,
               COUNT(sr.id) as requests_count,
               COALESCE(SUM(sr.actual_price), 0) as total_income
        FROM services s
        LEFT JOIN service_requests sr ON s.id = sr.service_id
        GROUP BY s.id, s.service_name
        """

        rows3 = self.execute_query(query3, fetch=True)
        if rows3:
            reports += "3. ДОХОДЫ ОТ УСЛУГ:\n"
            reports += "-" * 40 + "\n"
            for row in rows3:
                reports += f"{row[0]}:\n"
                reports += f"  Заявок: {row[1]}, Доход: {row[2]:,.2f} руб.\n"

        return reports

    def update_record_count(self):
        """Обновить количество записей в статусной строке"""
        count = len(self.tree.get_children())
        self.info_var.set(f"Записей: {count}")

    def add_record(self):
        """Добавить запись"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Добавить запись в {self.current_table}")

        # Адаптивный размер диалогового окна
        dialog_width = min(500, self.root.winfo_width() - 100)
        dialog_height = min(600, self.root.winfo_height() - 100)
        dialog.geometry(f"{dialog_width}x{dialog_height}")

        # Центрируем диалоговое окно
        dialog.transient(self.root)
        dialog.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() - dialog_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog_height) // 2
        dialog.geometry(f"+{x}+{y}")

        if self.current_table == "employees":
            self.add_employee_dialog(dialog)
        elif self.current_table == "clients":
            self.add_client_dialog(dialog)
        elif self.current_table == "properties":
            self.add_property_dialog(dialog)
        elif self.current_table == "deals":
            self.add_deal_dialog(dialog)
        elif self.current_table == "viewings":
            self.add_viewing_dialog(dialog)
        elif self.current_table == "services":
            self.add_service_dialog(dialog)
        else:
            messagebox.showinfo("Информация", "Выберите таблицу для добавления записи")
            dialog.destroy()

    def add_employee_dialog(self, dialog, entries=None):
        """Диалог добавления сотрудника - кнопка сохранить заблокирована пока не заполнены все поля"""
        dialog.title("Добавить сотрудника")

        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем переменные для каждого поля
        first_name_var = tk.StringVar()
        last_name_var = tk.StringVar()
        phone_var = tk.StringVar()
        email_var = tk.StringVar()
        commission_var = tk.StringVar(value="2.5")

        # Функция для проверки всех полей
        def check_all_fields():
            """Проверяет заполнение всех полей"""
            conditions = [
                bool(first_name_var.get().strip()),
                bool(last_name_var.get().strip()),
                bool(phone_var.get().strip()),
                bool(email_var.get().strip()),
                bool(commission_var.get().strip())
            ]
            return all(conditions)

        def update_save_button(*args):
            """Обновляет состояние кнопки Сохранить"""
            if check_all_fields():
                save_button.configure(state='normal')
                status_label.configure(text="✓ Можно сохранить", foreground='green')
            else:
                save_button.configure(state='disabled')
                status_label.configure(text="Заполните все поля", foreground='black')

        # Привязываем отслеживание изменений
        first_name_var.trace('w', update_save_button)
        last_name_var.trace('w', update_save_button)
        phone_var.trace('w', update_save_button)
        email_var.trace('w', update_save_button)
        commission_var.trace('w', update_save_button)

        # Поля формы
        ttk.Label(main_frame, text="Имя:*", foreground='black').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        first_name_entry = ttk.Entry(main_frame, width=30, textvariable=first_name_var)
        first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Фамилия:*", foreground='black').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        last_name_entry = ttk.Entry(main_frame, width=30, textvariable=last_name_var)
        last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Телефон:*", foreground='black').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        phone_entry = ttk.Entry(main_frame, width=30, textvariable=phone_var)
        phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Email:*", foreground='black').grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        email_entry = ttk.Entry(main_frame, width=30, textvariable=email_var)
        email_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Комиссия (%):*", foreground='black').grid(row=4, column=0, padx=5, pady=5,
                                                                            sticky=tk.W)
        commission_entry = ttk.Entry(main_frame, width=30, textvariable=commission_var)
        commission_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        # Checkbox для активности
        active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Активен", variable=active_var).grid(
            row=5, column=1, padx=5, pady=5, sticky=tk.W
        )

        # Статусная строка
        status_label = ttk.Label(main_frame, text="Заполните все поля", foreground='black')
        status_label.grid(row=6, column=0, columnspan=2, pady=(10, 5))

        # Функция сохранения с дополнительной проверкой
        def save():
            # Проверка email
            email = email_var.get().strip()
            if '@' not in email:
                messagebox.showerror("Ошибка", "Email должен содержать '@'")
                email_entry.focus_set()
                return

            # Проверка комиссии
            try:
                commission = float(commission_var.get().strip())
                if commission <= 0:
                    messagebox.showerror("Ошибка", "Комиссия должна быть больше 0")
                    commission_entry.focus_set()
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Комиссия должна быть числом")
                commission_entry.focus_set()
                return

            # Все проверки пройдены
            data = (
                first_name_var.get().strip(),
                last_name_var.get().strip(),
                phone_var.get().strip(),
                email,
                commission,
                active_var.get()
            )

            query = """
            INSERT INTO employees (first_name, last_name, phone, email, commission_rate, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            self.execute_query(query, data)
            self.refresh_data()
            dialog.destroy()
            messagebox.showinfo("Успех", "Сотрудник добавлен")

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        save_button = ttk.Button(button_frame, text="Сохранить", command=save, width=15, state='disabled')
        save_button.pack(side=tk.LEFT, padx=10)

        ttk.Button(button_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=10)

        # Фокус на первое поле
        first_name_entry.focus_set()

        # Функция проверки полей
        def check_fields():
            """Проверяет заполнение всех полей"""
            missing_fields = []

            for key, (label, widget) in fields.items():
                value = widget.get().strip()
                if not value:
                    missing_fields.append(label)
                    # Подсвечиваем поле с ошибкой
                    widget.configure(style='Error.TEntry')
                else:
                    widget.configure(style='TEntry')

                    # Дополнительная проверка для email
                    if key == "email" and '@' not in value:
                        messagebox.showerror("Ошибка", "Email должен содержать '@'")
                        widget.configure(style='Error.TEntry')
                        return False

                    # Дополнительная проверка для комиссии
                    if key == "commission":
                        try:
                            comm = float(value)
                            if comm <= 0:
                                messagebox.showerror("Ошибка", "Комиссия должна быть больше 0")
                                widget.configure(style='Error.TEntry')
                                return False
                        except ValueError:
                            messagebox.showerror("Ошибка", "Комиссия должна быть числом")
                            widget.configure(style='Error.TEntry')
                            return False

            if missing_fields:
                messagebox.showerror(
                    "Обязательные поля не заполнены",
                    f"Заполните следующие поля:\n\n• " + "\n• ".join(missing_fields)
                )
                return False

            return True

        def save(entries=None):
            """Сохраняет запись после проверки
            :param entries:
            """
            if not check_fields():
                return

            try:
                data = (
                    entries["first_name"].get().strip(),
                    entries["last_name"].get().strip(),
                    entries["phone"].get().strip(),
                    entries["email"].get().strip(),
                    float(entries["commission"].get().strip()),
                    active_var.get()
                )

                query = """
                INSERT INTO employees (first_name, last_name, phone, email, commission_rate, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
                """

                self.execute_query(query, data)
                self.refresh_data()
                dialog.destroy()
                messagebox.showinfo("Успех", "Сотрудник добавлен")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить сотрудника:\n{str(e)}")

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Сохранить", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        # Стиль для ошибок
        style = ttk.Style()
        style.configure('Error.TEntry', fieldbackground='#FFE6E6', foreground='black')

        # Фокус на первое поле
        entries["first_name"].focus_set()

    def add_client_dialog(self, dialog):
        """Диалог добавления клиента - универсальный с полной валидацией"""
        dialog.title("Добавить клиента")

        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем стиль для ошибок
        style = ttk.Style()
        style.configure('Error.TEntry', fieldbackground='#FFE6E6', foreground='black')
        style.configure('Error.TCombobox', fieldbackground='#FFE6E6', foreground='black')

        # Поля формы
        ttk.Label(main_frame, text="Имя:*", foreground='black').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        first_name_entry = ttk.Entry(main_frame, width=30)
        first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Фамилия:*", foreground='black').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        last_name_entry = ttk.Entry(main_frame, width=30)
        last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Телефон:*", foreground='black').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        phone_entry = ttk.Entry(main_frame, width=30)
        phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Email:*", foreground='black').grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        email_entry = ttk.Entry(main_frame, width=30)
        email_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        # Выбор типа клиента
        ttk.Label(main_frame, text="Тип клиента:*", foreground='black').grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        client_type_var = tk.StringVar(value="")
        client_type_combo = ttk.Combobox(main_frame, textvariable=client_type_var,
                                         values=["buyer", "seller", "both"], state="readonly")
        client_type_combo.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        # Информационное сообщение
        info_label = ttk.Label(main_frame, text="* - обязательные поля", foreground='black')
        info_label.grid(row=5, column=0, columnspan=2, pady=(10, 5))

        # Функция проверки всех полей
        def validate_all_fields():
            """Проверяет все поля и возвращает список ошибок"""
            errors = []

            # Сбрасываем стили
            first_name_entry.configure(style='TEntry')
            last_name_entry.configure(style='TEntry')
            phone_entry.configure(style='TEntry')
            email_entry.configure(style='TEntry')
            client_type_combo.configure(style='TCombobox')

            # Проверка имени
            first_name = first_name_entry.get().strip()
            if not first_name:
                errors.append("Имя не заполнено")
                first_name_entry.configure(style='Error.TEntry')
            elif len(first_name) < 2:
                errors.append("Имя должно содержать минимум 2 символа")
                first_name_entry.configure(style='Error.TEntry')

            # Проверка фамилии
            last_name = last_name_entry.get().strip()
            if not last_name:
                errors.append("Фамилия не заполнена")
                last_name_entry.configure(style='Error.TEntry')
            elif len(last_name) < 2:
                errors.append("Фамилия должна содержать минимум 2 символа")
                last_name_entry.configure(style='Error.TEntry')

            # Проверка телефона
            phone = phone_entry.get().strip()
            if not phone:
                errors.append("Телефон не заполнен")
                phone_entry.configure(style='Error.TEntry')
            else:
                # Считаем количество цифр
                digit_count = sum(c.isdigit() for c in phone)
                if digit_count < 5:
                    errors.append("Телефон должен содержать минимум 5 цифр")
                    phone_entry.configure(style='Error.TEntry')

            # Проверка email
            email = email_entry.get().strip()
            if not email:
                errors.append("Email не заполнен")
                email_entry.configure(style='Error.TEntry')
            else:
                # Базовая проверка email
                if '@' not in email:
                    errors.append("Email должен содержать символ '@'")
                    email_entry.configure(style='Error.TEntry')
                elif '.' not in email.split('@')[-1]:
                    errors.append("Email должен содержать домен (например: .com, .ru)")
                    email_entry.configure(style='Error.TEntry')

            # Проверка типа клиента
            client_type = client_type_var.get()
            if not client_type:
                errors.append("Выберите тип клиента")
                client_type_combo.configure(style='Error.TCombobox')

            return errors

        # Функция сохранения
        def save():
            errors = validate_all_fields()

            if errors:
                # Показываем все ошибки
                error_text = "Исправьте следующие ошибки:\n\n" + "\n".join(f"• {error}" for error in errors)
                messagebox.showerror("Ошибки заполнения", error_text)
                return

            # Все проверки пройдены
            try:
                data = (
                    first_name_entry.get().strip(),
                    last_name_entry.get().strip(),
                    phone_entry.get().strip(),
                    email_entry.get().strip(),
                    client_type_var.get()
                )

                query = """
                INSERT INTO clients (first_name, last_name, phone, email, client_type)
                VALUES (%s, %s, %s, %s, %s)
                """

                result = self.execute_query(query, data)
                if result is not None:
                    self.refresh_data()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Клиент успешно добавлен")
                else:
                    messagebox.showerror("Ошибка", "Не удалось добавить клиента")

            except Exception as e:
                messagebox.showerror("Ошибка базы данных", f"Произошла ошибка:\n{str(e)}")

        # Функция очистки формы
        def clear_form():
            first_name_entry.delete(0, tk.END)
            last_name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            client_type_var.set("")

            # Сбрасываем стили
            first_name_entry.configure(style='TEntry')
            last_name_entry.configure(style='TEntry')
            phone_entry.configure(style='TEntry')
            email_entry.configure(style='TEntry')
            client_type_combo.configure(style='TCombobox')

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Очистить", command=clear_form, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=10)

        # Привязываем Enter к сохранению
        dialog.bind('<Return>', lambda e: save())

        # Фокус на первое поле
        first_name_entry.focus_set()

    def add_property_dialog(self, dialog):
        """Диалог добавления объекта - адаптивный"""
        # Получаем список клиентов и сотрудников
        clients = self.execute_query("SELECT id, first_name || ' ' || last_name FROM clients", fetch=True)
        employees = self.execute_query(
            "SELECT id, first_name || ' ' || last_name FROM employees WHERE is_active = true", fetch=True)

        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=self.padding, pady=self.padding)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Поля формы
        fields = [
            ("Адрес:", "entry"),
            ("Город:", "entry"),
            ("Тип:", "combo"),
            ("Комнат:", "entry"),
            ("Площадь (м²):", "entry"),
            ("Цена:", "entry"),
            ("Статус:", "combo"),
            ("Владелец:", "combo"),
            ("Агент:", "combo"),
        ]

        entries = {}
        combo_values = {
            "Тип:": ["apartment", "house", "commercial", "land"],
            "Статус:": ["active", "sold", "rented", "archived"],
            "Владелец:": [f"{c[0]} - {c[1]}" for c in clients] if clients else [],
            "Агент:": [f"{e[0]} - {e[1]}" for e in employees] if employees else [],
        }

        for i, (label, field_type) in enumerate(fields):
            ttk.Label(scrollable_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)

            if field_type == "entry":
                entry = ttk.Entry(scrollable_frame, width=30)
                if label == "Город:":
                    entry.insert(0, "Москва")
                entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
                entries[label] = entry
            elif field_type == "combo":
                var = tk.StringVar()
                if label == "Тип:":
                    var.set("apartment")
                elif label == "Статус:":
                    var.set("active")

                combo = ttk.Combobox(scrollable_frame, textvariable=var, values=combo_values[label],
                                     state="readonly", width=27)
                combo.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
                entries[label] = var

        def save():
            try:
                owner_id = int(entries["Владелец:"].get().split(" - ")[0]) if entries["Владелец:"].get() else None
                agent_id = int(entries["Агент:"].get().split(" - ")[0]) if entries["Агент:"].get() else None

                data = (
                    entries["Адрес:"].get(),
                    entries["Город:"].get(),
                    entries["Тип:"].get(),
                    int(entries["Комнат:"].get()) if entries["Комнат:"].get() else None,
                    float(entries["Площадь (м²):"].get()),
                    float(entries["Цена:"].get()),
                    entries["Статус:"].get(),
                    owner_id,
                    agent_id
                )

                query = """
                INSERT INTO properties (address, city, property_type, rooms, total_area, 
                                       price, status, owner_id, agent_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                self.execute_query(query, data)
                self.refresh_data()
                dialog.destroy()
                messagebox.showinfo("Успех", "Объект добавлен")
            except ValueError as e:
                messagebox.showerror("Ошибка", "Проверьте правильность ввода числовых значений")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        ttk.Button(scrollable_frame, text="Сохранить", command=save).grid(
            row=len(fields) + 1, column=0, columnspan=2, pady=20
        )

    def add_deal_dialog(self, dialog):
        """Диалог добавления сделки - адаптивный"""
        # Получаем данные для выпадающих списков
        properties = self.execute_query("SELECT id, address FROM properties", fetch=True)
        clients = self.execute_query("SELECT id, first_name || ' ' || last_name FROM clients", fetch=True)
        employees = self.execute_query(
            "SELECT id, first_name || ' ' || last_name FROM employees WHERE is_active = true", fetch=True)

        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=self.padding, pady=self.padding)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Поля формы
        fields = [
            ("Объект:", "combo"),
            ("Покупатель:", "combo"),
            ("Продавец:", "combo"),
            ("Агент:", "combo"),
            ("Цена сделки:", "entry"),
            ("Комиссия:", "entry"),
            ("Тип сделки:", "combo"),
        ]

        entries = {}
        combo_values = {
            "Объект:": [f"{p[0]} - {p[1]}" for p in properties] if properties else [],
            "Покупатель:": [f"{c[0]} - {c[1]}" for c in clients] if clients else [],
            "Продавец:": [f"{c[0]} - {c[1]}" for c in clients] if clients else [],
            "Агент:": [f"{e[0]} - {e[1]}" for e in employees] if employees else [],
            "Тип сделки:": ["sale", "rent"],
        }

        for i, (label, field_type) in enumerate(fields):
            ttk.Label(scrollable_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)

            if field_type == "entry":
                entry = ttk.Entry(scrollable_frame, width=30)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
                entries[label] = entry
            elif field_type == "combo":
                var = tk.StringVar()
                if label == "Тип сделки:":
                    var.set("sale")

                combo = ttk.Combobox(scrollable_frame, textvariable=var, values=combo_values[label],
                                     state="readonly", width=27)
                combo.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
                entries[label] = var

        def save():
            try:
                # Получаем ID из выбранных значений
                property_id = int(entries["Объект:"].get().split(" - ")[0]) if entries["Объект:"].get() else None
                buyer_id = int(entries["Покупатель:"].get().split(" - ")[0]) if entries["Покупатель:"].get() else None
                seller_id = int(entries["Продавец:"].get().split(" - ")[0]) if entries["Продавец:"].get() else None
                agent_id = int(entries["Агент:"].get().split(" - ")[0]) if entries["Агент:"].get() else None

                data = (
                    property_id,
                    buyer_id,
                    seller_id,
                    agent_id,
                    float(entries["Цена сделки:"].get()),
                    float(entries["Комиссия:"].get()),
                    entries["Тип сделки:"].get()
                )

                query = """
                INSERT INTO deals (property_id, buyer_id, seller_id, agent_id, 
                                 deal_price, commission_amount, deal_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                self.execute_query(query, data)
                self.refresh_data()
                dialog.destroy()
                messagebox.showinfo("Успех", "Сделка добавлена")
            except ValueError as e:
                messagebox.showerror("Ошибка", "Проверьте правильность ввода данных")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        ttk.Button(scrollable_frame, text="Сохранить", command=save).grid(
            row=len(fields) + 1, column=0, columnspan=2, pady=20
        )

    def add_viewing_dialog(self, dialog):
        """Диалог добавления просмотра - с календарем"""
        from tkinter import simpledialog
        import calendar

        properties = self.execute_query("SELECT id, address FROM properties", fetch=True)
        clients = self.execute_query("SELECT id, first_name || ' ' || last_name FROM clients", fetch=True)
        employees = self.execute_query(
            "SELECT id, first_name || ' ' || last_name FROM employees WHERE is_active = true", fetch=True)

        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=self.padding, pady=self.padding)

        # Стиль для ошибок
        style = ttk.Style()
        style.configure('Error.TEntry', fieldbackground='#FFE6E6', foreground='red')
        style.configure('Disabled.TEntry', foreground='gray')

        # Поля формы
        ttk.Label(main_frame, text="Объект:*", foreground='red').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        property_var = tk.StringVar()
        property_combo = ttk.Combobox(main_frame, textvariable=property_var, state="readonly", width=35)
        if properties:
            property_combo["values"] = [f"{p[0]} - {p[1]}" for p in properties]
        property_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Клиент:*", foreground='red').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        client_var = tk.StringVar()
        client_combo = ttk.Combobox(main_frame, textvariable=client_var, state="readonly", width=35)
        if clients:
            client_combo["values"] = [f"{c[0]} - {c[1]}" for c in clients]
        client_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Агент:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        agent_var = tk.StringVar()
        agent_combo = ttk.Combobox(main_frame, textvariable=agent_var, state="readonly", width=35)
        if employees:
            agent_combo["values"] = [f"{e[0]} - {e[1]}" for e in employees]
        agent_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Фрейм для выбора даты и времени
        datetime_frame = ttk.LabelFrame(main_frame, text="Дата и время просмотра *", padding=10)
        datetime_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky=tk.EW)

        # Текущая дата
        now = datetime.now()
        current_date = now.date()
        current_time = now.time()

        # Переменные для даты и времени
        date_var = tk.StringVar(value=current_date.strftime("%Y-%m-%d"))
        hour_var = tk.StringVar(value=str(current_time.hour).zfill(2))
        minute_var = tk.StringVar(value=str(current_time.minute).zfill(2))

        # Функция для обновления даты
        def update_date(year, month, day):
            date_var.set(f"{year}-{month:02d}-{day:02d}")
            validate_future_datetime()

        # Функция для отображения календаря
        def show_calendar():
            calendar_dialog = tk.Toplevel(dialog)
            calendar_dialog.title("Выбор даты")
            calendar_dialog.geometry("300x300")
            calendar_dialog.transient(dialog)
            calendar_dialog.grab_set()

            # Центрируем
            x = dialog.winfo_x() + (dialog.winfo_width() - 300) // 2
            y = dialog.winfo_y() + (dialog.winfo_height() - 300) // 2
            calendar_dialog.geometry(f"+{x}+{y}")

            # Текущая дата
            current = datetime.now()
            year = current.year
            month = current.month

            # Фрейм для управления месяцем/годом
            control_frame = ttk.Frame(calendar_dialog)
            control_frame.pack(pady=10)

            # Кнопки навигации
            def prev_month():
                nonlocal month, year
                month -= 1
                if month < 1:
                    month = 12
                    year -= 1
                update_calendar()

            def next_month():
                nonlocal month, year
                month += 1
                if month > 12:
                    month = 1
                    year += 1
                update_calendar()

            ttk.Button(control_frame, text="◀", width=3, command=prev_month).pack(side=tk.LEFT, padx=5)
            month_year_label = ttk.Label(control_frame, text="", font=('Arial', 10, 'bold'))
            month_year_label.pack(side=tk.LEFT, padx=10)
            ttk.Button(control_frame, text="▶", width=3, command=next_month).pack(side=tk.LEFT, padx=5)

            # Фрейм для дней недели
            days_frame = ttk.Frame(calendar_dialog)
            days_frame.pack()

            # Дни недели
            days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
            for i, day in enumerate(days):
                ttk.Label(days_frame, text=day, width=4, anchor='center').grid(row=0, column=i, padx=2, pady=2)

            # Фрейм для дней месяца
            days_grid_frame = ttk.Frame(calendar_dialog)
            days_grid_frame.pack()

            def update_calendar():
                # Очищаем старые дни
                for widget in days_grid_frame.winfo_children():
                    widget.destroy()

                # Обновляем заголовок
                month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                               'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
                month_year_label.configure(text=f"{month_names[month - 1]} {year}")

                # Получаем календарь
                cal = calendar.monthcalendar(year, month)

                # Отображаем дни
                for week_num, week in enumerate(cal):
                    for day_num, day in enumerate(week):
                        if day != 0:
                            # Проверяем, не прошедшая ли это дата
                            selected_date = datetime(year, month, day)
                            is_past = selected_date.date() < datetime.now().date()

                            if is_past:
                                btn = ttk.Label(days_grid_frame, text=str(day), width=4,
                                                background='#f0f0f0', foreground='gray')
                                btn.grid(row=week_num + 1, column=day_num, padx=2, pady=2)
                            else:
                                btn = ttk.Button(days_grid_frame, text=str(day), width=4,
                                                 command=lambda d=day: select_date(d))
                                btn.grid(row=week_num + 1, column=day_num, padx=2, pady=2)

            def select_date(day):
                update_date(year, month, day)
                calendar_dialog.destroy()

            # Инициализируем календарь
            update_calendar()

        # Функция для проверки будущей даты
        def validate_future_datetime():
            try:
                selected_date = datetime.strptime(date_var.get(), "%Y-%m-%d").date()
                selected_time = datetime.strptime(f"{hour_var.get()}:{minute_var.get()}", "%H:%M").time()
                selected_datetime = datetime.combine(selected_date, selected_time)

                current_datetime = datetime.now()

                if selected_datetime < current_datetime:
                    date_label.configure(foreground='red')
                    time_label.configure(text="Время в прошлом!", foreground='red')
                    return False
                else:
                    date_label.configure(foreground='green')
                    time_label.configure(text="Время в будущем ✓", foreground='green')
                    return True
            except:
                return False

        # Кнопка выбора даты
        date_label = ttk.Label(datetime_frame, text="Дата:")
        date_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Button(datetime_frame, text="📅 Выбрать дату", command=show_calendar, width=15).grid(
            row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Поле для отображения выбранной даты
        ttk.Label(datetime_frame, text="Выбранная дата:").grid(row=0, column=2, padx=(20, 5), pady=5, sticky=tk.W)
        date_display = ttk.Label(datetime_frame, textvariable=date_var, font=('Arial', 10, 'bold'))
        date_display.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        # Выбор времени
        ttk.Label(datetime_frame, text="Время:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        time_frame = ttk.Frame(datetime_frame)
        time_frame.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)

        # Часы
        hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=3,
                                  textvariable=hour_var, format="%02.0f")
        hour_spinbox.pack(side=tk.LEFT, padx=2)
        ttk.Label(time_frame, text=":").pack(side=tk.LEFT)

        # Минуты
        minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=3,
                                    textvariable=minute_var, format="%02.0f")
        minute_spinbox.pack(side=tk.LEFT, padx=2)

        # Метка проверки времени
        time_label = ttk.Label(datetime_frame, text="")
        time_label.grid(row=2, column=1, columnspan=3, padx=5, pady=(5, 0), sticky=tk.W)

        # Кнопка для установки текущего времени
        def set_current_time():
            now = datetime.now()
            hour_var.set(str(now.hour).zfill(2))
            minute_var.set(str(now.minute).zfill(2))
            validate_future_datetime()

        ttk.Button(datetime_frame, text="🕐 Текущее время", command=set_current_time, width=15).grid(
            row=3, column=1, padx=5, pady=10, sticky=tk.W)

        # Другие поля
        ttk.Label(main_frame, text="Статус:*", foreground='red').grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        status_var = tk.StringVar(value="scheduled")
        status_combo = ttk.Combobox(main_frame, textvariable=status_var,
                                    values=["scheduled", "completed", "cancelled"], state="readonly", width=35)
        status_combo.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Отзыв клиента:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        feedback_text = tk.Text(main_frame, height=4, width=35)
        feedback_text.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        # Функция сохранения
        def save():
            # Проверка обязательных полей
            if not property_var.get():
                messagebox.showerror("Ошибка", "Выберите объект недвижимости")
                return

            if not client_var.get():
                messagebox.showerror("Ошибка", "Выберите клиента")
                return

            # Проверка даты и времени
            if not validate_future_datetime():
                messagebox.showerror("Ошибка", "Нельзя выбрать прошедшее время")
                return

            try:
                property_id = int(property_var.get().split(" - ")[0])
                client_id = int(client_var.get().split(" - ")[0])
                agent_id = int(agent_var.get().split(" - ")[0]) if agent_var.get() else None

                # Формируем дату-время
                datetime_str = f"{date_var.get()} {hour_var.get()}:{minute_var.get()}"

                data = (
                    property_id,
                    client_id,
                    agent_id,
                    datetime_str,
                    status_var.get(),
                    feedback_text.get("1.0", "end-1c").strip()
                )

                query = """
                INSERT INTO viewings (property_id, client_id, agent_id, viewing_date, status, client_feedback)
                VALUES (%s, %s, %s, %s, %s, %s)
                """

                self.execute_query(query, data)
                self.refresh_data()
                dialog.destroy()
                messagebox.showinfo("Успех", "Просмотр добавлен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении:\n{str(e)}")

        # Привязываем проверку при изменении времени
        hour_var.trace('w', lambda *args: validate_future_datetime())
        minute_var.trace('w', lambda *args: validate_future_datetime())
        date_var.trace('w', lambda *args: validate_future_datetime())

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)

        # Инициализируем проверку
        validate_future_datetime()

        # Фокус
        property_combo.focus_set()

    def add_service_dialog(self, dialog):
        """Диалог добавления услуги - адаптивный"""
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=self.padding, pady=self.padding)

        # Поля формы
        ttk.Label(main_frame, text="Название услуги:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(main_frame, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Описание:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        desc_entry = ttk.Entry(main_frame, width=30)
        desc_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Цена:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        price_entry = ttk.Entry(main_frame, width=30)
        price_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Срок (дней):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        duration_entry = ttk.Entry(main_frame, width=30)
        duration_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        def save():
            try:
                data = (
                    name_entry.get(),
                    desc_entry.get(),
                    float(price_entry.get()) if price_entry.get() else None,
                    int(duration_entry.get()) if duration_entry.get() else None
                )

                query = """
                INSERT INTO services (service_name, description, standard_price, duration_days)
                VALUES (%s, %s, %s, %s)
                """

                self.execute_query(query, data)
                self.refresh_data()
                dialog.destroy()
                messagebox.showinfo("Успех", "Услуга добавлена")
            except ValueError as e:
                messagebox.showerror("Ошибка", "Проверьте правильность ввода числовых значений")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        ttk.Button(main_frame, text="Сохранить", command=save).grid(row=4, column=0, columnspan=2, pady=20)

    def search_dialog(self):
        """Диалог поиска"""
        if self.current_table == "reports":
            messagebox.showinfo("Поиск", "Поиск недоступен в режиме отчетов")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Поиск")

        dialog_width = min(400, self.root.winfo_width() - 100)
        dialog_height = min(300, self.root.winfo_height() - 100)
        dialog.geometry(f"{dialog_width}x{dialog_height}")

        dialog.transient(self.root)
        dialog.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() - dialog_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog_height) // 2
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding=self.padding)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Поиск:").pack(anchor=tk.W)
        search_entry = ttk.Entry(main_frame, width=30)
        search_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(main_frame, text="Искать в:").pack(anchor=tk.W)

        # Определяем доступные колонки для поиска
        if self.current_table == "employees":
            columns = ["Имя", "Фамилия", "Телефон", "Email"]
        elif self.current_table == "clients":
            columns = ["Имя", "Фамилия", "Телефон", "Email", "Тип"]
        elif self.current_table == "properties":
            columns = ["Адрес", "Город", "Тип", "Статус"]
        elif self.current_table == "deals":
            columns = ["Тип"]
        elif self.current_table == "viewings":
            columns = ["Статус", "Отзыв"]
        elif self.current_table == "services":
            columns = ["Название", "Описание"]
        else:
            columns = []

        column_var = tk.StringVar(value=columns[0] if columns else "")
        column_combo = ttk.Combobox(main_frame, textvariable=column_var, values=columns, state="readonly")
        column_combo.pack(fill=tk.X, pady=(0, 20))

        def search():
            search_text = search_entry.get().lower()
            column_name = column_var.get()

            if not search_text:
                messagebox.showwarning("Внимание", "Введите текст для поиска")
                return

            # Очищаем текущее выделение
            for item in self.tree.selection():
                self.tree.selection_remove(item)

            # Ищем совпадения
            found_items = []
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']

                # Определяем индекс колонки для поиска
                if column_name == "Имя":
                    col_index = 1
                elif column_name == "Фамилия":
                    col_index = 2
                elif column_name == "Телефон":
                    col_index = 3
                elif column_name == "Email":
                    col_index = 4
                elif column_name == "Тип":
                    col_index = 5 if self.current_table == "clients" else 7 if self.current_table == "deals" else 3
                elif column_name == "Адрес":
                    col_index = 1
                elif column_name == "Город":
                    col_index = 2
                elif column_name == "Статус":
                    col_index = 7 if self.current_table == "properties" else 4
                elif column_name == "Отзыв":
                    col_index = 5
                elif column_name == "Название":
                    col_index = 1
                elif column_name == "Описание":
                    col_index = 2
                else:
                    col_index = 0

                if col_index < len(values) and search_text in str(values[col_index]).lower():
                    found_items.append(item)

            if found_items:
                # Выделяем найденные элементы
                for item in found_items:
                    self.tree.selection_add(item)
                    self.tree.see(item)

                self.status_var.set(f"Найдено записей: {len(found_items)}")
                dialog.destroy()
            else:
                messagebox.showinfo("Результаты поиска", "Совпадений не найдено")

        ttk.Button(main_frame, text="Искать", command=search).pack(pady=10)

    def delete_record(self):
        """Удалить выбранную запись"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите запись для удаления")
            return

        if not messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
            return

        item = self.tree.item(selection[0])
        record_id = item['values'][0]

        try:
            if self.current_table == "employees":
                query = "DELETE FROM employees WHERE id = %s"
            elif self.current_table == "clients":
                query = "DELETE FROM clients WHERE id = %s"
            elif self.current_table == "properties":
                query = "DELETE FROM properties WHERE id = %s"
            elif self.current_table == "deals":
                query = "DELETE FROM deals WHERE id = %s"
            elif self.current_table == "viewings":
                query = "DELETE FROM viewings WHERE id = %s"
            elif self.current_table == "services":
                query = "DELETE FROM services WHERE id = %s"
            else:
                return

            self.execute_query(query, (record_id,))
            self.refresh_data()
            messagebox.showinfo("Успех", "Запись удалена")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить запись:\n{str(e)}")

    def refresh_data(self):
        """Обновить данные текущей таблицы"""
        if self.current_table == "reports":
            # Если мы в режиме отчетов, просто обновляем отчеты
            self.show_reports()
        else:
            # Для всех других таблиц показываем Treeview
            if hasattr(self, 'report_frame'):
                self.report_frame.destroy()
                delattr(self, 'report_frame')

            self.tree_frame.grid()

            # Обновляем данные текущей таблицы
            if self.current_table == "employees":
                self.show_employees()
            elif self.current_table == "clients":
                self.show_clients()
            elif self.current_table == "properties":
                self.show_properties()
            elif self.current_table == "deals":
                self.show_deals()
            elif self.current_table == "viewings":
                self.show_viewings()
            elif self.current_table == "services":
                self.show_services()

    def __del__(self):
        """Закрыть соединение с БД при завершении"""
        if self.conn:
            self.conn.close()

    def edit_employee_dialog(self, dialog, record_id, values):
        pass


def main():
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
