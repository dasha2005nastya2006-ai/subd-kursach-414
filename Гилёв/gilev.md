-- 1. Таблица сотрудников (риэлторов)
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE,
    commission_rate DECIMAL(5,2) DEFAULT 2.5,
    is_active BOOLEAN DEFAULT TRUE
);

-- 2. Таблица клиентов (покупатели/продавцы)
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    client_type VARCHAR(10) CHECK (client_type IN ('buyer', 'seller', 'both')),
    registration_date DATE DEFAULT CURRENT_DATE
);

-- 3. Таблица объектов недвижимости
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50),
    property_type VARCHAR(20) CHECK (property_type IN ('apartment', 'house', 'commercial', 'land')),
    rooms INTEGER,
    total_area DECIMAL(10,2) NOT NULL,
    living_area DECIMAL(10,2),
    floor INTEGER,
    total_floors INTEGER,
    price DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'sold', 'rented', 'archived')),
    owner_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    agent_id INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    created_date DATE DEFAULT CURRENT_DATE,
    description TEXT
);

-- 4. Таблица сделок
CREATE TABLE deals (
    id SERIAL PRIMARY KEY,
    property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE RESTRICT,
    buyer_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE RESTRICT,
    seller_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE RESTRICT,
    agent_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE RESTRICT,
    deal_date DATE NOT NULL DEFAULT CURRENT_DATE,
    deal_price DECIMAL(12,2) NOT NULL,
    commission_amount DECIMAL(12,2) NOT NULL,
    deal_type VARCHAR(10) CHECK (deal_type IN ('sale', 'rent')),
    payment_method VARCHAR(30),
    notes TEXT
);

-- 5. Таблица просмотров объектов
CREATE TABLE viewings (
    id SERIAL PRIMARY KEY,
    property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    agent_id INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    viewing_date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    client_feedback TEXT,
    agent_notes TEXT
);

-- 6. Таблица услуг агентства
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    standard_price DECIMAL(10,2),
    duration_days INTEGER
);

-- 7. Таблица заявок на услуги
CREATE TABLE service_requests (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    service_id INTEGER NOT NULL REFERENCES services(id) ON DELETE RESTRICT,
    agent_id INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    request_date DATE DEFAULT CURRENT_DATE,
    completion_date DATE,
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'completed', 'cancelled')),
    actual_price DECIMAL(10,2),
    notes TEXT
);

-- Создадим индексы для улучшения производительности
CREATE INDEX idx_properties_city ON properties(city);
CREATE INDEX idx_properties_price ON properties(price);
CREATE INDEX idx_properties_status ON properties(status);
CREATE INDEX idx_deals_date ON deals(deal_date);
CREATE INDEX idx_deals_agent ON deals(agent_id);
CREATE INDEX idx_viewings_date ON viewings(viewing_date);
CREATE INDEX idx_clients_type ON clients(client_type);

-- Добавим комментарии к таблицам
COMMENT ON TABLE employees IS 'Сотрудники риэлторского агентства';
COMMENT ON TABLE clients IS 'Клиенты агентства (покупатели и продавцы)';
COMMENT ON TABLE properties IS 'Объекты недвижимости';
COMMENT ON TABLE deals IS 'Завершенные сделки';
COMMENT ON TABLE viewings IS 'Просмотры объектов недвижимости';
COMMENT ON TABLE services IS 'Услуги, предоставляемые агентством';
COMMENT ON TABLE service_requests IS 'Заявки клиентов на услуги';

-- 1. Заполняем таблицу сотрудников (риэлторов)
INSERT INTO employees (first_name, last_name, phone, email, hire_date, commission_rate, is_active) VALUES
('Анна', 'Иванова', '+79161234501', 'anna@agency.ru', '2020-03-15', 3.0, true),
('Дмитрий', 'Соколов', '+79161234502', 'dmitry@agency.ru', '2019-07-22', 3.5, true),
('Ольга', 'Кузнецова', '+79161234503', 'olga@agency.ru', '2021-11-05', 2.8, true),
('Сергей', 'Попов', '+79161234504', 'sergey@agency.ru', '2018-05-30', 4.0, false),
('Екатерина', 'Лебедева', '+79161234505', 'ekaterina@agency.ru', '2022-01-18', 2.5, true);

