from flask import Flask, request, render_template, redirect, url_for, current_app
from services.db.db import PyPostgreSQL

app = Flask(__name__)

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

@app.route('/') 
def index():
    # students = db.raw("""
    #     SELECT s.*, c.*, sc.*
    #     FROM students AS s
    #     JOIN students_courses AS sc ON s.id = sc.student_id
    #     JOIN courses AS c ON sc.course_id = c.id
    # """)
    # print(students)
    students = db.raw("""select * from students""")
    return render_template('index.html', students=students)

@app.route('/students/create', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/students/store', methods=['POST'])
def store():
    db.raw(
        query = "insert into students (full_name, age, identification) values (%s, %s, %s)",
        params = (request.form["name"], request.form["age"], request.form["identification"]),
        returning_results=False
    )
    return redirect(url_for('index'))

@app.route('/students/show/<id>', methods=['GET'])
def show(id: int):
        student = db.raw(f"select * from students where id = {id} limit 1")[0]
        return render_template('show.html', student=student)

@app.route('/students/edit/<id>', methods=['GET'])
def edit(id: int):
        student = db.raw(f"select * from students where id = {id} limit 1")[0]
        current_app.logger.debug(student)

        return render_template('edit.html', student=student)

@app.route('/students/update/<id>', methods=['POST'])
def update(id: int):
    current_app.logger.debug(request.form)
    db.raw(
        "update students set full_name = %s, age = %s, identification = %s where id = %s", 
        params = (request.form["full_name"], request.form["age"], request.form["identification"], id),
        returning_results=False
    )
    return redirect(url_for('index'))
    

@app.route('/students/delete/<id>', methods=['GET'])
def delete(id: int):
    db.raw(f"delete from students where id = {id}", returning_results=False)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
