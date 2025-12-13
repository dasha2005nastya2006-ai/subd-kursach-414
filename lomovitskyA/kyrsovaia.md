
### <p align="center"> Министерство образования, науки и молодежной политики Республики Коми

### <p align="center"> ГПОУ «Сыктывкарский политехнический техникум»

## <p align="center"> Курсовая работа

## <p align="center"> тема: Разработка базы данных для склада автотоваров </p>

#### <p align="right"> выполнил

 <p align="right">студент 4 курса

<p align="right">414 группы

<p align="right">Ломовицкий Алексей Игоревич 

#### <p align="right">проверил

<p align="right">Пунгин И.В.

<p align="right">дата проверки:

<p align="center">Сыктывкар, 2025 г.

***

## Задание на курсовую работу по МДК 11.01 "Технология разработки и защиты баз данных"

Специальность: <ins> 09.02.07 "Информационные системы и программирование"  </ins>

Тема курсовой работы: Разработка базы данных для склада автотоваров

Срок представления работы к защите: <ins> 22 декабря 2025 года. </ins>

Перечень подлежащих разработке вопросов:

1. **Анализ предметной области. Постановка задачи.**
    1.1. Описание предметной области и функции решаемых задач (адресное хранение, партионный учет).
    1.2. Перечень входных данных (накладные поставщиков, номенклатура).
    1.3. Перечень выходных данных (отчеты об остатках, неликвид, просрочка).
    1.4. Ограничения предметной области (отрицательные остатки, контроль сроков).
    1.5. Взаимодействие с другими программами.

2. **Инфологическая (концептуальная) модель базы данных.**
    2.1. Выделение информационных объектов (Товары, Контрагенты, Движения).
    2.2. Определение атрибутов объектов.
    2.3. Определение отношений и мощности отношений.
    2.4. Построение концептуальной модели (ER-диаграмма).

3. **Логическая структура БД.**
    Нормализация отношений и определение ключей.

4. **Физическая структура базы данных.**
    Выбор типов данных в СУБД PostgreSQL.

5. **Реализация проекта в среде конкретной СУБД.**
    5.1. Создание таблиц (`CREATE TABLE`).
    5.2. Реализация серверной логики (Триггеры для пересчета остатков).
    5.3. Создание пользовательских представлений (`VIEWS`).
    5.4. Назначение прав доступа.
    5.5. Разработка стратегии резервного копирования.

Руководитель работы __________________ <ins> И. В. Пунгин </ins>

Задание принял к исполнению _______________________________ <ins> Ломовицкий А.И. </ins>

***

## <a id="content">Содержание</a>

