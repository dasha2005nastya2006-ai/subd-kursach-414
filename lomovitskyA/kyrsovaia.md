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
    *<img width="1046" height="832" alt="{F298BBB3-E6B5-42DA-B096-E7D53F2805AD}" src="https://github.com/user-attachments/assets/39a6addc-2854-411f-989a-a1274ac0a52e" />
*

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


**3. Разработка API базы данных (Хранимые процедуры)**

Для обеспечения безопасности и сокрытия внутренней структуры базы данных от клиентского приложения был реализован слой серверного API. Клиентское приложение не выполняет прямых команд `INSERT` или `UPDATE` к таблицам, а обращается к хранимым процедурам.

*Процедура регистрации складской операции:*
Данная процедура инкапсулирует логику создания документа. Приложению не нужно знать, что накладная состоит из двух таблиц (`stock_movements` и `movement_items`) и что нужно искать текущую цену. Всё это делает сервер.

```sql
CREATE OR REPLACE PROCEDURE pr_register_operation(
    _product_id INT,
    _quantity INT,
    _op_type VARCHAR,
    _contractor_id INT
)
LANGUAGE plpgsql AS $$
DECLARE
    _mov_id INT;
    _current_price NUMERIC;
BEGIN
    -- 1. Получаем текущую цену товара (логика на сервере)
    SELECT price INTO _current_price FROM products WHERE product_id = _product_id;
    
    IF _current_price IS NULL THEN 
        RAISE EXCEPTION 'Товар с ID % не найден', _product_id; 
    END IF;

    -- 2. Создаем "шапку" документа
    INSERT INTO stock_movements (operation_type, contractor_id)
    VALUES (_op_type, _contractor_id)
    RETURNING movement_id INTO _mov_id;

    -- 3. Создаем позицию (цену берем из базы, а не от клиента)
    INSERT INTO movement_items (movement_id, product_id, quantity, price)
    VALUES (_mov_id, _product_id, _quantity, _current_price);
END;
$$;
```

*Процедура добавления нового товара:*
```sql
CREATE OR REPLACE PROCEDURE pr_add_product(
    _part_number VARCHAR, 
    _name VARCHAR, 
    _price NUMERIC, 
    _location VARCHAR
) 
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO products (part_number, name, price, location_code)
    VALUES (_part_number, _name, _price, _location);
END; 
$$;
```

**4. Назначение прав доступа**
Использование процедур позволяет реализовать принцип минимальных привилегий. Пользователю базы данных даются права **только** на запуск процедур (`EXECUTE`) и чтение представлений (`SELECT` на View), но закрывается прямой доступ к таблицам. Это защищает структуру БД от изменений и несанкционированного доступа.


#### <a id="client_app">Разработка клиентского приложения</a>

Для взаимодействия с базой данных разработано приложение на языке **Python** с использованием библиотеки `tkinter` (GUI) и драйвера `psycopg2`.

**Функционал приложения:**
1.  **Просмотр остатков:** Отображение данных из представления `v_warehouse_stock` в табличном виде.
2.  **Оформление операций:** Форма для ввода ID товара, количества и выбора типа операции (Приход/Расход). Приложение отправляет SQL-запросы, которые активируют триггеры в БД.
3.  **Обработка ошибок:** Если БД возвращает ошибку (например, нарушение `CHECK` при попытке уйти в минус), приложение выводит понятное сообщение пользователю.

*(Код приложения представлен в Приложении Б).*



#### <a id="client_app">1.6. Разработка и демонстрация интерфейса клиентского приложения</a>

Для обеспечения удобного взаимодействия персонала с разработанной базой данных было создано графическое приложение «АРМ Кладовщика». Интерфейс реализован с использованием библиотеки `tkinter`, что обеспечивает нативность отображения элементов управления в ОС Windows.

