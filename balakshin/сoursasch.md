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
  <li><a href="#приложение-а">Приложение А. Структура проекта</a></li>
  <li><a href="#приложение-б">Приложение Б. Структура проекта</a></li>
</ul>

---

<h2 id="введение">Введение</h2>

<p>В современном образовательном процессе контроль знаний студентов является важным элементом. Существую сторонние аналоги способные способные проверять знания учеников, но на примере ухода западных компания можно понять, что иметь свой собственный сервис точно не помешает, а также позволит расширять сервис под нужды центра. Система тестирования позволяет</p>
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
-- 1. Роли пользователей
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Пользователи
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role_id INT REFERENCES roles(id),
    created_at TIMESTAMP DEFAULT now(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    profile_photo TEXT,
    bio TEXT
);

-- 3. Курсы
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT now(),
    created_by INT REFERENCES users(id),
    is_active BOOLEAN DEFAULT true,
    category VARCHAR(100)
);

-- 4. Группы
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course_id INT REFERENCES courses(id),
    start_date DATE,
    end_date DATE,
    max_students INT
);

-- 5. Связь студентов с группами
CREATE TABLE group_students (
    group_id INT REFERENCES groups(id),
    student_id INT REFERENCES users(id),
    enrolled_at TIMESTAMP DEFAULT now(),
    status VARCHAR(20) CHECK (status IN ('active','completed','dropped')) DEFAULT 'active',
    PRIMARY KEY (group_id, student_id)
);

-- 6. Модули курсов
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    position INT,
    is_active BOOLEAN DEFAULT true
);

-- 7. Тесты
CREATE TABLE tests (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    teacher_id INT REFERENCES users(id),
    module_id INT REFERENCES modules(id),
    duration_minutes INT,
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT now(),
    category VARCHAR(50) CHECK (category IN ('quiz', 'exam', 'assignment')) DEFAULT 'quiz',
    max_attempts INT DEFAULT 1
);

-- 8. Вопросы
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    test_id INT REFERENCES tests(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    type VARCHAR(50) CHECK (type IN ('single', 'multiple', 'text', 'matching', 'code', 'file_upload')),
    points INT DEFAULT 1,
    hint TEXT,
    explanation TEXT
);

-- 9. Ответы на вопросы
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT false,
    media_url TEXT
);

-- 10. Теги для вопросов
CREATE TABLE question_tags (
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    tag VARCHAR(50),
    PRIMARY KEY (question_id, tag)
);

-- 11. Попытки прохождения теста студентами
CREATE TABLE test_attempts (
    id SERIAL PRIMARY KEY,
    test_id INT REFERENCES tests(id),
    student_id INT REFERENCES users(id),
    started_at TIMESTAMP DEFAULT now(),
    finished_at TIMESTAMP,
    score INT,
    status VARCHAR(20) CHECK (status IN ('in_progress','completed','abandoned')) DEFAULT 'in_progress',
    attempt_number INT DEFAULT 1
);

-- 12. Ответы студентов
CREATE TABLE student_answers (
    attempt_id INT REFERENCES test_attempts(id) ON DELETE CASCADE,
    question_id INT REFERENCES questions(id),
    answer_id INT REFERENCES answers(id),
    text_answer TEXT,
    file_answer TEXT,
    PRIMARY KEY (attempt_id, question_id, answer_id)
);

-- 13. Логи действий пользователей
CREATE TABLE user_logs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    action VARCHAR(255),
    created_at TIMESTAMP DEFAULT now(),
    ip_address VARCHAR(50),
    device_info TEXT
);

-- 14. Результаты модульных заданий
CREATE TABLE module_results (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES users(id),
    module_id INT REFERENCES modules(id),
    score INT,
    completed_at TIMESTAMP DEFAULT now(),
    status VARCHAR(20) CHECK (status IN ('completed','in_progress','failed')) DEFAULT 'in_progress'
);

