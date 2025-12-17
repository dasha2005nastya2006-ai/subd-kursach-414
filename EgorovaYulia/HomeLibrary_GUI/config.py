import os
from pathlib import Path
from dotenv import load_dotenv

# Получаем путь к корневой директории
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем .env из корневой директории проекта
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Загружен .env файл: {env_path}")
else:
    print(f"⚠ Файл .env не найден: {env_path}")
    # Используем значения по умолчанию
    load_dotenv()


class Config:
    # Настройки базы данных ИЗ .env файла
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'homelibrary')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '123456789')

    # Выводим настройки для проверки (можно убрать после отладки)
    print(f"\nНастройки БД:")
    print(f"  Хост: {DB_HOST}:{DB_PORT}")
    print(f"  База: {DB_NAME}")
    print(f"  Пользователь: {DB_USER}")

    # Настройки приложения
    APP_TITLE = "Домашняя библиотека"
    APP_VERSION = "1.0.0"

    # Пути к файлам
    STATIC_PATH = os.path.join(os.path.dirname(__file__), '..', 'static')
    ICONS_PATH = os.path.join(STATIC_PATH, 'icons')
    STYLES_PATH = os.path.join(STATIC_PATH, 'styles.css')

    # Цвета приложения
    PRIMARY_COLOR = "#2c3e50"
    SECONDARY_COLOR = "#3498db"
    ACCENT_COLOR = "#e74c3c"
    SUCCESS_COLOR = "#27ae60"
    WARNING_COLOR = "#f39c12"

    # Размеры окон
    LOGIN_WINDOW_SIZE = (400, 300)
    MAIN_WINDOW_SIZE = (1200, 700)
