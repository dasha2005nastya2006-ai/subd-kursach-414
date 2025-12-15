HomeLibraryGUI/
│
├── main.py                    # Точка входа в приложение
├── database.py                # Модуль работы с PostgreSQL
├── config.py                  # Настройки подключения к БД
├── .env                       # Переменные окружения (пароли, настройки)
├── requirements.txt           # Зависимости Python
├── library.db                 # SQLite база данных (альтернативная)
│
├── gui/                       # Графический интерфейс
│   ├── __init__.py
│   ├── auth_window.py         # Окно авторизации
│   ├── main_window.py         # Главное окно с меню
│   ├── books_window.py        # Управление книгами
│   ├── loans_window.py        # Управление выдачами
│   ├── users_window.py        # Управление пользователями
│   └── reports_window.py      # Отчеты и статистика
│
├── static/                    # Статические файлы
│   └── styles.css             # CSS стили интерфейса