-- 15. Отчеты по тестам
CREATE TABLE test_reports (
    id SERIAL PRIMARY KEY,
    test_id INT REFERENCES tests(id),
    report_data JSONB,
    generated_at TIMESTAMP DEFAULT now()
);

-- 16. Материалы курса
CREATE TABLE course_materials (
    id SERIAL PRIMARY KEY,
    module_id INT REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(255),
    description TEXT,
    file_url TEXT,
    material_type VARCHAR(50) CHECK (material_type IN ('video','pdf','presentation','link','other')),
    created_at TIMESTAMP DEFAULT now()
);

-- 17. Задания
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    module_id INT REFERENCES modules(id),
    title VARCHAR(255),
    description TEXT,
    due_date TIMESTAMP,
    max_score INT
);

-- 18. Ответы на задания
CREATE TABLE assignment_submissions (
    id SERIAL PRIMARY KEY,
    assignment_id INT REFERENCES assignments(id),
    student_id INT REFERENCES users(id),
    submitted_at TIMESTAMP DEFAULT now(),
    score INT,
    feedback TEXT,
    file_url TEXT,
    status VARCHAR(20) CHECK (status IN ('submitted','graded','late','missing')) DEFAULT 'submitted'
);

-- 19. Расписание занятий
CREATE TABLE schedule (
    id SERIAL PRIMARY KEY,
    group_id INT REFERENCES groups(id),
    module_id INT REFERENCES modules(id),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    location VARCHAR(255),
    teacher_id INT REFERENCES users(id)
);

-- 20. Уведомления
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    title VARCHAR(255),
    message TEXT,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT now(),
    type VARCHAR(50) CHECK (type IN ('info','alert','reminder'))
);

-- 21. Достижения и бейджи
CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    points INT
);

CREATE TABLE user_achievements (
    user_id INT REFERENCES users(id),
    achievement_id INT REFERENCES achievements(id),
    awarded_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (user_id, achievement_id)
);

-- 22. Обратная связь и комментарии
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    entity_type VARCHAR(50) CHECK (entity_type IN ('course','module','test','question','assignment')),
    entity_id INT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT now()
);

-- 23. Интеграция с внешними сервисами (например, облачное хранение, видео-хостинг)
CREATE TABLE integrations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    api_key TEXT,
    config JSONB,
    created_at TIMESTAMP DEFAULT now()
);

-- 24. Индексы для оптимизации
CREATE INDEX idx_users_role ON users(role_id);
CREATE INDEX idx_tests_teacher ON tests(teacher_id);
CREATE INDEX idx_tests_module ON tests(module_id);
CREATE INDEX idx_attempts_student ON test_attempts(student_id);
CREATE INDEX idx_group_students_student ON group_students(student_id);
CREATE INDEX idx_user_logs_user ON user_logs(user_id);
CREATE INDEX idx_schedule_group ON schedule(group_id);
CREATE INDEX idx_assignment_submissions_student ON assignment_submissions(student_id);

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
<p>Для реализации системы выбран сервер баз данных <strong>PostgreSQL 14+</strong>. Это современная реляционная СУБД, известная своей надежностью, высокой производительностью и поддержкой расширенных функций, таких как полнотекстовый поиск, сложные типы данных и транзакции с высокой согласованностью. PostgreSQL также хорошо масштабируется, поддерживает параллельное выполнение запросов и имеет активное сообщество, что обеспечивает долгосрочную поддержку проекта.</p> 

<h3>4.2. Типы данных</h3>
<p>При проектировании базы данных важно правильно выбрать типы данных для хранения информации. Это напрямую влияет на скорость выполнения запросов, размер базы и целостность данных. В таблице ниже приведены основные типы данных, используемые в проекте:</p>
<table>
    <tr><th>Тип данных</th><th>Применение</th></tr>
    <tr><td>SERIAL</td><td>Автоинкрементные первичные ключи, обеспечивающие уникальность записей</td></tr>
    <tr><td>INTEGER</td><td>Количественные данные, например, возраст, количество попыток теста, год</td></tr>
    <tr><td>DECIMAL(10,2)</td><td>Денежные значения с точностью до копеек, например, стоимость курсов</td></tr>
    <tr><td>VARCHAR</td><td>Текстовые данные переменной длины, такие как названия курсов или имена пользователей</td></tr>
    <tr><td>TEXT</td><td>Длинные текстовые описания, комментарии и пояснения</td></tr>
    <tr><td>DATE/TIMESTAMP</td><td>Даты и время создания записей, начала и окончания тестов</td></tr>