-- 2. Заполняем таблицу клиентов
INSERT INTO clients (first_name, last_name, phone, email, client_type, registration_date) VALUES
('Иван', 'Петров', '+79161112233', 'ivan.petrov@mail.ru', 'seller', '2023-01-10'),
('Мария', 'Сидорова', '+79162223344', 'maria.sidorova@gmail.com', 'buyer', '2023-02-15'),
('Александр', 'Васильев', '+79163334455', 'alex.vasiliev@yandex.ru', 'both', '2023-03-20'),
('Елена', 'Михайлова', '+79164445566', 'elena.mikhailova@mail.ru', 'seller', '2023-04-05'),
('Андрей', 'Федоров', '+79165556677', 'andrey.fedorov@gmail.com', 'buyer', '2023-05-12'),
('Наталья', 'Морозова', '+79166667788', 'natalya.morozova@yandex.ru', 'both', '2023-06-18'),
('Павел', 'Никитин', '+79167778899', 'pavel.nikitin@mail.ru', 'seller', '2023-07-22'),
('Юлия', 'Захарова', '+79168889900', 'yulia.zakharova@gmail.com', 'buyer', '2023-08-30');

-- 3. Заполняем таблицу объектов недвижимости
INSERT INTO properties (address, city, district, property_type, rooms, total_area, living_area, floor, total_floors, price, status, owner_id, agent_id, created_date, description) VALUES
('ул. Ленина, д. 10, кв. 25', 'Москва', 'Центральный', 'apartment', 2, 54.5, 38.2, 5, 9, 12500000.00, 'active', 1, 1, '2023-01-20', 'Квартира с евроремонтом, вид на парк'),
('пр. Победы, д. 45, кв. 12', 'Москва', 'Северный', 'apartment', 3, 78.3, 55.6, 7, 12, 18500000.00, 'active', 4, 2, '2023-04-10', 'Просторная трехкомнатная квартира, свежий ремонт'),
('ул. Садовая, д. 15', 'Москва', 'Западный', 'house', 4, 120.5, 95.8, 1, 2, 35000000.00, 'sold', 3, 3, '2023-03-01', 'Частный дом с участком 6 соток'),
('ул. Молодежная, д. 8, кв. 7', 'Москва', 'Южный', 'apartment', 1, 36.8, 24.5, 2, 5, 8500000.00, 'active', 7, 1, '2023-07-25', 'Студия в новостройке, с отделкой'),
('ул. Центральная, д. 33', 'Москва', 'Восточный', 'commercial', 0, 250.0, 250.0, 1, 3, 50000000.00, 'active', 4, 2, '2023-04-15', 'Торговое помещение в центре района'),
('ул. Лесная, д. 5', 'Москва', 'Северный', 'land', 0, 1200.0, 0.0, 0, 0, 15000000.00, 'active', 1, 3, '2023-01-25', 'Земельный участок под ИЖС'),
('ул. Школьная, д. 18, кв. 42', 'Москва', 'Западный', 'apartment', 2, 48.3, 32.7, 3, 5, 9500000.00, 'rented', 6, 1, '2023-06-20', 'Сдается в аренду, долгосрочно'),
('ул. Парковая, д. 22', 'Москва', 'Центральный', 'house', 5, 180.2, 145.6, 1, 2, 42000000.00, 'active', 3, 2, '2023-03-25', 'Элитный коттедж с бассейном');

-- 4. Заполняем таблицу сделок
INSERT INTO deals (property_id, buyer_id, seller_id, agent_id, deal_date, deal_price, commission_amount, deal_type, payment_method, notes) VALUES
(3, 2, 3, 3, '2023-03-15', 34500000.00, 1035000.00, 'sale', 'ипотека', 'Сделка прошла успешно, покупатель оформил ипотеку в Сбербанке'),
(7, 5, 6, 1, '2023-07-01', 9500000.00, 237500.00, 'rent', 'наличные', 'Долгосрочная аренда на 3 года с возможностью продления'),
(1, 8, 1, 1, '2023-09-10', 12200000.00, 366000.00, 'sale', 'ипотека', 'Покупатель - молодая семья, первый взнос от родителей');

-- 5. Заполняем таблицу просмотров объектов
INSERT INTO viewings (property_id, client_id, agent_id, viewing_date, status, client_feedback, agent_notes) VALUES
(1, 2, 1, '2023-02-10 14:30:00', 'completed', 'Понравилась квартира, но цена высокая', 'Клиент просит скидку 5%'),
(1, 5, 1, '2023-02-12 11:00:00', 'completed', 'Слишком маленькая кухня', 'Ищет квартиру с просторной кухней'),
(2, 5, 2, '2023-04-20 16:00:00', 'completed', 'Отличный вариант, рассмотрю с семьей', 'Высокая вероятность покупки, нужна ипотека'),
(3, 2, 3, '2023-03-10 12:00:00', 'completed', 'Идеально подходит, готовы сделать предложение', 'Срочная сделка, клиент уже продал свою квартиру'),
(4, 8, 1, '2023-08-05 15:30:00', 'completed', 'Устраивает цена, но нет парковки', 'Предложить соседний вариант с парковкой'),
(4, 5, 1, '2023-08-10 10:00:00', 'cancelled', NULL, 'Клиент не пришел, не отвечает на звонки'),
(5, 6, 2, '2023-09-15 17:00:00', 'scheduled', NULL, 'Запланирован просмотр под бизнес'),
(8, 2, 2, '2023-10-01 14:00:00', 'scheduled', NULL, 'Потенциальный покупатель из другого города');

