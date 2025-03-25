CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    identification VARCHAR(10),
    age INT
);

CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
    professor_id INT,
    FOREIGN KEY (professor_id) REFERENCES professors (id)
);

CREATE TABLE IF NOT EXISTS students_courses (
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (course_id) REFERENCES courses (id)
);

CREATE TABLE IF NOT EXISTS professors (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    identification VARCHAR(10),
    age INT
);