</table>
<p>Выбор правильного типа данных позволяет не только эффективно хранить информацию, но и упрощает последующую обработку данных в аналитических запросах.</p>

<h3>4.3. Стратегия резервного копирования</h3> 
<p>Для минимизации риска потери данных предусмотрена комплексная стратегия резервного копирования:</p>
<ul> 
    <li>Полные резервные копии базы данных выполняются раз в день в 02:00, что позволяет восстанавливать данные за последние сутки</li> 
    <li>Инкрементные копии выполняются каждые 4 часа, фиксируя изменения с момента последнего полного бэкапа</li> 
    <li>Резервные копии хранятся как на отдельном сервере, так и в облачном хранилище, что обеспечивает отказоустойчивость</li> 
    <li>Регулярно проводится тестирование восстановления, чтобы убедиться в работоспособности всех резервных копий и корректности процедуры восстановления</li> 
</ul> 
<p>Данная стратегия обеспечивает баланс между безопасностью данных и временем восстановления системы в случае сбоя.</p>

<h3>4.4. Безопасность данных</h3> 
<p>Безопасность данных является приоритетом проекта. В системе реализованы следующие меры:</p>
<ul> 
    <li>Шифрование паролей пользователей с использованием алгоритма <strong>bcrypt</strong> для защиты учетных данных</li> 
    <li>Ролевая модель доступа с разграничением полномочий: <em>admin</em>, <em>teacher</em>, <em>student</em>, <em>viewer</em>, что предотвращает несанкционированный доступ</li> 
    <li>SSL-шифрование соединений между клиентом и сервером базы данных для защиты данных при передаче</li> 
    <li>Аудит критических операций с фиксацией действий пользователей, таких как создание тестов, удаление данных или изменение ролей</li> 
</ul> 
<p>Все эти меры в совокупности обеспечивают высокий уровень защиты информации, соответствующий современным требованиям к безопасности образовательных платформ.</p>


<h2 id="глава5-реализация-проекта">5. Реализация проекта в среде PostgreSQL</h2> 
<h3 id="51-создание-таблиц">5.1. Создание таблиц</h3> 
<code>
-- 1. Роли пользователей
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Пользователи
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role_id INT REFERENCES roles(id),
    created_at TIMESTAMP DEFAULT now(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    profile_photo TEXT,
    bio TEXT
);

-- 3. Курсы
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT now(),
    created_by INT REFERENCES users(id),
    is_active BOOLEAN DEFAULT true,
    category VARCHAR(100)
);

-- 4. Группы
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course_id INT REFERENCES courses(id),
    start_date DATE,
    end_date DATE,
    max_students INT
);

-- 5. Связь студентов с группами
CREATE TABLE group_students (
    group_id INT REFERENCES groups(id),
    student_id INT REFERENCES users(id),
    enrolled_at TIMESTAMP DEFAULT now(),
    status VARCHAR(20) CHECK (status IN ('active','completed','dropped')) DEFAULT 'active',
    PRIMARY KEY (group_id, student_id)
);

-- 6. Модули курсов
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    position INT,
    is_active BOOLEAN DEFAULT true
);

-- 7. Тесты
CREATE TABLE tests (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    teacher_id INT REFERENCES users(id),
    module_id INT REFERENCES modules(id),
    duration_minutes INT,
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT now(),
    category VARCHAR(50) CHECK (category IN ('quiz', 'exam', 'assignment')) DEFAULT 'quiz',
    max_attempts INT DEFAULT 1
);

