***

<p align="center">Министерство образования, науки и молодежной политики Республики Коми</p>

<p align="center">ГПОУ "Сыктывкарский политехнический техникум"</p>






<p align="center">Курсовая работа</p>

<p align="center">тема: Разработка базы данных и программного обеспечения для склада автотоваров</p>
















<p align="right"> выполнил </p>

<p align="right">студент 4 курса </p>

<p align="right">414 группы </p>

<p align="right">Ломовицкий Алексей Игоревич</p>



<p align="right">проверил</p>

<p align="right">Пунгин И.В.</p>

<p align="right">дата проверки: ______________</p>










<p align="center">Сыктывкар, 2025</p>

## <a id="content">Содержание</a>

1. [Введение](#introduction)
    - [Цель работы](#target)
    - [Задачи работы](#tasks)
2. [Основная часть](#main)
    - [Анализ предметной области. Постановка задачи](#analysis)
    - [Инфологическая (концептуальная) модель базы данных](#infological_model)
    - [Логическая структура БД](#logical_structure)
    - [Физическая структура базы данных](#physical_structure)
    - [Реализация проекта в среде конкретной СУБД](#project_realization)
    - [Разработка клиентского приложения](#client_app)
3. [Заключение](#conclusion)
4. [Список использованных информационных источников](#literature)
5. [Приложения](#applications)

***

## <a id="introduction">Введение</a>
В современном мире автобизнеса понимание того, какая деталь, в каком количестве и где именно хранится, является ядром логистического процесса. Огромная номенклатура автозапчастей, насчитывающая тысячи наименований, наличие аналогов и товаров с ограниченным сроком годности (масла, автохимия) делают ручной учет невозможным. Всё это обуславливает актуальность разработки базы данных (БД) для склада автотоваров. Эта система должна обеспечивать удобный доступ к информации о наличии запчастей, их точном местоположении (адресное хранение), а также фиксировать все движения товаров (приход, расход, списание).

Внедрение базы данных позволит ускорить процесс приемки и отгрузки товаров, сократить время поиска нужной детали кладовщиком и минимизировать финансовые потери от пересортицы и просрочки. Ключевой задачей разработки является создание надежного хранилища данных и интуитивно понятного интерфейса для взаимодействия с ним. Система должна обрабатывать транзакции в реальном времени и обеспечивать целостность данных, исключая появление отрицательных остатков.

Реализация данного проекта создаст эффективную систему, способную хранить и анализировать данные о товарообороте. Таким образом, курсовая работа направлена на разработку базы данных и программного обеспечения для склада автотоваров, отвечающих современным требованиям логистики.

#### <a id="target">Цель работы</a>
Целью данной курсовой работы является разработка базы данных и клиентского приложения для склада автотоваров, которая позволит эффективно управлять товарными запасами, отслеживать сроки годности и автоматизировать складские операции. В рамках работы предполагается несколько этапов:
1.	**Создание структуры базы данных:** Разработать схему базы данных, произвести анализ и нормализацию, чтобы обеспечить целостность данных. Важно предусмотреть хранение справочников (бренды, категории) и транзакционных данных (накладные).
2.	**Реализация функционала для управления данными:** Разработка триггеров и хранимых процедур для автоматического пересчета остатков при оформлении накладных. Это исключит человеческий фактор и ошибки в расчетах.
3.	**Создание представлений для отображения информации:** Реализация представлений (Views), которые будут отображать актуальные остатки с расшифровкой брендов и статусы сроков годности.
4.	**Обеспечение целостности и безопасности:** Разработка ограничений (Constraints), запрещающих отрицательные цены и остатки, а также удаление справочных данных, используемых в товарообороте.
5.	**Разработка клиентского интерфейса:** Создание приложения на языке Python, обеспечивающего удобное рабочее место для кладовщика.
6.	**Документирование процесса:** Подготовка SQL-скриптов и описания архитектуры системы.

#### <a id="tasks">Задачи работы</a>
Для достижения поставленной цели необходимо решить следующие задачи:
1.	**Анализировать предметную область склада автозапчастей.** Изучить специфику адресного хранения, партионного учета и кросс-номеров. Определить необходимые входные и выходные данные.
2.	**Проектировать структуру базы данных.** Определить сущности (Товары, Контрагенты, Движения), их атрибуты и связи. Построить инфологическую модель.
3.	**Выбрать и обосновать СУБД.** Провести анализ и обосновать выбор PostgreSQL как наиболее подходящей системы для надежного хранения данных с поддержкой ACID.
4.	**Реализовать структуру базы данных на выбранной СУБД.** Написать SQL-код для создания таблиц, индексов и ограничений.
5.	**Автоматизировать бизнес-логику.** Разработать триггеры на языке PL/pgSQL для контроля остатков.
6.	**Разработать программное обеспечение.** Создать приложение с графическим интерфейсом (GUI) для взаимодействия с базой данных.
7.	**Осуществить тестирование.** Проверить работу системы на тестовых данных, убедиться в корректности расчетов и срабатывании ограничений.

## <a id="main">Основная часть</a>

#### <a id="analysis">Анализ предметной области. Постановка задачи</a>
1.	**Описание предметной области и функции решаемых задач**
  - **Предметная область** — складское хозяйство магазина автозапчастей. Система направлена на автоматизацию учета материальных ценностей.
  - **Функции решаемых задач:**
    - **Адресное хранение:** Фиксация точного места расположения товара (Зона-Ряд-Полка) для ускорения сборки заказов.
    - **Партионный учет:** Регистрация каждой операции (приход/расход) отдельным документом с привязкой к контрагенту.
    - **Контроль сроков годности:** Отслеживание товаров (масла, химия), срок реализации которых подходит к концу.
    - **Единый реестр контрагентов:** Учет поставщиков и клиентов в единой базе.

2.	**Перечень входных данных.**
	  - **Справочники:**
    	- Категории товаров (Двигатель, Подвеска, Кузов);
    	- Производители (Бренды);
  	- **Товарная номенклатура:**
 	   - Артикул (Part Number);
	    - Наименование;
    	- Базовая цена;
    	- Код ячейки хранения;
  	- **Данные о контрагентах:**
	    - Название организации;
    	- Тип (Поставщик/Клиент);
    	- Контакты;
  	- **Первичные документы:**
    	- Накладные на приход;
    	- Накладные на отгрузку;
    	- Акты списания.

3.	**Перечень выходных данных.**
	  - **Отчет об остатках:** Актуальное количество товаров в разрезе ячеек хранения и брендов.
 	 - **Монитор сроков годности:** Список товаров, истекающих в ближайшие 30 дней.
	  - **История движения:** Детальный отчет о том, когда, кому и по какой цене был отгружен конкретный товар.

4.	**Ограничения предметной области.**
	  - **Отрицательные остатки:** Система не должна позволять списывать товара больше, чем есть в наличии.
	  - **Целостность:** Нельзя удалить категорию или производителя, если к ним привязаны товары.
	  - **Уникальность:** В рамках одного бренда артикул должен быть уникален.

5.	**Взаимодействие с другими программами.**
    База данных проектируется как backend-составляющая. Реализовано взаимодействие с клиентским приложением на языке Python (через драйвер `psycopg2`) для работы кладовщика. Возможна интеграция с бухгалтерскими системами (1С).

#### <a id="infological_model">Инфологическая (концептуальная) модель базы данных</a>
Концептуальная модель описывает структуру данных без привязки к конкретной СУБД.

1.	**Выделение информационных объектов:**
  - **Товары (Products)** — центральная сущность.
  - **Категории (Categories)** — справочник групп товаров.
  - **Производители (Manufacturers)** — справочник брендов.
  - **Контрагенты (Contractors)** — поставщики и клиенты.
  - **Движения (Stock Movements)** — шапки накладных.
  - **Позиции движения (Movement Items)** — строки накладных.

2.	**Определение атрибутов объектов:**
  - **Товар:** Артикул, Название, Ячейка, Остаток, Цена, Срок годности.
  - **Движение:** Дата, Тип операции (IN/OUT), Контрагент.
  - **Позиция:** Ссылка на товар, Количество, Цена операции.

3.	**Определение отношений и мощности:**
  - **Категория — Товар (1:M):** Одна категория содержит много товаров.
  - **Производитель — Товар (1:M):** Один бренд выпускает много товаров.
  - **Контрагент — Движение (1:M):** Один контрагент участвует во множестве накладных.
  - **Движение — Позиция (1:M):** Накладная состоит из строк.
  - **Товар — Позиция (1:M):** Товар фигурирует во множестве накладных.

4.	**Построение концептуальной модели.**
    *(Здесь место для ER-диаграммы)*

#### <a id="logical_structure">Логическая структура базы данных</a>
Логическая структура представляет собой детализированное описание таблиц, приведенных к 3-й нормальной форме (3NF).

**Определение таблиц и их атрибутов:**

1.	**Таблица Categories (Категории)**
    - `category_id` (PK) — SERIAL.
    - `name` — VARCHAR, UNIQUE, NOT NULL.

2.	**Таблица Manufacturers (Производители)**
    - `manufacturer_id` (PK) — SERIAL.
    - `name` — VARCHAR, UNIQUE, NOT NULL.
    - `country` — VARCHAR.

3.	**Таблица Contractors (Контрагенты)**
    - `contractor_id` (PK) — SERIAL.
    - `name` — VARCHAR, NOT NULL.
    - `type` — VARCHAR (Check: 'supplier'/'client').

4.	**Таблица Products (Товары)**
    - `product_id` (PK) — SERIAL.
    - `part_number` — VARCHAR, NOT NULL.
    - `name` — VARCHAR, NOT NULL.
    - `location_code` — VARCHAR (Адрес ячейки).
    - `stock_quantity` — INTEGER (Check >= 0).
    - `price` — NUMERIC(10,2).
    - `expiration_date` — DATE.
    - `category_id` (FK), `manufacturer_id` (FK).

5.	**Таблица Stock_Movements (Движения)**
    - `movement_id` (PK) — SERIAL.
    - `created_at` — TIMESTAMP.
    - `operation_type` — VARCHAR (Check: 'in'/'out'/'writeoff').
    - `contractor_id` (FK).

6.	**Таблица Movement_Items (Позиции)**
    - `item_id` (PK) — SERIAL.
    - `movement_id` (FK).
    - `product_id` (FK).
    - `quantity` — INTEGER (Check > 0).
    - `price` — NUMERIC(10,2).

**Нормализация:**
Структура находится в 3NF: все атрибуты атомарны, неключевые атрибуты зависят только от первичного ключа, транзитивные зависимости устранены путем вынесения справочников.

## <a id="physical_structure">Физическая структура базы данных</a>

Физический уровень базы данных отвечает за непосредственное хранение данных. Для реализации проекта выбрана СУБД **PostgreSQL**, так как она обеспечивает надежность транзакций (ACID) и поддерживает мощный процедурный язык PL/pgSQL.

#### <a id="ps1">1. Выбор типов данных</a>

Правильный выбор типов данных критичен для точности и производительности:

- **SERIAL:** Для автоматической генерации уникальных ключей (`id`).
- **VARCHAR(n):** Для хранения текстовых данных (названия, артикулы). Экономит место по сравнению с `CHAR`.
- **NUMERIC(10, 2):** Для цен. Использование `FLOAT` недопустимо в финансовых системах из-за ошибок округления. `NUMERIC` хранит точные значения.
- **INTEGER:** Для количества товаров.
- **TIMESTAMP / DATE:** Для фиксации времени операций и сроков годности.

#### <a id="ps2">2. Оптимизация индексов</a>

Индексы ускоряют доступ к данным.
- **Первичные ключи (PK):** PostgreSQL автоматически создает B-Tree индексы для всех первичных ключей.
- **Внешние ключи (FK):** Индексирование полей `product_id` в таблице `movement_items` ускоряет JOIN-запросы при формировании отчетов.
- **Уникальные индексы:** Поля `part_number` (в связке с брендом) и `name` в справочниках требуют уникальности.

#### <a id="ps3">3. Архитектура хранения и MVCC</a>

PostgreSQL использует механизм многоверсионного управления конкурентным доступом (MVCC).
**Преимущество:** Операции чтения (формирование отчета об остатках) не блокируют операции записи (проведение накладной). Это позволяет менеджеру видеть актуальные остатки, пока кладовщик принимает товар, без задержек системы.

#### <a id="ps4">4. Политика обеспечения целостности данных</a>

PostgreSQL предоставляет мощные инструменты защиты данных, которые были задействованы в проекте:

- **CHECK constraints:**
    - `CHECK (stock_quantity >= 0)`: Гарантирует, что на складе не возникнет отрицательного остатка, даже если в программе произойдет сбой.
    - `CHECK (price >= 0)`: Запрет на отрицательные цены.
    - `CHECK (operation_type IN ...)`: Ограничение списка допустимых операций.
- **Foreign Keys:**
    - `ON DELETE SET NULL`: Если удалить категорию, товары останутся, но без категории.
    - `ON DELETE CASCADE`: Если удалить накладную, удалятся все её позиции (чтобы не было "мусора").

#### <a id="ps5">5. Параметры хранения и резервное копирование</a>

Для защиты данных от сбоев необходимо регулярное резервное копирование.
**Логическое резервное копирование (`pg_dump`):**
Позволяет выгрузить структуру и данные в SQL-файл. Это основной метод для переноса базы между серверами.
Пример команды:
```bash
pg_dump -U postgres -d autoparts_db -f backup.sql
```
Это обеспечивает возможность восстановления системы в случае критического сбоя оборудования.

#### <a id="ps6">6. SQL-код создания таблиц с физической структурой</a>

Пример реализации основной таблицы товаров:
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    part_number VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    location_code VARCHAR(20) DEFAULT 'RECEPTION', 
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    expiration_date DATE,
    category_id INTEGER REFERENCES categories(category_id) ON DELETE SET NULL,
    manufacturer_id INTEGER REFERENCES manufacturers(manufacturer_id) ON DELETE SET NULL
);
```
*(Полный код представлен в Приложении А)*

#### <a id="project_realization">Реализация проекта в среде конкретной СУБД</a>

Этот раздел описывает практическую реализацию логики базы данных.

1.  **Создание таблиц:** (См. Приложение А).

2.  **Создание представлений (Views):**
    Для удобства работы и интеграции с ПО реализованы представления.
    
    *Представление для мониторинга просроченных товаров:*
    ```sql
    CREATE OR REPLACE VIEW v_expiring_goods AS
    SELECT name, location_code, expiration_date 
    FROM products 
    WHERE expiration_date <= (CURRENT_DATE + INTERVAL '30 days')
    AND stock_quantity > 0;
    ```
    
    *Представление складской справки:*
    ```sql
    CREATE OR REPLACE VIEW v_warehouse_stock AS
    SELECT p.part_number, p.name, m.name AS brand, p.stock_quantity, p.price
    FROM products p
    LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id;
    ```

3.  **Хранимые процедуры и триггеры:**
    Ключевой элемент автоматизации — триггер пересчета остатков. Он гарантирует согласованность данных между журналом операций и таблицей товаров.
    
    ```sql
    CREATE OR REPLACE FUNCTION update_stock_on_movement() RETURNS TRIGGER AS $$
    DECLARE op_type VARCHAR(10);
    BEGIN
        SELECT operation_type INTO op_type FROM stock_movements WHERE movement_id = NEW.movement_id;
        
        IF op_type = 'in' THEN
            UPDATE products SET stock_quantity = stock_quantity + NEW.quantity WHERE product_id = NEW.product_id;
        ELSIF op_type IN ('out', 'writeoff') THEN
            IF (SELECT stock_quantity FROM products WHERE product_id = NEW.product_id) < NEW.quantity THEN
                RAISE EXCEPTION 'Недостаточно товара!';
            END IF;
            UPDATE products SET stock_quantity = stock_quantity - NEW.quantity WHERE product_id = NEW.product_id;
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER trg_update_stock AFTER INSERT ON movement_items
    FOR EACH ROW EXECUTE FUNCTION update_stock_on_movement();
    ```

4.  **Хранимые процедуры для добавления данных (API БД):**
    Для упрощения работы клиентского приложения созданы обертки над `INSERT`.
    
    *Процедура добавления нового товара:*
    ```sql
    CREATE OR REPLACE PROCEDURE pr_add_product(
        _part_number varchar, _name varchar, _price numeric, _loc varchar
    ) LANGUAGE plpgsql AS $$
    BEGIN
        INSERT INTO products (part_number, name, price, location_code)
        VALUES (_part_number, _name, _price, _loc);
    END; $$;
    ```

5.  **Назначение прав доступа:**
    *   **Роль `storekeeper`:** Разрешен `SELECT` ко всем таблицам, `INSERT` в таблицы движений.
    *   **Роль `manager`:** Полный доступ к справочникам и отчетам.

#### <a id="client_app">Разработка клиентского приложения</a>

Для взаимодействия с базой данных разработано приложение на языке **Python** с использованием библиотеки `tkinter` (GUI) и драйвера `psycopg2`.

**Функционал приложения:**
1.  **Просмотр остатков:** Отображение данных из представления `v_warehouse_stock` в табличном виде.
2.  **Оформление операций:** Форма для ввода ID товара, количества и выбора типа операции (Приход/Расход). Приложение отправляет SQL-запросы, которые активируют триггеры в БД.
3.  **Обработка ошибок:** Если БД возвращает ошибку (например, нарушение `CHECK` при попытке уйти в минус), приложение выводит понятное сообщение пользователю.

*(Код приложения представлен в Приложении Б).*

## <a id="conclusion">Заключение</a>

В результате выполнения курсовой работы была разработана база данных и программное обеспечение для автоматизации склада автотоваров.
Основные достижения и выводы:
- **Анализ:** Определены ключевые требования (адресное хранение, партионный учет).
- **Структура БД:** Создана нормализованная схема (3NF), исключающая дублирование.
- **Физическая реализация:** Использованы возможности PostgreSQL (типы данных, индексы, MVCC) для обеспечения высокой производительности.
- **Автоматизация:** Реализована серверная логика (триггеры PL/pgSQL), которая полностью исключает ошибки в расчетах остатков и защищает от отрицательных значений.
- **Интерфейс:** Разработано приложение на Python, позволяющее удобно работать с системой.

Разработанная система готова к внедрению на предприятиях малого и среднего бизнеса в сфере автозапчастей.

## <a id="literature">Список использованных информационных источников</a>
1.	Дейт К. Дж. Введение в системы баз данных. – 8-е изд. – М.: Вильямс, 2016.
2.	Официальная документация PostgreSQL [Электронный ресурс]. – Режим доступа: https://www.postgresql.org/docs/
3.	Моргунов Е.П. PostgreSQL. Основы языка SQL. – СПб.: БХВ-Петербург, 2018.
4.	Луц М. Программирование на Python, том 1. – 4-е изд. – СПб.: Символ-Плюс, 2011.
5.	Документация библиотеки Psycopg2 [Электронный ресурс]. – Режим доступа: https://www.psycopg.org/docs/

## <a id="applications">Приложения</a>

#### Приложение А: SQL-запросы на создание структуры БД

```sql
-- 1. ОЧИСТКА
DROP VIEW IF EXISTS v_expiring_goods;
DROP VIEW IF EXISTS v_warehouse_stock;
DROP TABLE IF EXISTS movement_items CASCADE;
DROP TABLE IF EXISTS stock_movements CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS contractors CASCADE;
DROP TABLE IF EXISTS manufacturers CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- 2. ТАБЛИЦЫ
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE manufacturers (
    manufacturer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(50)
);

CREATE TABLE contractors (
    contractor_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('supplier', 'client')),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    part_number VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    location_code VARCHAR(20) DEFAULT 'RECEPTION', 
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    expiration_date DATE,
    category_id INTEGER REFERENCES categories(category_id) ON DELETE SET NULL,
    manufacturer_id INTEGER REFERENCES manufacturers(manufacturer_id) ON DELETE SET NULL
);

CREATE TABLE stock_movements (
    movement_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operation_type VARCHAR(10) NOT NULL CHECK (operation_type IN ('in', 'out', 'writeoff')),
    contractor_id INTEGER REFERENCES contractors(contractor_id) ON DELETE SET NULL,
    comments TEXT
);

CREATE TABLE movement_items (
    item_id SERIAL PRIMARY KEY,
    movement_id INTEGER REFERENCES stock_movements(movement_id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(product_id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price NUMERIC(10, 2) NOT NULL
);

-- 3. ТРИГГЕРЫ
CREATE OR REPLACE FUNCTION update_stock_on_movement()
RETURNS TRIGGER AS $$
DECLARE op_type VARCHAR(10);
BEGIN
    SELECT operation_type INTO op_type FROM stock_movements WHERE movement_id = NEW.movement_id;
    IF op_type = 'in' THEN
        UPDATE products SET stock_quantity = stock_quantity + NEW.quantity WHERE product_id = NEW.product_id;
    ELSIF op_type IN ('out', 'writeoff') THEN
        IF (SELECT stock_quantity FROM products WHERE product_id = NEW.product_id) < NEW.quantity THEN
            RAISE EXCEPTION 'Ошибка: Недостаточно товара!';
        END IF;
        UPDATE products SET stock_quantity = stock_quantity - NEW.quantity WHERE product_id = NEW.product_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_stock
AFTER INSERT ON movement_items
FOR EACH ROW EXECUTE FUNCTION update_stock_on_movement();
```

#### Приложение Б: Исходный код приложения (Python)

```python
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",
    "password": "YOUR_PASSWORD", 
    "database": "autoparts_db"
}

class WarehouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("АРМ Склад Автотоваров")
        self.root.geometry("900x600")
        self.conn = None
        if not self.connect_db(): root.destroy(); return

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        self.tab_stock = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_stock, text="Складские остатки")
        self.setup_stock_tab()
        self.tab_ops = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ops, text="Операции")
        self.setup_ops_tab()
        self.refresh_stock()

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return False

    def setup_stock_tab(self):
        ttk.Button(self.tab_stock, text="Обновить", command=self.refresh_stock).pack(pady=10)
        cols = ("art", "name", "loc", "qty", "price")
        self.tree = ttk.Treeview(self.tab_stock, columns=cols, show="headings")
        for c, h in zip(cols, ["Артикул", "Название", "Ячейка", "Остаток", "Цена"]):
            self.tree.heading(c, text=h)
        self.tree.pack(expand=True, fill='both')

    def setup_ops_tab(self):
        f = ttk.Frame(self.tab_ops); f.pack(pady=20)
        ttk.Label(f, text="ID Товара:").grid(row=0, column=0)
        self.e_id = ttk.Entry(f); self.e_id.grid(row=0, column=1)
        ttk.Label(f, text="Кол-во:").grid(row=1, column=0)
        self.e_qty = ttk.Entry(f); self.e_qty.grid(row=1, column=1)
        self.v_op = tk.StringVar(value="in")
        ttk.Radiobutton(f, text="Приход", variable=self.v_op, value="in").grid(row=2, column=1)
        ttk.Radiobutton(f, text="Расход", variable=self.v_op, value="out").grid(row=3, column=1)
        ttk.Button(f, text="Выполнить", command=self.run_op).grid(row=4, column=0, columnspan=2, pady=10)

    def refresh_stock(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT part_number, name, location_code, stock_quantity, price FROM products")
            for row in cur.fetchall(): self.tree.insert("", tk.END, values=row)
        except Exception as e: messagebox.showerror("Error", str(e))

    def run_op(self):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO stock_movements (operation_type, contractor_id) VALUES (%s, 1) RETURNING movement_id", (self.v_op.get(),))
            mid = cur.fetchone()[0]
            cur.execute("SELECT price FROM products WHERE product_id=%s", (self.e_id.get(),))
            price = cur.fetchone()[0]
            cur.execute("INSERT INTO movement_items (movement_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)", (mid, self.e_id.get(), self.e_qty.get(), price))
            self.conn.commit()
            messagebox.showinfo("OK", "Успешно")
            self.refresh_stock()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    WarehouseApp(root)
    root.mainloop()
```

[Вернуться к содержанию](#content)
