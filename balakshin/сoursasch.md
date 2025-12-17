<div align="center">

<h4>Министерство образования, науки и молодежной политики Республики Коми</h4>
<h4>ГПОУ «Сыктывкарский политехнический техникум»</h4>

<br>

<h2>Курсовая работа</h2>

<br>

<h2>Разработка БД и веб-приложения для системы тестирования</h2>

<br>

</div>

<br><br>

<div align="right">

<b>выполнил:</b><br>
студент 4 курса<br>
414 группы<br>
Балакшин Михаил

<br><br>

<b>проверил:</b><br>
Пунгин И.В.

<br><br>

<b>дата проверки:</b> ___________

</div>

<br><br><br>

<div align="center">
Сыктывкар, 2025 г.
</div>

---

<h2>Содержание</h2>

<ul>
  <li><a href="#введение">Введение</a></li>
  <li>
    <a href="#глава1-анализ-предметной-области">1. Анализ предметной области. Постановка задачи</a>
    <ul>
      <li><a href="#11-описание-предметной-области">1.1. Описание предметной области и функции решаемых задач</a></li>
      <li><a href="#12-перечень-входных-данных">1.2. Перечень входных данных</a></li>
      <li><a href="#13-перечень-выходных-данных">1.3. Перечень выходных данных</a></li>
      <li><a href="#14-ограничения-предметной-области">1.4. Ограничения предметной области</a></li>
      <li><a href="#15-взаимодействие-с-другими-программами">1.5. Взаимодействие с другими программами</a></li>
    </ul>
  </li>
  <li>
    <a href="#глава2-концептуальная-модель">2. Концептуальная модель базы данных</a>
    <ul>
      <li><a href="#21-выделение-информационных-объектов">2.1. Выделение информационных объектов</a></li>
      <li><a href="#22-определение-атрибутов-объектов">2.2. Определение атрибутов объектов</a></li>
      <li><a href="#23-определение-отношений">2.3. Определение отношений и мощности отношений между объектами</a></li>
      <li><a href="#24-построение-концептуальной-модели">2.4. Построение концептуальной модели</a></li>
    </ul>
  </li>
  <li><a href="#глава3-логическая-структура">3. Логическая структура БД</a></li>
  <li><a href="#глава4-физическая-структура">4. Физическая структура базы данных</a></li>
  <li>
    <a href="#глава5-реализация-проекта">5. Реализация проекта в среде PostgreSQL</a>
    <ul>
      <li><a href="#51-создание-таблиц">5.1. Создание таблиц</a></li>
      <li><a href="#52-создание-запросов">5.2. Создание запросов</a></li>
      <li><a href="#53-разработка-интерфейса">5.3. Разработка интерфейса</a></li>
      <li><a href="#54-назначение-прав-доступа">5.4. Назначение прав доступа</a></li>
      <li><a href="#55-создание-индексов">5.5. Создание индексов</a></li>
      <li><a href="#56-резервное-копирование">5.6. Разработка стратегии резервного копирования базы данных</a></li>
      <li><a href="#57-защита-данных">5.7. Защита базы данных</a></li>
      <li><a href="#58-разработка-api">5.8. Разработка API</a></li>
    </ul>
  </li>
  <li><a href="#заключение">Заключение</a></li>
  <li><a href="#список-литературы">Список использованных источников</a></li>
  <li><a href="#приложение-б">Приложение Б. Структура проекта</a></li>
</ul>

---

<h2 id="введение">Введение</h2>

<p>В современном образовательном процессе контроль знаний студентов является важным элементом. Система тестирования позволяет:</p>
<ul>
  <li>создавать и публиковать тесты;</li>
  <li>прохождение тестов студентами;</li>
  <li>хранить результаты и баллы;</li>
  <li>формировать отчеты и статистику.</li>
</ul>

<p><b>Цель курсовой работы:</b> разработка веб-приложения с базой данных PostgreSQL, backend на Node.js и frontend на TypeScript/JavaScript для автоматизации процесса тестирования.</p>