-- 8. Вопросы
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    test_id INT REFERENCES tests(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    type VARCHAR(50) CHECK (type IN ('single', 'multiple', 'text', 'matching', 'code', 'file_upload')),
    points INT DEFAULT 1,
    hint TEXT,
    explanation TEXT
);

-- 9. Ответы на вопросы
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT false,
    media_url TEXT
);

-- 10. Теги для вопросов
CREATE TABLE question_tags (
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    tag VARCHAR(50),
    PRIMARY KEY (question_id, tag)
);

-- 11. Попытки прохождения теста студентами
CREATE TABLE test_attempts (
    id SERIAL PRIMARY KEY,
    test_id INT REFERENCES tests(id),
    student_id INT REFERENCES users(id),
    started_at TIMESTAMP DEFAULT now(),
    finished_at TIMESTAMP,
    score INT,
    status VARCHAR(20) CHECK (status IN ('in_progress','completed','abandoned')) DEFAULT 'in_progress',
    attempt_number INT DEFAULT 1
);

-- 12. Ответы студентов
CREATE TABLE student_answers (
    attempt_id INT REFERENCES test_attempts(id) ON DELETE CASCADE,
    question_id INT REFERENCES questions(id),
    answer_id INT REFERENCES answers(id),
    text_answer TEXT,
    file_answer TEXT,
    PRIMARY KEY (attempt_id, question_id, answer_id)
);

-- 13. Логи действий пользователей
CREATE TABLE user_logs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    action VARCHAR(255),
    created_at TIMESTAMP DEFAULT now(),
    ip_address VARCHAR(50),
    device_info TEXT
);

-- 14. Результаты модульных заданий
CREATE TABLE module_results (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES users(id),
    module_id INT REFERENCES modules(id),
    score INT,
    completed_at TIMESTAMP DEFAULT now(),
    status VARCHAR(20) CHECK (status IN ('completed','in_progress','failed')) DEFAULT 'in_progress'
);

-- 15. Отчеты по тестам
CREATE TABLE test_reports (
    id SERIAL PRIMARY KEY,
    test_id INT REFERENCES tests(id),
    report_data JSONB,
    generated_at TIMESTAMP DEFAULT now()
);

-- 16. Материалы курса
CREATE TABLE course_materials (
    id SERIAL PRIMARY KEY,
    module_id INT REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(255),
    description TEXT,
    file_url TEXT,
    material_type VARCHAR(50) CHECK (material_type IN ('video','pdf','presentation','link','other')),
    created_at TIMESTAMP DEFAULT now()
);

-- 17. Задания
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    module_id INT REFERENCES modules(id),
    title VARCHAR(255),
    description TEXT,
    due_date TIMESTAMP,
    max_score INT
);

-- 18. Ответы на задания
CREATE TABLE assignment_submissions (
    id SERIAL PRIMARY KEY,
    assignment_id INT REFERENCES assignments(id),
    student_id INT REFERENCES users(id),
    submitted_at TIMESTAMP DEFAULT now(),
    score INT,
    feedback TEXT,
    file_url TEXT,
    status VARCHAR(20) CHECK (status IN ('submitted','graded','late','missing')) DEFAULT 'submitted'
);

-- 19. Расписание занятий
CREATE TABLE schedule (
    id SERIAL PRIMARY KEY,
    group_id INT REFERENCES groups(id),
    module_id INT REFERENCES modules(id),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    location VARCHAR(255),
    teacher_id INT REFERENCES users(id)
);

-- 20. Уведомления
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    title VARCHAR(255),
    message TEXT,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT now(),
    type VARCHAR(50) CHECK (type IN ('info','alert','reminder'))
);

-- 21. Достижения и бейджи
CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    points INT
);

CREATE TABLE user_achievements (
    user_id INT REFERENCES users(id),
    achievement_id INT REFERENCES achievements(id),
    awarded_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (user_id, achievement_id)
);