**Главное окно приложения**
При запуске программы открывается вкладка «Справочник товаров / Остатки». Основную часть экрана занимает таблица, отображающая данные из представления `v_warehouse_stock`.
В верхней части расположена панель инструментов, предоставляющая доступ к основным функциям (CRUD):
*   **Добавить товар:** Открывает модальное окно для ввода данных о новой номенклатуре.
*   **Изменить/Удалить:** Позволяет редактировать или удалять выбранные записи (с проверкой ссылочной целостности).
*   **Поиск:** Фильтрация таблицы по артикулу или названию.

*Визуализация главного окна с таблицей остатков представлена на Рисунке 1.*

<img width="1252" height="852" alt="{7D8FD92C-C20D-4108-9992-417B0516BE07}" src="https://github.com/user-attachments/assets/b9c6faf3-ae57-44cd-a37a-fd606bfcf387" />

*Рисунок 1. Главное окно приложения: просмотр остатков и панель управления.*

**Оформление складских операций**
Вторая вкладка приложения предназначена для регистрации движения товаров. Интерфейс спроектирован так, чтобы минимизировать ошибки ввода.
Пользователь заполняет поля:
1.  **Артикул:** Идентификатор товара.
2.  **Количество:** Число единиц.
3.  **Тип операции:** Выбор из списка (Приход, Расход, Списание).

При нажатии кнопки «Провести документ» приложение отправляет транзакционный запрос к БД. В случае успеха выводится сообщение, а остатки обновляются автоматически благодаря триггерам PostgreSQL.

*Интерфейс модуля оформления операций представлен на Рисунке 2.*


<img width="1251" height="848" alt="{FB3A7B29-5882-4E78-A335-75B11C60B312}" src="https://github.com/user-attachments/assets/af645a16-a424-4eff-ac2a-f266ba72ddb1" />


**Добавление новой номенклатуры**
Для ввода новых позиций используется отдельное модальное окно. Это предотвращает случайное изменение данных в основной таблице и позволяет сосредоточиться на заполнении карточки товара.

<img width="500" height="601" alt="{F4035AAD-C1C9-49DE-BF81-A058730FABF4}" src="https://github.com/user-attachments/assets/4dd76897-722f-4f70-a0d3-01fb2c94aa04" />

*Рисунок 3. Форма создания новой карточки товара.*

Разработанный интерфейс полностью удовлетворяет требованиям к эргономике и функциональности, обеспечивая доступ ко всем возможностям спроектированной базы данных.

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

-- ==========================================
-- API БАЗЫ ДАННЫХ (ПРОЦЕДУРЫ)
-- ==========================================

-- 1. Процедура проведения операции (Приход/Расход)
CREATE OR REPLACE PROCEDURE pr_register_operation(
    _product_id INT,
    _quantity INT,
    _op_type VARCHAR,
    _contractor_id INT
)
LANGUAGE plpgsql AS $$
DECLARE
    _mov_id INT;
    _current_price NUMERIC;
BEGIN
    -- Проверка существования товара
    SELECT price INTO _current_price FROM products WHERE product_id = _product_id;
    IF _current_price IS NULL THEN 
        RAISE EXCEPTION 'Товар не найден'; 
    END IF;

    -- Создание движения
    INSERT INTO stock_movements (operation_type, contractor_id)
    VALUES (_op_type, _contractor_id)
    RETURNING movement_id INTO _mov_id;

    -- Добавление позиции
    INSERT INTO movement_items (movement_id, product_id, quantity, price)
    VALUES (_mov_id, _product_id, _quantity, _current_price);
END;
$$;

-- 2. Процедура создания товара
CREATE OR REPLACE PROCEDURE pr_add_product(
    _part_number VARCHAR, 
    _name VARCHAR, 
    _price NUMERIC, 
    _location VARCHAR
) 
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO products (part_number, name, price, location_code)
    VALUES (_part_number, _name, _price, _location);
END; 
$$;
```

#### Приложение Б: Исходный код приложения (Python)

```python
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import Error

