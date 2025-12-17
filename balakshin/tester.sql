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