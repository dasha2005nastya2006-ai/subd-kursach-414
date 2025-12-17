# Пояснительная записка к проекту БД «Склад автотоваров»

---

# 1. Введение и постановка задачи

### 1.1. Актуальность темы и описание предметной области
Темой моей курсовой работы является разработка базы данных для автоматизации складского учета в магазине автозапчастей.
Специфика автобизнеса заключается в огромной номенклатуре товаров. Даже небольшой магазин может иметь на остатках тысячи позиций: от мелких предохранителей и уплотнительных колец до крупных кузовных деталей и агрегатов.

В ходе анализа работы магазина я выяснил, что отсутствие грамотной структуры хранения данных приводит к хаосу:
1.  **Потеря времени:** Кладовщик тратит до 30% рабочего времени на поиск детали, так как она лежит «где-то на полке», а не по конкретному адресу.
2.  **Пересортица:** Часто возникают ситуации, когда по компьютеру деталь числится (остаток > 0), а фактически её нет (или она бракована).
3.  **Замораживание средств:** Без точного учета сложно отследить неликвидный товар, который лежит годами, и вовремя дозаказать ходовые позиции ("Точка перезаказа").

Для решения этих проблем Excel или бумажных журналов недостаточно. Требуется реляционная база данных, обеспечивающая целостность данных, высокую скорость поиска и защиту от ошибок оператора. В качестве инструмента разработки я выбрал **СУБД PostgreSQL**, так как она является стандартом в индустрии, поддерживает сложные типы данных и обладает мощным механизмом процедурных расширений (PL/pgSQL).

### 1.2. Постановка задачи
Передо мной была поставлена цель: спроектировать и реализовать структуру базы данных, которая станет цифровым ядром склада.

Я сформулировал основные функциональные требования (задачи), которые должна решать моя БД:
1.  **Организация адресного хранения:** Система должна знать не просто «сколько» товара есть, но и «где конкретно» он лежит (Код ячейки: Зона-Ряд-Полка).
2.  **Строгий партионный учет (Приход/Расход):** Товар не появляется из воздуха. Любое изменение остатка должно быть подтверждено документом (накладной). Я отказался от простого редактирования поля `quantity` вручную в пользу транзакционной модели.
3.  **Унификация контрагентов:** Склад взаимодействует как с внешними поставщиками (приемка), так и с торговым залом магазина (внутренняя отгрузка). Необходимо хранить всех участников цепочки в едином реестре.
4.  **Контроль отрицательных остатков:** База данных должна на физическом уровне (Constraints) запрещать отгрузку товара, которого нет в наличии.

### 1.3. Описание разработанной структуры данных
Для реализации поставленных задач я спроектировал схему данных, включающую следующие ключевые компоненты:

**А. Справочники (Нормализация данных)**
Чтобы избежать дублирования информации (например, многократного написания бренда "Toyota" с возможными опечатками), я выделил статические данные в отдельные таблицы:
*   `categories` (Категории) — для группировки товаров (Масла, Фильтры, Ходовая).
*   `manufacturers` (Производители) — справочник брендов.
*   `contractors` (Контрагенты) — единая таблица для поставщиков и получателей.

**Б. Товарная номенклатура (`products`)**
Это центральная таблица. В отличие от простого списка, я добавил в неё атрибут `location_code` (адрес ячейки). Это решает проблему долгого поиска товара. Также я предусмотрел поле `part_number` (артикул), так как в автомагазине поиск чаще всего идет именно по нему, а не по названию.

**В. Учет движения (`stock_movements` и `movement_items`)**
Я принял архитектурное решение разделить процесс учета на две сущности:
*   **Шапка документа (`stock_movements`):** Фиксирует «кто», «когда» и «какую операцию» совершил (Приход от поставщика или Отгрузка в зал).
*   **Табличная часть (`movement_items`):** Хранит перечень конкретных товаров в этом документе.

Такая структура ("Один ко многим") позволяет в одном документе приходовать сразу сотню разных позиций, что соответствует реальной накладной от поставщика.

**Г. Автоматизация (Триггеры)**
Я посчитал, что пересчет остатков вручную ненадежен. Поэтому я реализовал триггерную логику: при добавлении записи в таблицу движения (`movement_items`), база данных сама пересчитывает поле `stock_quantity` в таблице товаров. Это гарантирует, что цифра остатка всегда актуальна.

