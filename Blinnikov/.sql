CREATE TABLE post (post_id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE);
# должности

CREATE TABLE employee (employee_id SERIAL PRIMARY KEY, surname TEXT NOT NULL, name TEXT NOT NULL, patronymic text, post_id INT REFERENCES post(post_id), phone VARCHAR(255));
# сотрудники

CREATE TABLE client (client_id SERIAL PRIMARY KEY, surname TEXT, name TEXT NOT NULL, patronymic text, phone VARCHAR(255), email TEXT);
# клиенты

CREATE TABLE payment_method (payment_method_id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE);
# методы оплаты

CREATE TABLE contact_method (contact_method_id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE);
# методы связи

CREATE TABLE service (service_id SERIAL PRIMARY KEY, name TEXT NOT NULL, service_price NUMERIC(10, 2) NOT NULL);
# услуги

CREATE TABLE order_info (order_info_id SERIAL PRIMARY KEY, order_id INT, service_id INT REFERENCES service(service_id), quantity INT);
# данные о покупке

CREATE TABLE orders (order_id SERIAL PRIMARY KEY, client_id INT REFERENCES client(client_id), payment_method_id INT REFERENCES payment_method(payment_method_id), date TIMESTAMP DEFAULT NOW(), total_sum NUMERIC(10, 2), contact_method_id INT REFERENCES contact_method(contact_method_id));
# все покупки

CREATE TABLE users (user_id SERIAL PRIMARY KEY, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, role TEXT NOT NULL CHECK (role IN ('owner', 'administrator', 'worker', 'accountant')), name TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
# пользователи бд