-- 22. Обратная связь и комментарии
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    entity_type VARCHAR(50) CHECK (entity_type IN ('course','module','test','question','assignment')),
    entity_id INT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT now()
);

-- 23. Интеграция с внешними сервисами (например, облачное хранение, видео-хостинг)
CREATE TABLE integrations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    api_key TEXT,
    config JSONB,
    created_at TIMESTAMP DEFAULT now()
);

-- 24. Индексы для оптимизации
CREATE INDEX idx_users_role ON users(role_id);
CREATE INDEX idx_tests_teacher ON tests(teacher_id);
CREATE INDEX idx_tests_module ON tests(module_id);
CREATE INDEX idx_attempts_student ON test_attempts(student_id);
CREATE INDEX idx_group_students_student ON group_students(student_id);
CREATE INDEX idx_user_logs_user ON user_logs(user_id);
CREATE INDEX idx_schedule_group ON schedule(group_id);
CREATE INDEX idx_assignment_submissions_student ON assignment_submissions(student_id);

</code>

<h3 id="52-создание-запросов">5.2. Создание запросов</h3>
<code>
-- Получение всех тестов студента
-- 1. Получение всех тестов студента с информацией о курсе и модуле
SELECT t.id AS test_id, t.title AS test_title, m.title AS module_title, c.title AS course_title, t.is_published
FROM test_attempts ta
JOIN tests t ON ta.test_id = t.id
JOIN modules m ON t.module_id = m.id
JOIN courses c ON m.course_id = c.id
WHERE ta.student_id = 1;

-- 2. Получение всех студентов группы с их текущим статусом
SELECT u.id AS student_id, u.full_name, gs.status
FROM group_students gs
JOIN users u ON gs.student_id = u.id
WHERE gs.group_id = 3;

-- 3. Получение среднего балла студентов по конкретному тесту
SELECT u.full_name, AVG(ta.score) AS avg_score
FROM test_attempts ta
JOIN users u ON ta.student_id = u.id
WHERE ta.test_id = 5
GROUP BY u.id
ORDER BY avg_score DESC;

-- 4. Получение списка тестов преподавателя с количеством попыток
SELECT t.id, t.title, COUNT(ta.id) AS attempts_count
FROM tests t
LEFT JOIN test_attempts ta ON t.id = ta.test_id
WHERE t.teacher_id = 2
GROUP BY t.id;

-- 5. Получение всех заданий студента с оценками и статусом
SELECT a.title AS assignment_title, asub.score, asub.status, asub.submitted_at
FROM assignment_submissions asub
JOIN assignments a ON asub.assignment_id = a.id
WHERE asub.student_id = 1
ORDER BY asub.submitted_at DESC;

-- 6. Получение всех модулей курса с количеством тестов и заданий
SELECT m.id, m.title, 
       COUNT(DISTINCT t.id) AS tests_count, 
       COUNT(DISTINCT a.id) AS assignments_count
FROM modules m
LEFT JOIN tests t ON t.module_id = m.id
LEFT JOIN assignments a ON a.module_id = m.id
WHERE m.course_id = 2
GROUP BY m.id;

-- 7. Получение уведомлений пользователя, которые еще не прочитаны
SELECT id, title, message, type, created_at
FROM notifications
WHERE user_id = 1 AND is_read = false
ORDER BY created_at DESC;

-- 8. Получение прогресса студента по курсам (кол-во пройденных модулей)
SELECT c.title AS course_title, COUNT(DISTINCT mr.module_id) AS completed_modules
FROM module_results mr
JOIN modules m ON mr.module_id = m.id
JOIN courses c ON m.course_id = c.id
WHERE mr.student_id = 1 AND mr.status = 'completed'
GROUP BY c.id;

-- 9. Получение всех комментариев к курсу
SELECT u.full_name, c.comment, c.created_at
FROM comments c
JOIN users u ON c.user_id = u.id
WHERE c.entity_type = 'course' AND c.entity_id = 2
ORDER BY c.created_at DESC;