### 1.4. Ожидаемый результат
В результате разработки я планирую получить полностью функциональную базу данных, готовую к интеграции с программным обеспечением (на Python). Она обеспечит прозрачность складских процессов, минимизирует ошибки человеческого фактора и позволит мгновенно получать отчеты о состоянии склада.

---

### 2. Проектирование схемы данных (Логическая модель)

Перед написанием кода я провел инфологическое проектирование. Основываясь на требованиях из п. 1.2, я выделил ключевые сущности и определил связи между ними.

Мной были приняты следующие архитектурные решения:

1.  **Сущность «Товары» (`products`):**
    Я решил, что хранить только Название и Цену недостаточно. Я добавил поле `part_number` (Артикул), так как это основной идентификатор в автобизнесе. Также я ввел поле `location_code` для реализации адресного хранения.

2.  **Сущность «Контрагенты» (`contractors`):**
    Вместо создания двух разных таблиц («Поставщики» и «Клиенты»), я использовал паттерн обобщения. Я создал одну таблицу `contractors` с полем `type` (тип контрагента). Это упрощает архитектуру, так как и те, и другие имеют одинаковые атрибуты (Название, Телефон, Адрес).

3.  **Сущность «Движение товара» (Журнал операций):**
    Я отказался от прямой связи «Клиент — Товар». Вместо этого я внедрил промежуточную сущность — Документ (`stock_movements`). Это позволяет одним документом оформлять перемещение десятков разных товаров, что соответствует реальной накладной.

База данных была спроектирована в **3-й нормальной форме (3NF)**: все неключевые атрибуты зависят только от первичного ключа, повторяющиеся данные (категории, бренды) вынесены в справочники.

---

### 3. Реализация структуры БД (SQL-код)

На основе спроектированной схемы я написал SQL-скрипт инициализации базы данных.

```sql
-- Очистка (на случай перезапуска скрипта при отладке)
DROP TABLE IF EXISTS movement_items CASCADE;
DROP TABLE IF EXISTS stock_movements CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS contractors CASCADE;
DROP TABLE IF EXISTS manufacturers CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- 1. Справочник категорий (например: Двигатель, Кузов, Электрика)
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Справочник производителей (например: Bosch, VAG, Toyota)
CREATE TABLE manufacturers (
    manufacturer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(50)
);

-- 3. Основная таблица товаров (ОБНОВЛЕННАЯ)
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    part_number VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    
    location_code VARCHAR(20) DEFAULT 'RECEPTION', 
    
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    
    -- НОВОЕ ПОЛЕ: Срок годности
    -- Делаем его необязательным (NULL), так как у железных запчастей срока нет
    expiration_date DATE,
    
    category_id INTEGER REFERENCES categories(category_id) ON DELETE SET NULL,
    manufacturer_id INTEGER REFERENCES manufacturers(manufacturer_id) ON DELETE SET NULL,
    description TEXT
);

-- ... Таблица contractors без изменений ...

-- 5. Журнал складских операций (ОБНОВЛЕННЫЙ)
CREATE TABLE stock_movements (
    movement_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- НОВЫЙ ТИП: 'writeoff' (Списание просрочки/брака)
    operation_type VARCHAR(10) NOT NULL CHECK (operation_type IN ('in', 'out', 'writeoff')),
    
    contractor_id INTEGER REFERENCES contractors(contractor_id) ON DELETE SET NULL,
    comments TEXT
);

-- 4. Таблица Контрагентов (Единый реестр)
CREATE TABLE contractors (
    contractor_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,  -- Название фирмы или ИП
    type VARCHAR(20) NOT NULL CHECK (type IN ('supplier', 'client')), -- Флаг: Поставщик или Клиент
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT
);

-- 5. Журнал складских операций (Шапка накладной)
CREATE TABLE stock_movements (
    movement_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Тип операции: 'in' (Приход на склад), 'out' (Расход/Отгрузка)
    operation_type VARCHAR(10) NOT NULL CHECK (operation_type IN ('in', 'out')),
    
    contractor_id INTEGER REFERENCES contractors(contractor_id) ON DELETE SET NULL,
    comments TEXT
);

-- 6. Состав накладной (Детализация: какие товары и сколько)
CREATE TABLE movement_items (
    item_id SERIAL PRIMARY KEY,
    movement_id INTEGER REFERENCES stock_movements(movement_id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(product_id) ON DELETE RESTRICT,
    
    quantity INTEGER NOT NULL CHECK (quantity > 0), -- Кол-во в документе
    price NUMERIC(10, 2) NOT NULL -- Цена в документе (может отличаться от учетной)
);
```