1. [Введение](#introduction)
    - [Актуальность темы](#relevance)
    - [Цель работы](#target)
    - [Задачи работы](#tasks)
2. [Основная часть](#main)
    - [Анализ предметной области. Постановка задачи](#analysis)
    - [Инфологическая (концептуальная) модель базы данных](#infological_model)
    - [Логическая структура БД](#logical_structure)
    - [Физическая структура базы данных](#physical_structure)
    - [Реализация проекта в среде конкретной СУБД](#project_realization)
3. [Заключение](#conclusion)
4. [Список использованных информационных источников](#literature)
5. [Приложения](#applications)

***

## <a id="introduction">Введение</a>

### <a id="relevance">Актуальность темы</a>
В современных экономических условиях эффективность работы предприятия автобизнеса напрямую зависит от качества управления складскими запасами. Специфика данной сферы заключается в огромной номенклатуре: даже небольшой магазин может иметь на остатках тысячи позиций — от мелких предохранителей до кузовных деталей и масел с ограниченным сроком годности.

Ручной учет или использование простых таблиц Excel приводит к серьезным проблемам:
*   **Потеря времени:** Кладовщики тратят до 30% времени на поиск детали, если не внедрено адресное хранение (конкретная ячейка).
*   **Пересортица:** Расхождение фактического наличия с данными в компьютере.
*   **Финансовые потери:** "Замораживание" денег в неликвидном товаре и списание просроченной автохимии, которую вовремя не реализовали.

Разработка реляционной базы данных, автоматизирующей процессы приемки, отгрузки и контроля сроков годности, является критически важной задачей для минимизации издержек и повышения скорости обслуживания.

### <a id="target">Цель работы</a>
Проектирование и реализация базы данных для автоматизации складского учета автотоваров, обеспечивающей целостность данных, поддержку адресного хранения и автоматический пересчет остатков с использованием триггеров.

### <a id="tasks">Задачи работы</a>
Для достижения поставленной цели необходимо решить следующие задачи:
1.  **Проанализировать предметную область:** изучить процессы движения товаров на складе (приход, расход, списание).
2.  **Спроектировать структуру БД:** выделить сущности, атрибуты и связи, построить инфологическую модель.
3.  **Обосновать выбор СУБД:** сравнить доступные решения и аргументировать выбор PostgreSQL.
4.  **Реализовать базу данных:** написать SQL-скрипты создания таблиц и ограничений.
5.  **Автоматизировать бизнес-логику:** разработать триггеры для контроля остатков.
6.  **Создать интерфейс данных:** разработать представления (Views) для генерации отчетов.

***

## <a id="main">Основная часть</a>

#### <a id="analysis">Анализ предметной области. Постановка задачи</a>

1.  **Описание предметной области и функции решаемых задач**
    *   **Предметная область:** Складское хозяйство магазина автозапчастей. Система направлена на учет материальных ценностей.
    *   **Функции:**
        *   **Адресное хранение:** Фиксация точного места расположения товара (Зона-Ряд-Полка).
        *   **Партионный учет:** Регистрация каждой операции (приходной или расходной накладной).
        *   **Контроль сроков:** Отслеживание товаров с истекающим сроком годности (масла, химия).
        *   **Единый реестр контрагентов:** Учет поставщиков и оптовых клиентов в единой базе.

2.  **Перечень входных данных.**
    *   **Справочники:** Категории товаров (Двигатель, Подвеска...), Производители (Bosch, Denso...).
    *   **Товарная номенклатура:** Артикул, наименование, базовая цена.
    *   **Первичные документы:** Приходные накладные от поставщиков, накладные на отгрузку, акты списания.

3.  **Перечень выходных данных.**
    *   **Отчет об остатках:** Актуальное количество товаров в разрезе ячеек хранения.
    *   **Монитор сроков годности:** Список товаров, истекающих в ближайшие 30 дней.
    *   **История движения:** Детальный отчет о том, когда и кому был отгружен конкретный товар.

4.  **Ограничения предметной области.**
    *   **Отрицательные остатки:** Нельзя отгрузить товара больше, чем числится на складе.
    *   **Целостность:** Нельзя удалить категорию товара, если к ней привязаны существующие товары.
    *   **Уникальность:** В рамках одного производителя артикул должен быть уникален.

5.  **Взаимодействие с другими программами.**
    База данных проектируется как backend-составляющая. Планируется взаимодействие с клиентским приложением на языке Python (через драйвер `psycopg2`) для работы кладовщика и интеграция с системой бухгалтерского учета.

#### <a id="infological_model">Инфологическая (концептуальная) модель базы данных</a>

Концептуальная модель описывает структуру данных без привязки к конкретной СУБД.

1.  **Выделение информационных объектов:**
    *   **Товары (Products):** Центральный объект учета.
    *   **Категории (Categories) и Производители (Manufacturers):** Справочники.
    *   **Контрагенты (Contractors):** Поставщики и получатели.
    *   **Движения (Stock Movements):** Документы (шапки накладных).
    *   **Позиции движения (Movement Items):** Состав накладных.

2.  **Определение атрибутов объектов:**
    *   **Товар:** Артикул, Название, Место хранения (код ячейки), Цена, Остаток, Срок годности.
    *   **Контрагент:** Название, Тип (Поставщик/Клиент), Телефон.
    *   **Движение:** Дата, Тип операции (Приход/Расход/Списание), Ссылка на контрагента.

3.  **Определение отношений:**
    *   **Категория — Товар (1:M):** Одна категория содержит много товаров.
    *   **Контрагент — Движение (1:M):** Один контрагент может фигурировать в множестве накладных.
    *   **Движение — Позиция (1:M):** Одна накладная содержит много строк с товарами.
    *   **Товар — Позиция (1:M):** Один товар может встречаться в разных накладных.

4.  **Построение концептуальной модели.**
    *(Здесь предполагается вставка скриншота ER-диаграммы, связывающей таблицы Products, Categories, Stock_Movements и т.д.)*

#### <a id="logical_structure">Логическая структура базы данных</a>

В данной структуре определены следующие таблицы, приведенные к 3-й нормальной форме:

1.  **Таблица "categories" (Категории)**
    *   `category_id` (PK) - Идентификатор.
    *   `name` - Название категории.

2.  **Таблица "manufacturers" (Производители)**
    *   `manufacturer_id` (PK).
    *   `name` - Бренд.
    *   `country` - Страна.

3.  **Таблица "products" (Товары)**
    *   `product_id` (PK).
    *   `part_number` - Артикул (основной поисковый атрибут).
    *   `name` - Наименование.
    *   `location_code` - Код ячейки склада (например, "A-12-05").
    *   `stock_quantity` - Текущий остаток.
    *   `price` - Учетная цена.
    *   `expiration_date` - Срок годности (может быть NULL).
    *   `category_id`, `manufacturer_id` (FK).

4.  **Таблица "contractors" (Контрагенты)**
    *   `contractor_id` (PK).
    *   `name` - Название компании.
    *   `type` - Тип ('supplier' или 'client').

5.  **Таблица "stock_movements" (Журнал операций)**
    *   `movement_id` (PK).
    *   `created_at` - Дата и время.
    *   `operation_type` - Тип ('in', 'out', 'writeoff').
    *   `contractor_id` (FK).

6.  **Таблица "movement_items" (Позиции)**
    *   `item_id` (PK).
    *   `movement_id` (FK) - Ссылка на документ.
    *   `product_id` (FK) - Ссылка на товар.
    *   `quantity` - Количество.

#### <a id="physical_structure">Физическая структура базы данных</a>

Для реализации выбрана СУБД PostgreSQL. Выбор типов данных обусловлен требованиями точности и оптимизации:

*   **SERIAL:** Для автоматической генерации первичных ключей.
*   **NUMERIC(10, 2):** Для цен. Использование `FLOAT` недопустимо в финансовых расчетах из-за ошибок округления.
*   **VARCHAR(n):** Для текстовых полей.
*   **TIMESTAMP:** Для точной фиксации времени операции.
*   **DATE:** Для сроков годности.

**Ограничения (Constraints):**
*   `CHECK (stock_quantity >= 0)`: Гарантирует отсутствие отрицательных остатков.
*   `CHECK (price >= 0)`: Цена не может быть отрицательной.
*   `CHECK (operation_type IN (...))`: Защита от некорректных типов операций.

#### <a id="project_realization">Реализация проекта в среде конкретной СУБД</a>

**5.1. Создание таблиц (SQL DDL)**

```sql
-- Создание таблицы товаров с учетом адресного хранения
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    part_number VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    location_code VARCHAR(20) DEFAULT 'RECEPTION', 
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    expiration_date DATE,
    category_id INTEGER REFERENCES categories(category_id),
    manufacturer_id INTEGER REFERENCES manufacturers(manufacturer_id)
);
-- (Остальные таблицы создаются аналогичным образом)
```

**5.2. Реализация автоматизации (Триггеры)**

Для автоматического изменения остатков при добавлении накладной была написана хранимая функция на языке PL/pgSQL.

Логика работы:
1. Если операция 'in' (Приход) -> Увеличить `stock_quantity`.
2. Если операция 'out' или 'writeoff' (Расход/Списание) -> Проверить наличие товара и уменьшить `stock_quantity`.

```sql
CREATE OR REPLACE FUNCTION update_stock_on_movement() RETURNS TRIGGER AS $$
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
```

**5.3. Создание представлений (Views)**

Для удобства работы и формирования отчетов были созданы виртуальные таблицы:

*   `v_warehouse_stock`: Отображает остатки с понятными названиями брендов и суммой в деньгах.
*   `v_expiring_goods` (Монитор просрочки): Фильтрует товары, срок годности которых истекает через 30 дней или меньше.

```sql
CREATE VIEW v_expiring_goods AS
SELECT name, location_code, expiration_date 
FROM products 
WHERE expiration_date <= (CURRENT_DATE + INTERVAL '30 days');
```

## <a id="conclusion">Заключение </a>

В ходе выполнения курсовой работы была успешно разработана база данных для автоматизации складского учета автотоваров.

**Основные достижения:**
1.  Спроектирована реляционная модель данных, учитывающая специфику автобизнеса (артикулы, бренды, адресное хранение).
2.  Реализована защита целостности данных: база данных не допускает появления отрицательных остатков и некорректных связей.
3.  Внедрена серверная логика (триггеры), которая полностью автоматизировала процесс пересчета количества товара. Это исключает ошибки оператора.
4.  Разработана система контроля сроков годности, позволяющая минимизировать убытки от списания просроченной продукции.

Разработанная БД готова к внедрению и интеграции с программным обеспечением высокого уровня.

## <a id="literature">Список использованных информационных источников</a>

1.  Дейт К. Дж. Введение в системы баз данных. – 8-е изд. – М.: Вильямс, 2016.
2.  Официальная документация PostgreSQL [Электронный ресурс]. – Режим доступа: https://www.postgresql.org/docs/
3.  Моргунов Е.П. PostgreSQL. Основы языка SQL. – СПб.: БХВ-Петербург, 2018.

## <a id="applications">Приложения</a>

*Приложение А. Полный листинг SQL-скрипта создания базы данных.*

```sql
-- ============================================================
-- ПРИЛОЖЕНИЕ А. Полный листинг SQL-скрипта создания БД
-- ============================================================

-- 1. ОЧИСТКА БД (Удаление старых таблиц, если они есть)
DROP VIEW IF EXISTS v_expiring_goods;
DROP VIEW IF EXISTS v_movement_history;
DROP VIEW IF EXISTS v_warehouse_stock;
DROP TABLE IF EXISTS movement_items CASCADE;
DROP TABLE IF EXISTS stock_movements CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS contractors CASCADE;
DROP TABLE IF EXISTS manufacturers CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- 2. СОЗДАНИЕ СПРАВОЧНИКОВ

-- Категории товаров (Масла, Фильтры, Шины и т.д.)
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Производители (Бренды)
CREATE TABLE manufacturers (
    manufacturer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(50)
);

-- Контрагенты (Единая таблица для Поставщиков и Клиентов)
CREATE TABLE contractors (
    contractor_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL, -- Название фирмы
    type VARCHAR(20) NOT NULL CHECK (type IN ('supplier', 'client')),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT
);

-- 3. СОЗДАНИЕ ОСНОВНЫХ ТАБЛИЦ

-- Товары (Номенклатура + Текущие остатки)
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    part_number VARCHAR(50) NOT NULL,       -- Артикул
    name VARCHAR(255) NOT NULL,             -- Название
    location_code VARCHAR(20) DEFAULT 'RECEPTION', -- Адрес ячейки (Зона-Ряд-Полка)
    
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    
    expiration_date DATE, -- Срок годности (для масел/химии)
    
    category_id INTEGER REFERENCES categories(category_id) ON DELETE SET NULL,
    manufacturer_id INTEGER REFERENCES manufacturers(manufacturer_id) ON DELETE SET NULL
);

-- Журнал движения (Шапка документа)
CREATE TABLE stock_movements (
    movement_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Типы операций: Приход, Расход, Списание
    operation_type VARCHAR(10) NOT NULL CHECK (operation_type IN ('in', 'out', 'writeoff')),
    contractor_id INTEGER REFERENCES contractors(contractor_id) ON DELETE SET NULL,
    comments TEXT
);

-- Позиции документа (Состав накладной)
CREATE TABLE movement_items (
    item_id SERIAL PRIMARY KEY,
    movement_id INTEGER REFERENCES stock_movements(movement_id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(product_id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price NUMERIC(10, 2) NOT NULL -- Цена в документе
);

-- 4. АВТОМАТИЗАЦИЯ (ТРИГГЕРЫ)

-- Функция пересчета остатков
CREATE OR REPLACE FUNCTION update_stock_on_movement()
RETURNS TRIGGER AS $$
DECLARE
    op_type VARCHAR(10);
BEGIN
    -- Получаем тип операции из шапки документа
    SELECT operation_type INTO op_type 
    FROM stock_movements 
    WHERE movement_id = NEW.movement_id;

    -- Логика:
    IF op_type = 'in' THEN
        -- ПРИХОД: Увеличиваем остаток
        UPDATE products 
        SET stock_quantity = stock_quantity + NEW.quantity
        WHERE product_id = NEW.product_id;
        
    ELSIF op_type IN ('out', 'writeoff') THEN
        -- РАСХОД или СПИСАНИЕ: Проверяем наличие и уменьшаем
        IF (SELECT stock_quantity FROM products WHERE product_id = NEW.product_id) < NEW.quantity THEN
            RAISE EXCEPTION 'Ошибка: Недостаточно товара на складе!';
        END IF;

        UPDATE products 
        SET stock_quantity = stock_quantity - NEW.quantity
        WHERE product_id = NEW.product_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера
CREATE TRIGGER trg_update_stock
AFTER INSERT ON movement_items
FOR EACH ROW
EXECUTE FUNCTION update_stock_on_movement();

-- 5. ПРЕДСТАВЛЕНИЯ (VIEWS)

-- View 1: Складская справка (Витрина остатков)
CREATE OR REPLACE VIEW v_warehouse_stock AS
SELECT 
    p.part_number AS Артикул,
    p.name AS Товар,
    m.name AS Бренд,
    p.location_code AS Ячейка,
    p.stock_quantity AS Остаток,
    p.price AS Учетная_Цена,
    (p.stock_quantity * p.price) AS Сумма_Остатка
FROM products p
LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id;

-- View 2: Монитор сроков годности (Товары, истекающие в течение 30 дней)
CREATE OR REPLACE VIEW v_expiring_goods AS
SELECT 
    p.part_number,
    p.name,
    p.location_code,
    p.stock_quantity,
    p.expiration_date,
    CASE 
        WHEN p.expiration_date < CURRENT_DATE THEN 'ПРОСРОЧЕНО'
        ELSE 'Истекает скоро'
    END AS Статус
FROM products p
WHERE 
    p.expiration_date IS NOT NULL 
    AND p.stock_quantity > 0
    AND p.expiration_date <= (CURRENT_DATE + INTERVAL '30 days');

-- View 3: История операций
CREATE OR REPLACE VIEW v_movement_history AS
SELECT 
    m.created_at AS Дата,
    m.operation_type AS Тип,
    c.name AS Контрагент,
    p.name AS Товар,
    mi.quantity AS Кол_во
FROM movement_items mi
JOIN stock_movements m ON mi.movement_id = m.movement_id
JOIN products p ON mi.product_id = p.product_id
LEFT JOIN contractors c ON m.contractor_id = c.contractor_id
ORDER BY m.created_at DESC;

-- 6. ТЕСТОВЫЕ ДАННЫЕ (Заполнение)

INSERT INTO categories (name) VALUES ('Масла'), ('Фильтры');
INSERT INTO manufacturers (name, country) VALUES ('Shell', 'EU'), ('Mann', 'DE');
INSERT INTO contractors (name, type) VALUES ('ООО Поставщик', 'supplier'), ('Магазин №1', 'client');

-- Добавляем товары (остаток 0)
INSERT INTO products (part_number, name, location_code, price, category_id, manufacturer_id, expiration_date) 
VALUES 
('HELIX-5W40', 'Масло Shell Helix Ultra 4л', 'A-01-01', 4000.00, 1, 1, CURRENT_DATE + INTERVAL '20 days'),
('W914/2', 'Фильтр масляный', 'B-02-05', 500.00, 2, 2, NULL);

-- Приход (Триггер сработает и сделает остаток 10)
INSERT INTO stock_movements (operation_type, contractor_id) VALUES ('in', 1);
INSERT INTO movement_items (movement_id, product_id, quantity, price) VALUES (1, 1, 10, 3500.00);

-- Расход (Триггер сработает и сделает остаток 8)
INSERT INTO stock_movements (operation_type, contractor_id) VALUES ('out', 2);
INSERT INTO movement_items (movement_id, product_id, quantity, price) VALUES (2, 1, 2, 4500.00);
```
