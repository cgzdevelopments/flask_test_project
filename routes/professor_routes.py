# routes/course_routes.py
from flask import Blueprint, request, render_template, redirect, url_for, current_app
from services.db.db import PyPostgreSQL

bp = Blueprint('professor', __name__, url_prefix='/professor')

# TODO: Add professor, course

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
def create_professor():
    return render_template('create.html')

@bp.route('/store', methods=['POST'])
def store_professor():
    db.raw(
        query = "insert into professor (full_name, age, identification) values (%s, %s, %s)",
        params = (request.form["name"], request.form["age"], request.form["identification"]),
        returning_results=False
    )
    return redirect(url_for('index'))

@bp.route('/show/<int:id>', methods=['GET'])
def show_professor(id: int):
        student = db.raw(f"select * from professor where id = {id} limit 1")[0]
        return render_template('show.html', student=student)

@bp.route('/edit/<int:id>', methods=['GET'])
def edit_professor(id: int):
        student = db.raw(f"select * from professor where id = {id} limit 1")[0]
        return render_template('edit.html', student=student)

@bp.route('/update/<int:id>', methods=['POST'])
def update_professor(id: int):
    current_app.logger.debug(request.form)
    db.raw(
        "update professor set full_name = %s, age = %s, identification = %s where id = %s", 
        params = (request.form["full_name"], request.form["age"], request.form["identification"], id),
        returning_results=False
    )
    return redirect(url_for('index'))
    

@bp.route('/delete/<int:id>', methods=['GET'])
def delete_professor(id: int):
    db.raw(f"delete from professor where id = {id}", returning_results=False)
    return redirect(url_for('index'))