---

### 4. Автоматизация бизнес-логики (Триггеры)

Одной из главных проблем ручного учета является «человеческий фактор»: оператор может забыть обновить остаток товара после оформления накладной.
Чтобы исключить это, я перенес логику пересчета остатков на сторону сервера БД, используя язык **PL/pgSQL**.

Мной был разработан триггер, который срабатывает автоматически при добавлении записи в таблицу позиций (`movement_items`).

```sql
-- Функция для автоматического изменения остатков
CREATE OR REPLACE FUNCTION update_stock_on_movement()
RETURNS TRIGGER AS $$
DECLARE
    op_type VARCHAR(10);
BEGIN
    SELECT operation_type INTO op_type 
    FROM stock_movements 
    WHERE movement_id = NEW.movement_id;

    -- Приход
    IF op_type = 'in' THEN
        UPDATE products 
        SET stock_quantity = stock_quantity + NEW.quantity
        WHERE product_id = NEW.product_id;
        
    -- Расход ИЛИ Списание (Логика одинаковая - товар уходит со склада)
    ELSIF op_type IN ('out', 'writeoff') THEN
        
        -- Проверка остатка
        IF (SELECT stock_quantity FROM products WHERE product_id = NEW.product_id) < NEW.quantity THEN
            RAISE EXCEPTION 'Ошибка: Недостаточно товара для отгрузки или списания!';
        END IF;

        UPDATE products 
        SET stock_quantity = stock_quantity - NEW.quantity
        WHERE product_id = NEW.product_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Привязка функции к событию INSERT
CREATE TRIGGER trg_update_stock
AFTER INSERT ON movement_items
FOR EACH ROW
EXECUTE FUNCTION update_stock_on_movement();
```

---

### 5. Разработка пользовательских представлений (Views)

Для упрощения разработки будущего программного обеспечения (на Python) я создал слой абстракции в виде Представлений. Это позволяет получать сложные отчеты простым `SELECT`-запросом.

```sql
-- 1. Представление "Складская справка"
-- Показывает понятные названия брендов и рассчитывает сумму остатков в деньгах
CREATE OR REPLACE VIEW v_warehouse_stock AS
SELECT 
    p.part_number AS Артикул,
    p.name AS Товар,
    m.name AS Бренд,
    p.location_code AS Ячейка,
    p.stock_quantity AS Остаток,
    p.price AS Учетная_Цена,
    (p.stock_quantity * p.price) AS Сумма_Остатка -- Вычисляемое поле
FROM products p
LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id;

-- 2. Представление "История движения товаров"
-- Собирает данные из трех таблиц для полного отчета о том, кто, когда и что купил/продал
CREATE OR REPLACE VIEW v_movement_history AS
SELECT 
    m.created_at AS Дата,
    CASE 
        WHEN m.operation_type = 'in' THEN 'Приход'
        WHEN m.operation_type = 'out' THEN 'Расход' 
    END AS Операция,
    c.name AS Контрагент,
    p.name AS Товар,
    mi.quantity AS Кол_во,
    mi.price AS Цена_операции
FROM movement_items mi
JOIN stock_movements m ON mi.movement_id = m.movement_id
JOIN products p ON mi.product_id = p.product_id
JOIN contractors c ON m.contractor_id = c.contractor_id
ORDER BY m.created_at DESC;

-- 3. НОВОЕ ПРЕДСТАВЛЕНИЕ: Монитор сроков годности
-- Показывает товары, которые УЖЕ просрочены или истекут в ближайшие 30 дней
CREATE OR REPLACE VIEW v_expiring_goods AS
SELECT 
    p.product_id,
    p.part_number,
    p.name,
    p.location_code,
    p.stock_quantity,
    p.expiration_date,
    -- Вычисляем статус:
    CASE 
        WHEN p.expiration_date < CURRENT_DATE THEN 'ПРОСРОЧЕНО'
        WHEN p.expiration_date <= (CURRENT_DATE + INTERVAL '30 days') THEN 'Истекает скоро'
        ELSE 'Норма'
    END AS статус_годности,
    -- Сколько дней осталось (отрицательное число = просрочка)
    (p.expiration_date - CURRENT_DATE) AS дней_осталось
FROM products p
WHERE 
    p.expiration_date IS NOT NULL  -- Ищем только товары со сроком годности
    AND p.stock_quantity > 0       -- И только те, что есть на остатке
    AND p.expiration_date <= (CURRENT_DATE + INTERVAL '30 days') -- Фильтр: 30 дней или меньше
ORDER BY p.expiration_date ASC;
```