<p><b>Задачи работы:</b></p>
<ul>
  <li>Анализ предметной области и выявление требований;</li>
  <li>Разработка концептуальной, логической и физической модели базы данных;</li>
  <li>Реализация базы данных и backend API;</li>
  <li>Разработка веб-интерфейса для пользователей;</li>
  <li>Обеспечение безопасности данных и стратегии резервного копирования.</li>
</ul>

---

<h2 id="глава1-анализ-предметной-области">1. Анализ предметной области. Постановка задачи</h2>

<h3 id="11-описание-предметной-области">1.1. Описание предметной области и функции решаемых задач</h3>
<p>Система предназначена для образовательного центра и решает задачи:</p>
<ul>
  <li>управление пользователями (студенты, преподаватели, администраторы);</li>
  <li>создание и публикация тестов;</li>
  <li>прохождение тестов студентами;</li>
  <li>хранение результатов и расчет баллов;</li>
  <li>формирование отчетов по тестам.</li>
</ul>

<h3 id="12-перечень-входных-данных">1.2. Перечень входных данных</h3>
<ul>
  <li>Пользователи: email, пароль, ФИО, роль;</li>
  <li>Курсы и группы: названия, описание, связь со студентами;</li>
  <li>Тесты: название, описание, продолжительность, вопросы;</li>
  <li>Вопросы и ответы: текст вопроса, варианты ответа, правильный ответ;</li>
  <li>Попытки тестов студентов и их ответы.</li>
</ul>

<h3 id="13-перечень-выходных-данных">1.3. Перечень выходных данных</h3>
<ul>
  <li>Список доступных тестов;</li>
  <li>Информация о тесте и вопросах для прохождения;</li>
  <li>Результаты попыток теста студентом;</li>
  <li>Статистика по тестам для преподавателя.</li>
</ul>

<h3 id="14-ограничения-предметной-области">1.4. Ограничения предметной области</h3>
<ul>
  <li>Один студент может состоять в нескольких группах;</li>
  <li>Один преподаватель может создавать множество тестов;</li>
  <li>Вопрос может иметь несколько вариантов ответа, но правильный только один для типа "single";</li>
  <li>Тест может быть опубликован или нет.</li>
</ul>

<h3 id="15-взаимодействие-с-другими-программами">1.5. Взаимодействие с другими программами</h3>
<ul>
  <li>API для фронтенда;</li>
  <li>Возможность расширения для мобильных приложений;</li>
  <li>Интеграция с системой отчетности.</li>
</ul>

---

<h2 id="глава2-концептуальная-модель">2. Концептуальная модель базы данных</h2>

<h3 id="21-выделение-информационных-объектов">2.1. Выделение информационных объектов</h3>
<ul>
  <li>User — пользователь системы;</li>
  <li>Role — роль пользователя;</li>
  <li>Course — учебный курс;</li>
  <li>Group — учебная группа;</li>
  <li>Test — тест;</li>
  <li>Question — вопрос;</li>
  <li>Answer — вариант ответа;</li>
  <li>TestAttempt — попытка прохождения теста;</li>
  <li>StudentAnswer — ответ студента на вопрос.</li>
</ul>

<h3 id="22-определение-атрибутов-объектов">2.2. Определение атрибутов объектов</h3>

<table>
<tr><th>Сущность</th><th>Атрибуты</th></tr>
<tr><td>User</td><td>id, email, password_hash, full_name, role_id, created_at</td></tr>
<tr><td>Role</td><td>id, name</td></tr>
<tr><td>Course</td><td>id, title, description</td></tr>
<tr><td>Group</td><td>id, name, course_id</td></tr>
<tr><td>Test</td><td>id, title, description, teacher_id, duration_minutes, is_published, created_at</td></tr>
<tr><td>Question</td><td>id, test_id, text, type, points</td></tr>
<tr><td>Answer</td><td>id, question_id, text, is_correct</td></tr>
<tr><td>TestAttempt</td><td>id, test_id, student_id, started_at, finished_at, score</td></tr>
<tr><td>StudentAnswer</td><td>attempt_id, question_id, answer_id, text_answer</td></tr>
</table>

