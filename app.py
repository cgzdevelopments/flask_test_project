from flask import Flask, render_template
from services.db.db import PyPostgreSQL
from routes import student_routes, course_routes, professor_routes

app = Flask(__name__)

app.register_blueprint(student_routes.bp)
# app.register_blueprint(course_routes.bp)
# app.register_blueprint(professor_routes.bp)

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
    students = db.raw((
        "select st.*,"
        "(select count(id) from students_courses) as courses_count"
        "from students st"
    ))
    # students = db.raw("select * from students")
    return render_template('index.html', students=students)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