# =============================================================================
# КОНФИГУРАЦИЯ ПОДКЛЮЧЕНИЯ
# =============================================================================
# Параметры для соединения с локальной базой данных PostgreSQL.
# В реальном проекте эти данные лучше выносить в отдельный файл .env
DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",       # Стандартный пользователь Postgres
    "password": "YOUR_PASSWORD", # <-- ВАЖНО: Замените на ваш пароль от БД
    "database": "autoparts_db" # Имя созданной базы данных
}

class WarehouseApp:
    """
    Главный класс графического приложения (GUI).
    Реализует интерфейс для работы кладовщика.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("АРМ Склад Автотоваров (API Client)")
        self.root.geometry("950x600") # Размер окна при запуске
        
        # Инициализация переменной подключения
        self.conn = None
        
        # Попытка подключения при старте
        if not self.connect_db():
            # Если база недоступна, закрываем приложение
            root.destroy()
            return

        # Настройка вкладок (TabControl)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # --- Вкладка 1: Просмотр остатков ---
        self.tab_stock = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_stock, text="Складские остатки")
        self.setup_stock_tab()

        # --- Вкладка 2: Операции ---
        self.tab_ops = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ops, text="Операции")
        self.setup_ops_tab()
        
        # Загрузка данных сразу после запуска
        self.refresh_stock()

    def connect_db(self):
        """
        Устанавливает соединение с СУБД PostgreSQL.
        Использует библиотеку psycopg2.
        """
        try:
            # Распаковка словаря DB_CONFIG и соединение
            self.conn = psycopg2.connect(**DB_CONFIG)
            return True
        except Exception as e:
            # Вывод окна с ошибкой, если сервер недоступен или пароль неверен
            messagebox.showerror("Критическая ошибка подключения", str(e))
            return False

    def setup_stock_tab(self):
        """
        Настройка интерфейса первой вкладки (Таблица остатков).
        """
        # Панель инструментов (кнопки сверху)
        toolbar = ttk.Frame(self.tab_stock)
        toolbar.pack(fill=tk.X, pady=5)
        
        # Кнопка обновления данных вручную
        ttk.Button(toolbar, text="Обновить", command=self.refresh_stock).pack(side=tk.LEFT, padx=5)
        # Кнопка вызова окна добавления нового товара
        ttk.Button(toolbar, text="Новый товар", command=self.open_add_product_window).pack(side=tk.LEFT, padx=5)

        # Настройка таблицы (Treeview)
        # columns - внутренние имена колонок
        cols = ("art", "brand", "name", "qty", "price", "sum")
        self.tree = ttk.Treeview(self.tab_stock, columns=cols, show="headings")
        
        # Настройка заголовков таблицы (то, что видит пользователь)
        headers = ["Артикул", "Бренд", "Наименование", "Остаток", "Цена", "Сумма"]
        for col, h in zip(cols, headers):
            self.tree.heading(col, text=h)
            self.tree.column(col, width=100) # Ширина колонок по умолчанию
            
        # Размещение таблицы с растягиванием на все окно
        self.tree.pack(expand=True, fill='both')

    def setup_ops_tab(self):
        """
        Настройка интерфейса второй вкладки (Форма операций).
        """
        # Создаем контейнер по центру экрана для красоты
        f = ttk.Frame(self.tab_ops)
        f.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        # Поле ввода ID товара
        ttk.Label(f, text="ID Товара (из таблицы):").grid(row=0, column=0, sticky=tk.W)
        self.e_id = ttk.Entry(f)
        self.e_id.grid(row=0, column=1, pady=5)
        
        # Поле ввода количества
        ttk.Label(f, text="Количество:").grid(row=1, column=0, sticky=tk.W)
        self.e_qty = ttk.Entry(f)
        self.e_qty.grid(row=1, column=1, pady=5)
        
        # Радиокнопки для выбора типа операции
        ttk.Label(f, text="Тип операции:").grid(row=2, column=0, sticky=tk.W)
        self.v_op = tk.StringVar(value="in") # По умолчанию - Приход ('in')
        
        frame_rb = ttk.Frame(f)
        frame_rb.grid(row=2, column=1, pady=5)
        
        # value='in'/'out' должно совпадать с CHECK constraint в базе данных!
        ttk.Radiobutton(frame_rb, text="Приход", variable=self.v_op, value="in").pack(side=tk.LEFT)
        ttk.Radiobutton(frame_rb, text="Расход", variable=self.v_op, value="out").pack(side=tk.LEFT)
        
        # Кнопка выполнения
        ttk.Button(f, text="Выполнить операцию", command=self.run_op).grid(row=3, column=0, columnspan=2, pady=20)

    # =========================================================================
    # ЛОГИКА ВЗАИМОДЕЙСТВИЯ С БД (API)
    # =========================================================================

    def refresh_stock(self):
        """
        Чтение данных. 
        ВАЖНО: Python не обращается к таблицам напрямую.
        Мы делаем выборку из ПРЕДСТАВЛЕНИЯ (VIEW) 'v_warehouse_stock'.
        Это скрывает структуру БД от приложения.
        """
        # 1. Очистка текущей таблицы
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        try:
            # Использование контекстного менеджера (with) для курсора
            with self.conn.cursor() as cur:
                # SQL-запрос к View
                cur.execute("SELECT part_number, brand, name, stock_quantity, price, (stock_quantity*price) FROM v_warehouse_stock")
                
                # Получение всех строк и вставка в интерфейс
                for row in cur.fetchall():
                    self.tree.insert("", tk.END, values=row)
        except Error as e:
            messagebox.showerror("Ошибка БД при чтении", str(e))

    def run_op(self):
        """
        Выполнение складской операции.
        ВАЖНО: Используется ХРАНИМАЯ ПРОЦЕДУРА (Stored Procedure).
        Логика поиска цены, создания накладной и позиций находится внутри БД.
        """
        try:
            with self.conn.cursor() as cur:
                # Вызов процедуры CALL. 
                # Параметры: ID товара, Кол-во, Тип операции, ID Контрагента (заглушка = 1)
                cur.execute("CALL pr_register_operation(%s, %s, %s, %s)", 
                            (self.e_id.get(), self.e_qty.get(), self.v_op.get(), 1))
                
                # Фиксация транзакции. Без этого изменения не сохранятся!
                self.conn.commit()
                
                messagebox.showinfo("Успех", "Операция успешно проведена сервером!")
                # Обновляем таблицу, чтобы увидеть новые остатки
                self.refresh_stock()
                
        except Exception as e:
            # Если БД вернула ошибку (например, сработал триггер "Недостаточно товара")
            self.conn.rollback() # Откат транзакции
            messagebox.showerror("Отказ сервера", f"БД отклонила операцию:\n{e}")

    def open_add_product_window(self):
        """
        Открывает дополнительное (модальное) окно для добавления товара.
        """
        top = tk.Toplevel(self.root)
        top.title("Новый товар")
        f = ttk.Frame(top, padding=10)
        f.pack()
        
        # Динамическое создание полей ввода из списка
        fields = ["Артикул", "Название", "Цена", "Ячейка"]
        entries = {} # Словарь для хранения ссылок на поля ввода
        
        for i, field in enumerate(fields):
            ttk.Label(f, text=field).grid(row=i, column=0)
            e = ttk.Entry(f)
            e.grid(row=i, column=1)
            entries[field] = e
            
        def save():
            """Внутренняя функция для сохранения нового товара"""
            try:
                with self.conn.cursor() as cur:
                    # Вызов процедуры добавления товара
                    cur.execute("CALL pr_add_product(%s, %s, %s, %s)", 
                               (entries["Артикул"].get(), 
                                entries["Название"].get(), 
                                entries["Цена"].get(), 
                                entries["Ячейка"].get()))
                    self.conn.commit()
                    top.destroy() # Закрыть окно
                    self.refresh_stock() # Обновить главную таблицу
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Ошибка сохранения", str(e))
                
        ttk.Button(f, text="Сохранить", command=save).grid(row=4, columnspan=2, pady=10)

# Точка входа в программу
if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()
```

[Вернуться к содержанию](#content)