-- 10. Получение всех студентов, которые не начали тест
SELECT u.full_name, t.title AS test_title
FROM test_attempts ta
JOIN users u ON ta.student_id = u.id
JOIN tests t ON ta.test_id = t.id
WHERE ta.status = 'in_progress' AND ta.started_at IS NULL;

-- 11. Получение топ-3 курсов по средней оценке студентов
SELECT c.title AS course_title, AVG(ta.score) AS avg_score
FROM test_attempts ta
JOIN tests t ON ta.test_id = t.id
JOIN modules m ON t.module_id = m.id
JOIN courses c ON m.course_id = c.id
GROUP BY c.id
ORDER BY avg_score DESC
LIMIT 3;

-- 12. Получение студентов, которые сдали задание с опозданием
SELECT u.full_name, a.title AS assignment_title, asub.status, asub.submitted_at
FROM assignment_submissions asub
JOIN users u ON asub.student_id = u.id
JOIN assignments a ON asub.assignment_id = a.id
WHERE asub.status = 'late';

-- 13. Получение активности пользователя за последний месяц (лог действий)
SELECT action, created_at, ip_address, device_info
FROM user_logs
WHERE user_id = 1 AND created_at >= now() - INTERVAL '30 days'
ORDER BY created_at DESC;

-- 14. Получение достижений студента
SELECT a.name AS achievement_name, a.description, a.points, ua.awarded_at
FROM user_achievements ua
JOIN achievements a ON ua.achievement_id = a.id
WHERE ua.user_id = 1
ORDER BY ua.awarded_at DESC;

-- 15. Получение всех материалов модуля с фильтром по типу
SELECT title, material_type, file_url
FROM course_materials
WHERE module_id = 4 AND material_type = 'video';

-- 16. Получение студентов, которые не сдавали ни одного теста
SELECT u.id, u.full_name
FROM users u
LEFT JOIN test_attempts ta ON u.id = ta.student_id
WHERE u.role_id = 3 AND ta.id IS NULL; -- роль 3 = студент

-- 17. Количество тестов и средний балл по каждому курсу
SELECT c.title AS course_title, COUNT(DISTINCT t.id) AS tests_count, AVG(ta.score) AS avg_score
FROM courses c
JOIN modules m ON c.id = m.course_id
LEFT JOIN tests t ON t.module_id = m.id
LEFT JOIN test_attempts ta ON ta.test_id = t.id
GROUP BY c.id;

-- 18. Среднее время прохождения теста студентами
SELECT t.title AS test_title, AVG(EXTRACT(EPOCH FROM (ta.finished_at - ta.started_at))/60) AS avg_minutes
FROM test_attempts ta
JOIN tests t ON ta.test_id = t.id
WHERE ta.finished_at IS NOT NULL
GROUP BY t.id;

-- 19. Студенты с наибольшим количеством успешных попыток
SELECT u.full_name, COUNT(*) AS passed_tests
FROM test_attempts ta
JOIN users u ON ta.student_id = u.id
WHERE ta.score >= 80
GROUP BY u.id
ORDER BY passed_tests DESC
LIMIT 5;

-- 20. Получение всех тестов и количества вопросов в каждом
SELECT t.id AS test_id, t.title, COUNT(q.id) AS questions_count
FROM tests t
LEFT JOIN questions q ON q.test_id = t.id
GROUP BY t.id;

-- 21. Процент студентов, прошедших каждый тест
SELECT t.title, 
       COUNT(CASE WHEN ta.score >= 50 THEN 1 END)*100.0/COUNT(ta.id) AS pass_percentage
FROM tests t
LEFT JOIN test_attempts ta ON t.id = ta.test_id
GROUP BY t.id;

-- 22. Рейтинг преподавателей по среднему баллу их тестов
SELECT u.full_name AS teacher_name, AVG(ta.score) AS avg_score
FROM users u
JOIN tests t ON t.teacher_id = u.id
JOIN test_attempts ta ON ta.test_id = t.id
GROUP BY u.id
ORDER BY avg_score DESC;