-- 6. Заполняем таблицу услуг
INSERT INTO services (service_name, description, standard_price, duration_days) VALUES
('Оценка недвижимости', 'Профессиональная оценка рыночной стоимости объекта', 5000.00, 3),
('Юридическое сопровождение', 'Проверка документов и юридическое сопровождение сделки', 15000.00, 7),
('Подбор недвижимости', 'Поиск объектов по критериям клиента', 10000.00, 14),
('Ипотечное сопровождение', 'Помощь в получении ипотечного кредита', 8000.00, 10),
('Фотосъемка объекта', 'Профессиональная фотосъемка для рекламы', 3000.00, 1),
('Консультация по инвестициям', 'Консультация по инвестициям в недвижимость', 7000.00, 2),
('Сдача в аренду', 'Полное сопровождение сдачи объекта в аренду', 12000.00, 5);

-- 7. Заполняем таблицу заявок на услуги
INSERT INTO service_requests (client_id, service_id, agent_id, request_date, completion_date, status, actual_price, notes) VALUES
(1, 1, 1, '2023-01-12', '2023-01-15', 'completed', 5000.00, 'Оценка для продажи квартиры на Ленина 10'),
(2, 3, 1, '2023-02-01', '2023-02-20', 'completed', 10000.00, 'Поиск 2-комнатной квартиры в центре'),
(3, 2, 3, '2023-03-05', '2023-03-12', 'completed', 15000.00, 'Сопровождение сделки по дому на Садовой'),
(4, 1, 2, '2023-04-08', '2023-04-11', 'completed', 5000.00, 'Оценка коммерческого помещения'),
(5, 4, 1, '2023-05-20', NULL, 'in_progress', 8000.00, 'Помощь в получении ипотеки для студии'),
(6, 7, 1, '2023-06-22', '2023-06-27', 'completed', 12000.00, 'Сопровождение сдачи квартиры в аренду'),
(7, 5, 1, '2023-07-26', '2023-07-27', 'completed', 3000.00, 'Фотосъемка квартиры для объявления'),
(8, 6, 2, '2023-08-31', NULL, 'new', 7000.00, 'Консультация по инвестициям в недвижимость');

-- 1. Посмотреть всех активных сотрудников
SELECT * FROM employees WHERE is_active = true;

-- 2. Показать активные объекты недвижимости в Москве
SELECT p.address, p.price, p.rooms, p.total_area, 
       c.first_name || ' ' || c.last_name as owner_name,
       e.first_name || ' ' || e.last_name as agent_name
FROM properties p
LEFT JOIN clients c ON p.owner_id = c.id
LEFT JOIN employees e ON p.agent_id = e.id
WHERE p.city = 'Москва' AND p.status = 'active'
ORDER BY p.price DESC;

-- 3. Посмотреть все сделки с информацией
SELECT d.deal_date, d.deal_price, d.commission_amount,
       p.address as property_address,
       buyer.first_name || ' ' || buyer.last_name as buyer_name,
       seller.first_name || ' ' || seller.last_name as seller_name,
       e.first_name || ' ' || e.last_name as agent_name
FROM deals d
JOIN properties p ON d.property_id = p.id
JOIN clients buyer ON d.buyer_id = buyer.id
JOIN clients seller ON d.seller_id = seller.id
JOIN employees e ON d.agent_id = e.id;

-- 4. Статистика по агентам (количество сделок и сумма комиссий)
SELECT e.first_name || ' ' || e.last_name as agent_name,
       COUNT(d.id) as total_deals,
       COALESCE(SUM(d.commission_amount), 0) as total_commission
FROM employees e
LEFT JOIN deals d ON e.id = d.agent_id
WHERE e.is_active = true
GROUP BY e.id
ORDER BY total_commission DESC;

-- 5. Показать запланированные просмотры
SELECT v.viewing_date, p.address, 
       c.first_name || ' ' || c.last_name as client_name,
       e.first_name || ' ' || e.last_name as agent_name
FROM viewings v
JOIN properties p ON v.property_id = p.id
JOIN clients c ON v.client_id = c.id
LEFT JOIN employees e ON v.agent_id = e.id
WHERE v.status = 'scheduled'
ORDER BY v.viewing_date;

-- 6. Доходы от услуг
SELECT s.service_name, COUNT(sr.id) as request_count, 
       COALESCE(SUM(sr.actual_price), 0) as total_income
FROM services s
LEFT JOIN service_requests sr ON s.id = sr.service_id
GROUP BY s.id
ORDER BY total_income DESC;