---

### 6. Тестирование работоспособности

Для проверки корректности спроектированной базы данных я провел серию тестов, имитирующих реальную работу склада.

```sql
-- 1. Наполнение справочников
INSERT INTO categories (name) VALUES ('Масла'), ('Ходовая');
INSERT INTO manufacturers (name) VALUES ('Shell'), ('Kayaba');
INSERT INTO contractors (name, type) VALUES ('ООО Опт-Снаб', 'supplier'), ('Магазин на Ленина', 'client');

-- 2. Создание карточки товара (Изначально остаток = 0)
INSERT INTO products (part_number, name, location_code, price, category_id, manufacturer_id)
VALUES ('5W40-4L', 'Масло Shell Helix Ultra 4л', 'Z-01-05', 4000.00, 1, 1);

-- 3. Тест ПРИХОДА товара
-- Создаем накладную на приход от поставщика
INSERT INTO stock_movements (operation_type, contractor_id) VALUES ('in', 1); -- id накладной = 1
-- Добавляем 10 канистр
INSERT INTO movement_items (movement_id, product_id, quantity, price) VALUES (1, 1, 10, 3800.00);

-- *Проверка:* SELECT stock_quantity FROM products; -> Результат: 10. Триггер сработал верно.

-- 4. Тест РАСХОДА (Отгрузка)
-- Создаем накладную на отгрузку клиенту
INSERT INTO stock_movements (operation_type, contractor_id) VALUES ('out', 2); -- id накладной = 2
-- Отгружаем 2 канистры
INSERT INTO movement_items (movement_id, product_id, quantity, price) VALUES (2, 1, 2, 4500.00);

-- *Проверка:* SELECT stock_quantity FROM products; -> Результат: 8. Остаток уменьшился.

-- 1. Добавляем масло, которое "протухает" завтра
INSERT INTO products (part_number, name, stock_quantity, price, expiration_date) 
VALUES ('OIL-OLD', 'Масло Старое', 5, 1000.00, CURRENT_DATE + INTERVAL '1 day');

-- 2. Смотрим отчет (Там должно появиться это масло)
SELECT * FROM v_expiring_goods;

-- 3. Списываем его (Утилизация)
INSERT INTO stock_movements (operation_type, comments) VALUES ('writeoff', 'Списание по сроку годности');
INSERT INTO movement_items (movement_id, product_id, quantity, price) VALUES 
((SELECT MAX(movement_id) FROM stock_movements), (SELECT product_id FROM products WHERE part_number = 'OIL-OLD'), 5, 0);

-- 4. Товар ушел в ноль
SELECT stock_quantity FROM products WHERE part_number = 'OIL-OLD';
```

---

### 7. Заключение

В ходе выполнения курсового проекта я разработал полноценную базу данных для склада автотоваров.

**Мной были изучены и применены на практике:**
1.  **Принципы нормализации:** Приведение схемы к 3NF позволило исключить избыточность данных.
2.  **Ссылочная целостность:** Использование внешних ключей (`FOREIGN KEY`) защищает базу от появления «сиротских» записей (например, товара без производителя).
3.  **Серверная логика:** Написание триггеров на `PL/pgSQL` позволило автоматизировать критически важный процесс пересчета складских остатков, снизив риск ошибок.
4.  **Представления:** Создание `Views` подготовило удобный интерфейс для будущей интеграции с программным обеспечением на языке Python.

Разработанная архитектура является масштабируемой: в будущем она позволяет легко добавить функционал инвентаризации, резервирования товаров и работу с несколькими складами одновременно.