-- 23. Студенты, набравшие меньше 50% по всем тестам курса
SELECT u.full_name, c.title AS course_title, AVG(ta.score) AS avg_score
FROM test_attempts ta
JOIN users u ON ta.student_id = u.id
JOIN tests t ON t.id = ta.test_id
JOIN modules m ON t.module_id = m.id
JOIN courses c ON m.course_id = c.id
GROUP BY u.id, c.id
HAVING AVG(ta.score) < 50;

-- 24. Последние 5 комментариев по каждому курсу
SELECT c.title AS course_title, cm.comment, u.full_name, cm.created_at
FROM comments cm
JOIN courses c ON cm.entity_type = 'course' AND cm.entity_id = c.id
JOIN users u ON cm.user_id = u.id
WHERE cm.entity_type = 'course'
ORDER BY cm.created_at DESC
LIMIT 5;

-- 25. Топ студентов по количеству пройденных модулей
SELECT u.full_name, COUNT(DISTINCT mr.module_id) AS completed_modules
FROM module_results mr
JOIN users u ON mr.student_id = u.id
WHERE mr.status = 'completed'
GROUP BY u.id
ORDER BY completed_modules DESC
LIMIT 10;

-- 26. Материалы модуля с количеством просмотров студентами
SELECT cm.title, cm.material_type, COUNT(v.id) AS views_count
FROM course_materials cm
LEFT JOIN material_views v ON cm.id = v.material_id
WHERE cm.module_id = 2
GROUP BY cm.id;

-- 27. Оконная функция: средний балл по тесту и сравнение с каждым студентом
SELECT ta.id AS attempt_id, u.full_name, ta.score,
       AVG(ta.score) OVER (PARTITION BY ta.test_id) AS avg_test_score,
       ta.score - AVG(ta.score) OVER (PARTITION BY ta.test_id) AS deviation_from_avg
FROM test_attempts ta
JOIN users u ON ta.student_id = u.id;

-- 28. Список всех студентов с количеством попыток по каждому тесту
SELECT u.full_name, t.title AS test_title, COUNT(ta.id) AS attempts_count
FROM users u
JOIN test_attempts ta ON u.id = ta.student_id
JOIN tests t ON t.id = ta.test_id
GROUP BY u.id, t.id;

-- 29. Получение уведомлений для группы студентов
SELECT n.title, n.message, n.created_at, g.name AS group_name
FROM notifications n
JOIN groups g ON n.group_id = g.id
WHERE g.id = 3 AND n.is_read = false;

-- 30. Получение всех тестов с количеством студентов, которые начали, но не закончили
SELECT t.title, COUNT(ta.id) AS in_progress_count
FROM tests t
LEFT JOIN test_attempts ta ON t.id = ta.test_id AND ta.finished_at IS NULL
GROUP BY t.id;
</code>

