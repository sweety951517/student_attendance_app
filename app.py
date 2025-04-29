from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Attendance
import urllib.parse

app = Flask(__name__)  

app.secret_key = 'super_secret_key'

# Replace with your actual values:
DB_USERNAME = "admin.user"
DB_PASSWORD = "Sushma@951517"
DB_SERVER = "student-attendance-server.database.windows.net"
DB_NAME = "student_attendance"

# URL encode the password
DB_PASSWORD = urllib.parse.quote_plus(DB_PASSWORD)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:1433/{DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

with app.app_context():
    db.create_all()

# ----------------- ROUTES ------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        name = request.form['name']

        session['role'] = role
        session['name'] = name

        # Check if user exists, if not, add to DB
        user = User.query.filter_by(name=name).first()
        if not user:
            new_user = User(name=name, role=role)
            db.session.add(new_user)
            db.session.commit()

        if role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))

    return render_template('login.html')

@app.route('/teacher', methods=['GET', 'POST'])
def teacher_dashboard():
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))

    if request.method == 'POST':
        student_name = request.form['student']
        date = request.form['date']
        status = request.form['status']

        existing = Attendance.query.filter_by(student_name=student_name, date=date).first()
        if existing:
            flash("⚠ Attendance already marked for this student on this date!", "warning")
        else:
            record = Attendance(student_name=student_name, date=date, status=status)
            db.session.add(record)
            db.session.commit()
            flash("✅ Attendance submitted successfully!", "success")

    data = Attendance.query.all()
    return render_template('teacher_dashboard.html', data=data)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_attendance(id):
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))

    record = Attendance.query.get_or_404(id)

    if request.method == 'POST':
        record.student_name = request.form['student']
        record.date = request.form['date']
        record.status = request.form['status']
        db.session.commit()
        flash("✅ Attendance record updated successfully!", "success")
        return redirect(url_for('teacher_dashboard'))

    return render_template('edit_attendance.html', record=record)

@app.route('/delete/<int:id>', methods=['GET'])
def delete_attendance(id):
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))

    record = Attendance.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash("🗑 Attendance record deleted successfully!", "success")
    return redirect(url_for('teacher_dashboard'))

@app.route('/student_dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('login'))

    name = session.get('name')
    student_data = Attendance.query.filter_by(student_name=name).all()
    return render_template('student_dashboard.html', name=name, data=student_data)

# Corrected this part too:
if __name__ == '__main__':
    app.run(debug=True)