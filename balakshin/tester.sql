-- =========================================
-- БАЗА ДАННЫХ: Онлайн-тестирование
-- =========================================

-- ---------- Роли пользователей ----------
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

-- ---------- Пользователи ----------
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- ---------- Учебные группы ----------
CREATE TABLE study_groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- ---------- Пользователи в группах ----------
CREATE TABLE group_members (
    group_member_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES study_groups(group_id)
);

-- ---------- Курсы ----------
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    description TEXT,
    teacher_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(user_id)
);

-- ---------- Запись групп на курсы ----------
CREATE TABLE course_groups (
    course_group_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL,
    group_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (group_id) REFERENCES study_groups(group_id)
);

-- ---------- Тесты ----------
CREATE TABLE tests (
    test_id SERIAL PRIMARY KEY,
    test_name VARCHAR(150) NOT NULL,
    course_id INT NOT NULL,
    time_limit INT, -- минуты
    attempts_limit INT DEFAULT 1,
    pass_score INT, -- проходной балл
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- ---------- Категории вопросов ----------
CREATE TABLE question_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

-- ---------- Вопросы ----------
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    test_id INT NOT NULL,
    category_id INT,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL, -- single, multiple, text
    score INT DEFAULT 1,
    FOREIGN KEY (test_id) REFERENCES tests(test_id),
    FOREIGN KEY (category_id) REFERENCES question_categories(category_id)
);

-- ---------- Варианты ответов ----------
CREATE TABLE answers (
    answer_id SERIAL PRIMARY KEY,
    question_id INT NOT NULL,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);

-- ---------- Попытки прохождения тестов ----------
CREATE TABLE test_attempts (
    attempt_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    test_id INT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    total_score INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'in_progress', -- завершён, прерван
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (test_id) REFERENCES tests(test_id)
);

-- ---------- Ответы пользователя ----------
CREATE TABLE user_answers (
    user_answer_id SERIAL PRIMARY KEY,
    attempt_id INT NOT NULL,
    question_id INT NOT NULL,
    answer_id INT,
    answer_text TEXT, -- для текстовых вопросов
    FOREIGN KEY (attempt_id) REFERENCES test_attempts(attempt_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id),
    FOREIGN KEY (answer_id) REFERENCES answers(answer_id)
);

-- ---------- Итоговые результаты ----------
CREATE TABLE test_results (
    result_id SERIAL PRIMARY KEY,
    attempt_id INT NOT NULL,
    passed BOOLEAN,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (attempt_id) REFERENCES test_attempts(attempt_id)
);

-- ---------- Логи действий ----------
CREATE TABLE system_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INT,
    action TEXT NOT NULL,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