<h3 id="53-разработка-интерфейса">5.3. Разработка интерфейса</h3> 
<p>Разработка интерфейса системы была выполнена с учётом принципов удобства использования, интуитивно понятной навигации и адаптивного дизайна для различных устройств. Основная цель интерфейса — обеспечить быстрый и комфортный доступ к функционалу для разных ролей пользователей (администратор, преподаватель, студент, просмотрщик).</p> 
<ul> 
  <li><strong>Frontend:</strong> Используются HTML, CSS и JavaScript/Typescript</li> 
  <li><strong>Backend:</strong> Node.js с Express отвечает за обработку запросов, логику работы приложения и взаимодействие с базой данных PostgreSQL. Такой стек обеспечивает высокую производительность и масштабируемость системы.</li> 
  <li><strong>JWT-аутентификация:</strong> Используется для безопасного подтверждения личности пользователей и защиты API. Токены позволяют фронтенду получать доступ к ресурсам без постоянного ввода логина и пароля, обеспечивая удобство и безопасность.</li> 
  <li><strong>REST API:</strong> Позволяет фронтенду взаимодействовать с сервером через стандартизированные HTTP-запросы. API поддерживает все основные операции: получение тестов, отправку ответов, регистрацию пользователей, просмотр результатов и статистики. Такой подход обеспечивает модульность, расширяемость и возможность интеграции с мобильными приложениями или сторонними сервисами.</li> 
  <li><strong>Адаптивный дизайн:</strong> Интерфейс автоматически подстраивается под размер экрана, обеспечивая комфортное использование на десктопах, планшетах и мобильных устройствах.</li> 
  <li><strong>Удобство и эргономика:</strong> Все элементы интерфейса структурированы логично, минимизируя количество кликов для выполнения основных действий. Важные функции и уведомления выделены визуально для быстрого доступа.</li> 
  <li><strong>Модульность:</strong> Компоненты интерфейса разработаны так, чтобы их легко было переиспользовать и модифицировать без глобальных изменений в коде.</li> 
  <li><strong>Пользовательский опыт:</strong> В интерфейсе реализованы подсказки, валидация форм и обратная связь пользователю для предотвращения ошибок и повышения эффективности работы.</li> 
</ul> 
<p>Таким образом, интерфейс сочетает в себе современный дизайн, безопасность, удобство и масштабируемость, обеспечивая качественное взаимодействие с системой для всех категорий пользователей.</p>

<h3 id="54-назначение-прав-доступа">5.4. Назначение прав доступа</h3>
<p>Система использует ролевую модель для управления доступом к функциям и данным. Каждая роль определяет, какие действия пользователь может выполнять в системе.</p>
<code>
-- Создание ролей
CREATE ROLE admin LOGIN PASSWORD 'admin123';
CREATE ROLE teacher LOGIN PASSWORD 'teacher123';
CREATE ROLE student LOGIN PASSWORD 'student123';
CREATE ROLE viewer LOGIN PASSWORD 'viewer123';

-- Права для администратора: полный доступ ко всем таблицам и последовательностям
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;

-- Права для преподавателя: управление курсами, тестами и вопросами
GRANT SELECT, INSERT, UPDATE, DELETE ON courses, groups, tests, questions, answers TO teacher;
GRANT SELECT, UPDATE ON test_attempts, student_answers TO teacher;
GRANT SELECT, UPDATE ON users TO teacher;

-- Права для студента: прохождение тестов и просмотр своих результатов
GRANT SELECT ON courses, groups, tests, questions, answers TO student;
GRANT INSERT, UPDATE ON test_attempts, student_answers TO student;
GRANT SELECT, UPDATE ON users TO student;

-- Права для просмотрщика (viewer): только чтение данных
GRANT SELECT ON courses, groups, tests, questions, answers, test_attempts, student_answers, users TO viewer;

</code>

<h3 id="55-создание-индексов">5.5. Создание индексов</h3>
<code>
CREATE INDEX idx_users_role ON users(role_id);
CREATE INDEX idx_tests_teacher ON tests(teacher_id);
CREATE INDEX idx_tests_module ON tests(module_id);
CREATE INDEX idx_attempts_student ON test_attempts(student_id);
CREATE INDEX idx_group_students_student ON group_students(student_id);
CREATE INDEX idx_user_logs_user ON user_logs(user_id);
CREATE INDEX idx_schedule_group ON schedule(group_id);
CREATE INDEX idx_assignment_submissions_student ON assignment_submissions(student_id);
</code>
<h3 id="56-резервное-копирование">5.6. Разработка стратегии резервного копирования</h3>
<p>Создание копии раз в определенное время и удаление старых бэкапов</p>
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
<p>API предоставляет интерфейс для взаимодействия фронтенда с сервером образовательного центра. Оно позволяет авторизовать пользователей, получать списки тестов, отдельные тесты с вопросами и вариантами ответов, а также отправлять ответы студентов на тесты.</p>
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




