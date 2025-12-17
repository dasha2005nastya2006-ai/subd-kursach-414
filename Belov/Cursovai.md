Create table place
(id_p serial4 primary key,
name varchar not null,
position varchar);

Create table time
(id_time serial4 primary key,
mounth varchar not null,
year int4 not null);

Create table objects
(id_ob serial4 primary key,
object_name varchar not null,
object_cod varchar not null,
creation_year int4,
IMAGE varchar,
description varchar);

Create table history
(id serial4 primary key,
id_ob int4 not null,
id_type int4 not null,
id_time int4 not null,
id_p int4 not null,
count int4 not null,
FOREIGN KEY (id_ob) REFERENCES objects (id_ob),
FOREIGN KEY (id_time) REFERENCES time (id_time),
FOREIGN KEY (id_p) REFERENCES place (id_p));

CREATE TABLE users
(id_u serial4 primary key,
login varchar(30) UNIQUE NOT NULL,
password varchar (50) not null);


CREATE OR REPLACE VIEW v_full_history AS
SELECT 
    h.id AS history_id,
    o.object_name,
    o.object_cod,
    p.name AS place_name,
    p.position AS place_position,
    h.count,
    h.id_type
FROM history h
JOIN objects o ON h.id_ob = o.id_ob
JOIN place p ON h.id_p = p.id_p;


CREATE OR REPLACE PROCEDURE _add_place(
    _name varchar, 
    _position varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO place (name, position)
    VALUES (_name, _position);
END;
$$;

CREATE OR REPLACE PROCEDURE add_object(
    _object_name varchar,
    _object_cod varchar,
    _creation_year int4,
    _image varchar,
    _description varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO objects (object_name, object_cod, creation_year, IMAGE, description)
    VALUES (_object_name, _object_cod, _creation_year, _image, _description);
END;
$$;

CREATE OR REPLACE PROCEDURE add_user(
    _login varchar, 
    _password varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users (login, password)
    VALUES (_login, _password);
    
    EXCEPTION WHEN unique_violation THEN
        RAISE NOTICE 'Пользователь с логином % уже существует.', _login;
END;
$$;


CREATE OR REPLACE PROCEDURE add_history(
    _id_ob int4,
    _id_type int4,
    _id_time int4,
    _id_p int4,
    _count int4
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM objects WHERE id_ob = _id_ob) THEN
        RAISE EXCEPTION 'Объект с ID % не найден', _id_ob;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM time WHERE id_time = _id_time) THEN
        RAISE EXCEPTION 'Время с ID % не найдено', _id_time;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM place WHERE id_p = _id_p) THEN
        RAISE EXCEPTION 'Место с ID % не найдено', _id_p;
    END IF;

    INSERT INTO history (id_ob, id_type, id_time, id_p, count)
    VALUES (_id_ob, _id_type, _id_time, _id_p, _count);
END;
$$;


-- 1. Создаем место
CALL pr_add_place('Главный склад', 'Полка 5');

-- 2. Создаем временную метку
CALL pr_add_time('Декабрь', 2024);

-- 3. Создаем объект
CALL pr_add_object('Монитор', 'MON-24', 2024, NULL);

-- 4. Создаем пользователя
CALL pr_add_user('admin', 'admin123');

-- 5. Создаем запись в истории (предполагая, что это первые записи, их ID будут 1)
-- Объект(1), Тип(1), Время(1), Место(1), Кол-во(50)
CALL pr_add_history(1, 1, 1, 1, 50);


CREATE OR REPLACE FUNCTION fn_show_places()
RETURNS TABLE (
    id int4,
    place_name varchar,
    position_info varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT id_p, name, position
    FROM place
    ORDER BY id_p;
END;
$$;


CREATE OR REPLACE FUNCTION fn_show_objects()
RETURNS TABLE (
    id int4,
    name varchar,
    code varchar,
    created_year int4,
    img_path varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT id_ob, object_name, object_cod, creation_year, IMAGE
    FROM objects
    ORDER BY object_name;
END;
$$;

CREATE OR REPLACE FUNCTION fn_show_time()
RETURNS TABLE (
    id int4,
    month_name varchar,
    year_num int4
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT id_time, mounth, year
    FROM time
    ORDER BY year DESC, id_time;
END;
$$;


CREATE OR REPLACE FUNCTION fn_show_objects()
RETURNS TABLE (
    id int4,
    name varchar,
    code varchar,
    created_year int4,
    img_path varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT id_ob, object_name, object_cod, creation_year, IMAGE
    FROM objects
    ORDER BY object_name;
END;
$$;


CREATE OR REPLACE FUNCTION fn_show_full_history()
RETURNS TABLE (
    history_id int4,
    obj_name varchar,
    obj_code varchar,
    type_id int4,       -- Таблицы типов у нас нет, выводим ID
    place_name varchar,
    month varchar,
    year int4,
    amount int4
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        h.id, 
        o.object_name, 
        o.object_cod,
        h.id_type,
        p.name, 
        t.mounth, 
        t.year, 
        h.count
    FROM history h
    JOIN objects o ON h.id_ob = o.id_ob
    JOIN place p ON h.id_p = p.id_p
    JOIN time t ON h.id_time = t.id_time
    ORDER BY h.id;
END;
$$;


SELECT * FROM fn_show_full_history();

SELECT * FROM fn_show_users();

SELECT * FROM fn_show_objects();

SELECT * FROM fn_show_time();

SELECT * FROM fn_show_places();