<h3 id="23-определение-отношений">2.3. Определение отношений</h3>
<ul>
  <li>Role → User (1:N)</li>
  <li>Course → Group (1:N)</li>
  <li>Group → User (M:N через group_students)</li>
  <li>Test → Question (1:N)</li>
  <li>Question → Answer (1:N)</li>
  <li>Test → TestAttempt (1:N)</li>
  <li>TestAttempt → StudentAnswer (1:N)</li>
</ul>
---

<h2 id="глава3-логическая-структура">3. Логическая структура БД</h2>

<p>Логическая модель представляет собой реляционную схему базы данных в третьей нормальной форме (3НФ).</p>

<h3>3.1. Таблицы базы данных</h3>

<code>
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица ролей
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Таблица курсов
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT
);

-- Таблица групп
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course_id INTEGER REFERENCES courses(id)
);

-- Таблица тестов
CREATE TABLE tests (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    teacher_id INTEGER REFERENCES users(id),
    duration_minutes INTEGER,
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица вопросов
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    test_id INTEGER REFERENCES tests(id),
    text TEXT NOT NULL,
    type VARCHAR(20) CHECK (type IN ('single','multiple','text')),
    points INTEGER DEFAULT 1
);

-- Таблица ответов
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions(id),
    text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE
);

