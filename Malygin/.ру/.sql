Пояснение к таблицам!
 Таблицы:
CREATE TABLE cat (cat_id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE);
# таблица категорий #

CREATE TABLE manufacturer (manufacturer_id SERIAL PRIMARY KEY, name TEXT NOT NULL, email TEXT, phone VARCHAR(255));
# таблица производителей #

CREATE TABLE supplier (supplier_id SERIAL PRIMARY KEY, name TEXT NOT NULL, email TEXT, phone VARCHAR(255));
# таблица потсавщиков #

CREATE TABLE post (post_id SERIAL PRIMARY KEY, name TEXT NOT NULL);
# таблица должностей #

CREATE TABLE employees (employees_id SERIAL PRIMARY KEY, surname TEXT NOT NULL, name TEXT NOT NULL, post_id INT REFERENCES post(post_id), phone VARCHAR(255));
# таблица сотрудников #

CREATE TABLE client (client_id SERIAL PRIMARY KEY, surname TEXT, name TEXT NOT NULL, phone VARCHAR(255), email TEXT);
# таблица клиентов #

CREATE TABLE pay_method (pay_method_id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE);
# таблица методов оплаты #

CREATE TABLE contact_method (contact_method_id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE);
# таблица методов связи #

CREATE TABLE product (product_id SERIAL PRIMARY KEY, cat_id INT REFERENCES cat(cat_id), manufacturer_id INT REFERENCES manufacturer(manufacturer_id), supplier_id INT REFERENCES supplier(supplier_id), name TEXT NOT NULL, stock INT NOT NULL DEFAULT 0, purch_price NUMERIC(10, 2) NOT NULL, sale_price NUMERIC(10, 2) NOT NULL);
# таблица товаров #

CREATE TABLE order_info (order_info_id SERIAL PRIMARY KEY, order_id INT, product_id INT REFERENCES product(product_id), quantity INT);
# таблица "корзины" #

CREATE TABLE orders (order_id SERIAL PRIMARY KEY, client_id INT REFERENCES client(client_id), order_info_id INT references order_info(order_info_id), pay_method_id INT REFERENCES pay_method(pay_method_id), date TIMESTAMP DEFAULT NOW(), total_sum NUMERIC(10, 2));
# таблица покупок #

CREATE TABLE users (user_id SERIAL PRIMARY KEY, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, role TEXT NOT NULL CHECK (role IN ('admin', 'seller', 'accountant')), full_name TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
# таблица для авторизации #

----------
==========
----------

Пользователи:
INSERT INTO users (username, password_hash, role, full_name) VALUES ('admin', %s, 'admin', 'администратор системы'), ('seller1', %s, 'seller', 'продавец'), ('accountant1', %s, 'accountant', 'бухгалтер') ON CONFLICT (username) DO NOTHING;
# %s - переменная в ЯП Python, служащая для приема вводимых пользователем данных. В данном случае вводятся данные в столбец "password_hash" #

----------
==========
----------

Заполнение таблиц:
INSERT INTO cat (name) VALUES ('Электрогитары'), ('Акустические гитары'), ('Бас-гитары'), ('Классические гитары'), ('Укулеле') ON CONFLICT (name) DO NOTHING;
INSERT INTO manufacturer (name, email, phone) VALUES ('Fender', 'info@fender.com', '+1-800-000-0001'), ('Gibson', 'info@gibson.com', '+1-800-000-0002'), ('Ibanez', 'info@ibanez.com', '+81-3-0000-0003'), ('Yamaha', 'info@yamaha.com', '+81-3-0000-0004'), ('Taylor', 'info@taylor.com', '+1-800-000-0005') ON CONFLICT DO NOTHING;
INSERT INTO supplier (name, email, phone) VALUES ('Music Supplies Inc.', 'orders@musicsupplies.com', '+1-800-100-0001'), ('Guitar World Ltd.', 'sales@guitarworld.com', '+1-800-100-0002'), ('Pro Audio Dist.', 'info@proaudio.com', '+1-800-100-0003') ON CONFLICT DO NOTHING;
INSERT INTO post (name) VALUES ('Продавец'), ('Бухгалтер'), ('Администратор') ON CONFLICT DO NOTHING;
INSERT INTO pay_method (name) VALUES ('Наличные'), ('Банковская карта'), ('Безналичный расчет'), ('Онлайн оплата') ON CONFLICT (name) DO NOTHING;
INSERT INTO contact_method (name) VALUES ('Телефон'), ('Email'), ('Telegram'), ('WhatsApp') ON CONFLICT (name) DO NOTHING;

----------
==========
----------

Авторизация:
SELECT user_id, username, role, full_name FROM users WHERE username = %s AND password_hash = %s
# тут данные берутся из олей ввода в программе, сравниваются с данными в таблице. в коде предусмотрен обработчик ошибок, который не даст войти с неверными данными. #

----------
==========
----------

Функционал приложения, зависящий от роли:
Функционал зависит от роли, от который был выполнен вход в базу. Интерфейс, функции, доступы жестко привязаны к роли. выполнено в коде программы.

----------
==========
----------

Дополнительные данные:
- ветка 1:
SELECT o.order_id, c.name, o.date, o.total_sum FROM orders o JOIN client c ON o.client_id = c.client_id ORDER BY o.date DESC LIMIT 10;
# Запрос, выводящий список последних десяти покупок #

SELECT COUNT(*) FROM product;
# Запрос, выводящий список товаров #

SELECT COUNT(*) FROM client;
# Запрос, выводящий список клиентов #

SELECT COALESCE(SUM(total_sum), 0) FROM orders;
# Запрос, выводящий сумму выручки #

SELECT COUNT(*) FROM product WHERE stock < 10;
# Запрос, выводящий остатки товаров #

SELECT COUNT(*), COALESCE(SUM(total_sum), 0) FROM orders WHERE DATE(date) = CURRENT_DATE;
# Запрос, выводящий сумму продаж за определенный день (параметр CURRENT_DATE) #

SELECT COUNT(*) FROM product WHERE stock > 0;
# Запрос, выводящий число товаров, которые можно приобрести #

SELECT COALESCE(SUM(total_sum), 0) FROM orders;
# Запрос, выводящий общую сумму прибыли #

SELECT COALESCE(AVG(total_sum), 0) FROM orders;
# Запрос, выводящий среднюю сумму чека #

-- ветка 2
для входа в базу данных нужно сначала войти в саму СУБД (логин postgres, пароль pgadmin), далее ввести данные для входа роли.
admin - admin123 # Админ (логин - пароль) #
seller1 - seller123 # Продавец (логин - пароль) #
accountant1 - accountant123 # Бухгалтер (логин - пароль) #




