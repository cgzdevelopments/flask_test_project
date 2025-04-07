# routes/course_routes.py
from flask import Blueprint, request, render_template, redirect, url_for, current_app
from services.db.db import PyPostgreSQL

bp = Blueprint('students', __name__, url_prefix='/students')

# Database configuration
db_config = {
    "database": "university",
    "user": "postgres",
    "password": "Admin1234*",
    "host": "db",
    "port": "5432"
}

# Initialize database connection
db = PyPostgreSQL(**db_config)
db.connect()

@bp.route('/create', methods=['GET'])
def create_student():
    available_courses: list = db.raw(query="select * from courses")
    return render_template('students/create.html', available_courses=available_courses)

@bp.route('/store', methods=['POST'])
def store_student():
    db.raw(
        query = "insert into students (full_name, age, identification) values (%s, %s, %s)",
        params = (request.form["name"], request.form["age"], request.form["identification"]),
        returning_results=False
    )

    for course_id in request.form.getlist("courses"):
        db.raw(
            query = "insert into students_courses (student_id, course_id) values ((select max(id) from students), %s)",
            params = (course_id),
            returning_results=False
        )

    return redirect(url_for('index'))

@bp.route('/show/<int:id>', methods=['GET'])
def show_student(id: int):
        student = db.raw(f"select * from students where id = {id}")[0]
        courses = db.raw(f"select * from courses where id in (select course_id from students_courses where student_id = {id})")
        return render_template('students/show.html', student=student, courses=courses)

@bp.route('/edit/<int:id>', methods=['GET'])
def edit_student(id: int):
        student = db.raw(f"select * from students where id = {id} limit 1")[0]
        courses = db.raw(f"select * from courses where id in (select course_id from students_courses where student_id = {id})")
        available_courses: list = db.raw(query="select * from courses")
        return render_template(
             'students/edit.html', 
             student=student, 
             courses=courses,
             available_courses=available_courses
        )

@bp.route('/update/<int:id>', methods=['POST'])
def update_student(id: int):
    db.raw(
        "update students set full_name = %s, age = %s, identification = %s where id = %s", 
        params = (request.form["full_name"], request.form["age"], request.form["identification"], id),
        returning_results=False
    )

    db.raw(
        f"delete from students_courses where student_id = {id}",
        returning_results=False
    )

    for course_id in request.form.getlist("courses"):
        db.raw(
            "insert into students_courses (student_id, course_id) values (%s, %s)",
            params = (id, request.form["course_id"]),
            returning_results=False
        )

    return redirect(url_for('index'))
    

@bp.route('/delete/<int:id>', methods=['GET'])
def delete_student(id: int):
    db.raw(f"delete from students_courses where student_id = {id}", returning_results=False)
    db.raw(f"delete from students where id = {id}", returning_results=False)
    return redirect(url_for('index'))