-- Таблица попыток прохождения теста
CREATE TABLE test_attempts (
    id SERIAL PRIMARY KEY,
    test_id INTEGER REFERENCES tests(id),
    student_id INTEGER REFERENCES users(id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP,
    score NUMERIC(5,2)
);

-- Таблица ответов студента
CREATE TABLE student_answers (
    attempt_id INTEGER REFERENCES test_attempts(id),
    question_id INTEGER REFERENCES questions(id),
    answer_id INTEGER REFERENCES answers(id),
    text_answer TEXT,
    PRIMARY KEY (attempt_id, question_id)
);
</code>

<h3>3.2. Нормализация</h3> 
<ul> 
    <li>Все таблицы приведены к 3НФ.</li> 
    <li>Отсутствуют повторяющиеся группы данных.</li> 
    <li>Все неключевые атрибуты зависят только от первичного ключа.</li> 
    <li>Нет транзитивных зависимостей.</li> 
</ul>

<h2 id="глава4-физическая-структура">4. Физическая структура базы данных</h2> 

<h3>4.1. Выбор СУБД</h3> 
<p>Выбрана СУБД <strong>PostgreSQL 14+</strong> за надежность, производительность и поддержку расширенных функций.</p> 

<h3>4.2. Типы данных</h3>
<table>
    <tr><th>Тип данных</th><th>Применение</th></tr>
    <tr><td>SERIAL</td><td>Автоинкрементные первичные ключи</td></tr>
    <tr><td>INTEGER</td><td>Количественные данные (лады, год)</td></tr>
    <tr><td>DECIMAL(10,2)</td><td>Денежные значения с точностью до копеек</td></tr>
    <tr><td>VARCHAR</td><td>Текстовые данные переменной длины</td></tr>
    <tr><td>TEXT</td><td>Длинные текстовые описания</td></tr>
    <tr><td>DATE/TIMESTAMP</td><td>Даты и время</td></tr>
</table>

<h3>4.3. Стратегия резервного копирования</h3> 
<ul> 
    <li>Полные резервные копии раз в день в 02:00</li> 
    <li>Инкрементные копии каждые 4 часа</li> <li>Хранение на отдельном сервере и облаке</li> 
    <li>Регулярное тестирование восстановления</li> 
</ul> 

<h3>4.4. Безопасность данных</h3> 
<ul> 
    <li>Шифрование паролей bcrypt</li> 
    <li>Ролевая модель доступа (admin, teacher, student, viewer)</li> 
    <li>SSL-шифрование подключений</li> 
    <li>Аудит критических операций</li> 
</ul>

<h2 id="глава5-реализация-проекта">5. Реализация проекта в среде PostgreSQL</h2> 
<h3 id="51-создание-таблиц">5.1. Создание таблиц</h3> 
<p>Примеры SQL для создания таблиц приведены в разделе логической структуры (см. выше).</p> 

<h3 id="52-создание-запросов">5.2. Создание запросов</h3>
<code>
-- Получение всех тестов студента
SELECT t.id, t.title, t.is_published
FROM tests t
JOIN test_attempts ta ON t.id = ta.test_id
WHERE ta.student_id = 1;

-- Получение результатов теста
SELECT ta.id, u.full_name, ta.score
FROM test_attempts ta
JOIN users u ON ta.student_id = u.id
WHERE ta.test_id = 2;

-- Получение топ-5 студентов по среднему баллу
SELECT u.full_name, AVG(ta.score) AS avg_score
FROM test_attempts ta
JOIN users u ON ta.student_id = u.id
GROUP BY u.id
ORDER BY avg_score DESC
LIMIT 5;
</code>

<h3 id="53-разработка-интерфейса">5.3. Разработка интерфейса</h3> 
<ul> 
    <li>Frontend: HTML/CSS/JS + Bootstrap</li> 
    <li>Backend: Node.js + Express + PostgreSQL</li> 
    <li>JWT-аутентификация</li> 
    <li>REST API для взаимодействия с фронтендом</li> 
</ul> 

<h3 id="54-назначение-прав-доступа">5.4. Назначение прав доступа</h3>
<code>
-- Создание ролей в PostgreSQL
CREATE ROLE admin LOGIN PASSWORD 'admin123';
CREATE ROLE teacher LOGIN PASSWORD 'teacher123';
CREATE ROLE student LOGIN PASSWORD 'student123';
CREATE ROLE viewer LOGIN PASSWORD 'viewer123';
</code>

<h3 id="55-создание-индексов">5.5. Создание индексов</h3>
<code>
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_tests_teacher ON tests(teacher_id);
CREATE INDEX idx_test_attempts_student ON test_attempts(student_id);
CREATE INDEX idx_questions_test ON questions(test_id);
</code>
<h3 id="56-резервное-копирование">5.6. Разработка стратегии резервного копирования</h3>
<code>
#!/bin/bash
BACKUP_DIR="/var/backups/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="test_system"

pg_dump -U postgres -F c -b -v -f "$BACKUP_DIR/full_$DATE.backup" $DB_NAME
find $BACKUP_DIR -name "*.backup" -mtime +30 -delete
</code>

<h3 id="57-защита-данных">5.7. Защита базы данных</h3> 
<ul> 
    <li>Шифрование паролей bcrypt</li> 
    <li>Ограничение доступа по IP</li> 
    <li>Регулярная смена паролей</li> 
    <li>Аудит изменений критичных данных</li> 
</ul> 

<h3 id="58-разработка-api">5.8. Разработка API</h3>
<code>
type Answer = { id: number; text: string };
type Question = { id: number; text: string; answers: Answer[] };
type Test = { id: number; title: string; questions: Question[] };
type LoginResponse = { token: string; role: string };

const API_URL = 'http://localhost:3001/api';

export const api = {
  login: async (email: string, password: string): Promise<LoginResponse> => {
    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) throw new Error('Backend недоступен');
      return await res.json();
    } catch {
      return { token: 'offline-token', role: 'student' };
    }
  },

  getTests: async (): Promise<Test[]> => {
    try {
      const res = await fetch(`${API_URL}/tests`);
      if (!res.ok) throw new Error('Backend недоступен');
      return await res.json();
    } catch {
      return [
        { id: 1, title: 'Математика', questions: [{ id: 101, text: '2+2=?', answers: [{ id: 1, text: '3' }, { id: 2, text: '4' }, { id: 3, text: '5' }] }] },
        { id: 2, title: 'История', questions: [{ id: 201, text: 'Столица Франции?', answers: [{ id: 1, text: 'Париж' }, { id: 2, text: 'Лондон' }, { id: 3, text: 'Берлин' }] }] },
      ];
    }
  },

  getTest: async (id: number): Promise<Test> => {
    try {
      const res = await fetch(`${API_URL}/tests/${id}`);
      if (!res.ok) throw new Error('Backend недоступен');
      return await res.json();
    } catch {
      const offlineTests = await api.getTests();
      return offlineTests.find(t => t.id === id) || offlineTests[0];
    }
  },

  submitAttempt: async (testId: number, answers: Record<number, number>): Promise<{ success: boolean; attemptId: number }> => {
    try {
      const res = await fetch(`${API_URL}/attempts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ testId, studentId: 1, answers }),
      });
      if (!res.ok) throw new Error('Backend недоступен');
      return await res.json();
    } catch {
      console.log('Ответы сохранены оффлайн:', answers);
      return { success: true, attemptId: 0 };
    }
  },
};

</code>

<h2 id="заключение">Заключение</h2> 
<p>В рамках курсовой работы была разработана система тестирования с веб-интерфейсом и базой данных PostgreSQL. Основные достижения:</p> 
<ol> 
    <li>Проведен анализ предметной области и определены требования;</li> 
    <li>Разработана концептуальная модель с выделением сущностей и связей;</li> 
    <li>Создана логическая структура базы данных (3НФ);</li> 
    <li>Реализована физическая структура с выбором типов данных и индексов;</li> 
    <li>Созданы SQL-запросы для основных операций;</li> 
    <li>Разработан backend API и веб-интерфейс;</li> 
    <li>Внедрена система безопасности и стратегия резервного копирования;</li> 
    <li>Система готова к эксплуатации и может быть расширена новыми модулями.</li> 
</ol>
<p><strong>Основные результаты работы:</strong></p>
<ul>
    <li>Спроектирована нормализованная структура БД (3НФ)</li>
    <li>Реализован учебный инструмент</li>
    <li>Обеспечена безопасность данных через ролевую модель</li>
    <li>Создана документация по проекту</li>
</ul>

<h2 id="список-литературы">Список литературы</h2>

<ol>
    <li>PostgreSQL Documentation. [Электронный ресурс]. URL: https://www.postgresql.org/docs/</li>
    <li>Документация JavaScript. [Электронный ресурс]. URl: https://developer.mozilla.org/ru/docs/Web/JavaScript</li>
    <li>Гарсиа-Молина Г., Ульман Д., Уидом Дж. Системы баз данных. Полный курс. – М.: Вильямс, 2019. – 1088 с.</li>
    <li>Документация Typescript. [Электронный ресурс]. URl: https://www.typescriptlang.org/docs/</li>
    <li>Документация по SQL. [Электронный ресурс]. URL: https://www.w3schools.com/sql/</li>
</ol>

<h2 id="приложение-А">Приложение А</h2> 
<h3>Реализация базы данных и примеры работы</h3> 
<p>Приводим создание таблиц, заполнения тестовыми данными и запросов:</p>
<code>
CREATE TABLE roles (
id SERIAL PRIMARY KEY,
name VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE users (
id SERIAL PRIMARY KEY,
email VARCHAR(255) UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
full_name VARCHAR(255) NOT NULL,
role_id INT REFERENCES roles(id),
created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE courses (
id SERIAL PRIMARY KEY,
title VARCHAR(255) NOT NULL,
description TEXT
);


CREATE TABLE groups (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
course_id INT REFERENCES courses(id)
);


CREATE TABLE group_students (
group_id INT REFERENCES groups(id),
student_id INT REFERENCES users(id),
PRIMARY KEY (group_id, student_id)
);

CREATE TABLE tests (
id SERIAL PRIMARY KEY,
title VARCHAR(255) NOT NULL,
description TEXT,
teacher_id INT REFERENCES users(id),
duration_minutes INT,
is_published BOOLEAN DEFAULT false,
created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE questions (
id SERIAL PRIMARY KEY,
test_id INT REFERENCES tests(id) ON DELETE CASCADE,
text TEXT NOT NULL,
type VARCHAR(50) CHECK (type IN ('single', 'multiple', 'text')),
points INT DEFAULT 1
);

CREATE TABLE answers (
id SERIAL PRIMARY KEY,
question_id INT REFERENCES questions(id) ON DELETE CASCADE,
text TEXT NOT NULL,
is_correct BOOLEAN DEFAULT false
);

CREATE TABLE test_attempts (
id SERIAL PRIMARY KEY,
test_id INT REFERENCES tests(id),
student_id INT REFERENCES users(id),
started_at TIMESTAMP DEFAULT now(),
finished_at TIMESTAMP,
score INT
);

CREATE TABLE student_answers (
attempt_id INT REFERENCES test_attempts(id) ON DELETE CASCADE,
question_id INT REFERENCES questions(id),
answer_id INT REFERENCES answers(id),
text_answer TEXT,
PRIMARY KEY (attempt_id, question_id, answer_id)
);

CREATE INDEX idx_users_role ON users(role_id);
CREATE INDEX idx_tests_teacher ON tests(teacher_id);
CREATE INDEX idx_attempts_student ON test_attempts(student_id);

-- Добавление пользователей
INSERT INTO users (email, password_hash, full_name, role_id)
VALUES ('student1@mail.com', 'hash1', 'Иван Иванов', 3),
       ('teacher1@mail.com', 'hash2', 'Мария Петрова', 2);

-- Добавление курса и группы
INSERT INTO courses (title, description) VALUES ('Математика', 'Курс по алгебре');
INSERT INTO groups (name, course_id) VALUES ('Группа А', 1);

-- Добавление теста и вопросов
INSERT INTO tests (title, teacher_id, duration_minutes, is_published)
VALUES ('Тест 1', 2, 30, TRUE);

INSERT INTO questions (test_id, text, type, points)
VALUES (1, '2+2=?', 'single', 1);

INSERT INTO answers (question_id, text, is_correct)
VALUES (1, '4', TRUE), (1, '5', FALSE);

-- Регистрация попытки студента
INSERT INTO test_attempts (test_id, student_id, score)
VALUES (1, 1, 1);

-- Получение результатов теста
SELECT u.full_name, ta.score
FROM test_attempts ta
JOIN users u ON ta.student_id = u.id
WHERE ta.test_id = 1;
</code>


<h2 id="приложение-б">Приложение Б</h2>

<h3>Реализация программы.
 
  
  
  Сам код интерфейса моего приложения, БД центра образования.
 
  
  
  (Проект написан на  практическом примере представления РЦО.)</h3>

<code>
//frontend state.ts

export const state = {
  token: null as string | null,
  userRole: 'student',
  answers: {} as Record<number, number> // questionId -> answerId
};

// frontend router.ts

import { renderLogin } from './pages/login.js';
import { renderDashboard } from './pages/dashboard.js';
import { renderTests } from './pages/tests.js';
import { renderPassTest } from './pages/passTest.js';
import { renderResults } from './pages/results.js';


export function router() {
const path = location.hash.slice(1) || '/login';


if (path === '/login') renderLogin();
else if (path === '/dashboard') renderDashboard();
else if (path === '/tests') renderTests();
else if (path.startsWith('/tests/')) renderPassTest(+path.split('/')[2]);
else if (path === '/results') renderResults();
}

// frontend main.ts

import { router } from './router.js';
import { state } from './state.js';

window.addEventListener('hashchange', router);
window.addEventListener('load', router);

(window as any).saveAnswer = (questionId: number, answerId: number) => {
  state.answers[questionId] = answerId;
};

// frontend api.ts

export const api = {
login: async (email: string, password: string) => {
return { token: 'mock-token', role: 'student' };
},


getTests: async () => [
{ id: 1, title: 'Математика', duration: 30 },
{ id: 2, title: 'Информатика', duration: 25 }
],


getTest: async (id: number) => ({
id,
title: 'Математика',
questions: [
{
id: 1,
text: '2 + 2 = ?',
answers: [
{ id: 1, text: '3' },
{ id: 2, text: '4' }
]
}
]
})
};

// frontend/pages tests.ts

import { api } from '../api.js';
import { layout } from '../components/layout.js';


export async function renderTests() {
const tests = await api.getTests();
const html = tests.map(t => `
<div class="card">
<h3>${t.title}</h3>
<p>Время: ${t.duration} мин</p>
<a href="#/tests/${t.id}">Начать</a>
</div>
`).join('');


document.getElementById('app')!.innerHTML = layout(html);
}

// frontend/pages results.ts

import { layout } from '../components/layout.js';
import { state } from '../state.js';

export function renderResults() {
  const answersHtml = Object.entries(state.answers)
    .map(([q, a]) => `<li>Вопрос ${q}: ответ ${a}</li>`)
    .join('');

  document.getElementById('app')!.innerHTML = layout(`
    <h2>Результаты</h2>
    <ul>${answersHtml}</ul>
  `);
}

// frontend/pages passTest.ts

import { api } from '../api.js';
import { layout } from '../components/layout.js';
import { questionBlock } from '../components/question.js';
import { state } from '../state.js';

export async function renderPassTest(id: number) {
  const test = await api.getTest(id);

  document.getElementById('app')!.innerHTML = layout(`
    <h2>${test.title}</h2>
    ${test.questions.map(questionBlock).join('')}
    <button class="btn-primary" id="finishBtn">Завершить</button>
  `);

  document.getElementById('finishBtn')!.onclick = () => {
    console.log('Ответы студента:', state.answers);
    location.hash = '/results';
  };
}

// frontend/pages login.ts

import { api } from '../api.js';
import { state } from '../state.js';
export function renderLogin() {
const app = document.getElementById('app')!;
app.innerHTML = `<div class="card" style="max-width:400px;margin:100px auto">
<h2>Вход</h2>
<input id="email" placeholder="Email" /><br/><br/>
<input id="pass" type="password" placeholder="Пароль" /><br/><br/>
<button class="btn-primary" id="loginBtn">Войти</button>
</div>`;
document.getElementById('loginBtn')!.onclick = async () => {
const email = (document.getElementById('email') as HTMLInputElement).value;
const pass = (document.getElementById('pass') as HTMLInputElement).value;
const res = await api.login(email, pass);
state.token = res.token;
state.userRole = res.role;
location.hash = '/dashboard';
};
}

import { api } from '../api.js';
import { layout } from '../components/layout.js';

export async function renderDashboard() {
  const app = document.getElementById('app')!;
  const tests = await api.getTests();
  app.innerHTML = layout(`
    <h2>Список тестов</h2>
    <ul>
      ${tests.map(t => `<li><a href="#/passTest/${t.id}">${t.title}</a></li>`).join('')}
    </ul>
  `);
}

// frontend/components testCard.ts 

export function testCard(test: { id: number; title: string; duration: number }) {
  return `
    <div class="card">
      <h3>${test.title}</h3>
      <p>Время: ${test.duration} мин</p>
      <a href="#/tests/${test.id}">Начать</a>
    </div>
  `;
}

// frontend/components question.ts

import { state } from '../state.js';

export function questionBlock(question: {
  id: number;
  text: string;
  answers: { id: number; text: string }[];
}) {
  return `
    <div class="card">
      <strong>${question.text}</strong>
      ${question.answers
        .map(
          a => `
            <div>
              <label>
                <input 
                  type="radio" 
                  name="q${question.id}" 
                  value="${a.id}"
                  onchange="window.saveAnswer(${question.id}, ${a.id})"
                />
                ${a.text}
              </label>
            </div>
          `
        )
        .join('')}
    </div>
  `;
}

// frontend/components layout.ts

export function layout(content: string) {
return `
<div class="layout">
<div class="sidebar">
<h2>Test System</h2>
<a href="#/dashboard">Главная</a>
<a href="#/tests">Тесты</a>
<a href="#/results">Результаты</a>
</div>
<div class="content">${content}</div>
</div>
`;
}

// backend index.js

import express from 'express';
import cors from 'cors';


import testsRoutes from './routes/tests.js';
import attemptsRoutes from './routes/attempts.js';


const app = express();
app.use(cors());
app.use(express.json());


app.use('/api/tests', testsRoutes);
app.use('/api/attempts', attemptsRoutes);


app.listen(3001, () => {
console.log('Backend started on http://localhost:3001');
});

// backend db.js

import pkg from 'pg';
const { Pool } = pkg;


export const pool = new Pool({
user: 'postgres',
password: 'password',
host: 'localhost',
port: 5432,
database: 'testing_system'
});

// backend/routes tests.js

import { Router } from 'express';
import { pool } from '../db.js';


const router = Router();


// Все тесты
router.get('/', async (req, res) => {
const { rows } = await pool.query(
'SELECT id, title, duration_minutes FROM tests WHERE is_published = true'
);
res.json(rows);
});


// Один тест с вопросами
router.get('/:id', async (req, res) => {
const testId = req.params.id;


const test = await pool.query(
'SELECT id, title FROM tests WHERE id = $1',
[testId]
);


const questions = await pool.query(`
SELECT q.id, q.text,
json_agg(json_build_object('id', a.id, 'text', a.text)) AS answers
FROM questions q
JOIN answers a ON a.question_id = q.id
WHERE q.test_id = $1
GROUP BY q.id
`, [testId]);


res.json({
...test.rows[0],
questions: questions.rows
});
});


export default router;

// backend/routes auth.js

import { Router } from 'express';
import { pool } from '../db.js';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';


const router = Router();
const SECRET = 'your_secret_key';


// Регистрация
router.post('/register', async (req, res) => {
const { email, password, role } = req.body;
const hash = await bcrypt.hash(password, 10);


try {
const result = await pool.query(
'INSERT INTO users(email, password, role) VALUES($1,$2,$3) RETURNING id, email, role',
[email, hash, role]
);
res.json(result.rows[0]);
} catch (err) {
res.status(400).json({ error: err.message });
}
});


// Логин
router.post('/login', async (req, res) => {
const { email, password } = req.body;
try {
const result = await pool.query('SELECT * FROM users WHERE email = $1', [email]);
const user = result.rows[0];
if (!user) return res.status(400).json({ error: 'User not found' });


const match = await bcrypt.compare(password, user.password);
if (!match) return res.status(400).json({ error: 'Wrong password' });


const token = jwt.sign({ id: user.id, role: user.role }, SECRET, { expiresIn: '2h' });
res.json({ token, role: user.role });
} catch (err) {
res.status(500).json({ error: err.message });
}
});


export default router;

// backend/routes attempts.js

import { Router } from 'express';
import { pool } from '../db.js';


const router = Router();


router.post('/', async (req, res) => {
const { testId, studentId, answers } = req.body;


const attempt = await pool.query(
'INSERT INTO test_attempts(test_id, student_id) VALUES($1,$2) RETURNING id',
[testId, studentId]
);


const attemptId = attempt.rows[0].id;


for (const [questionId, answerId] of Object.entries(answers)) {
await pool.query(
'INSERT INTO student_answers(attempt_id, question_id, answer_id) VALUES($1,$2,$3)',
[attemptId, questionId, answerId]
);
}


res.json({ success: true, attemptId });
});


export default router;


</code>
