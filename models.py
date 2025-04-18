from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(20), nullable=False)
 
class Attendance(db.Model):

    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)

    student_name = db.Column(db.String(100), nullable=False)

    date = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), nullable=False)

 