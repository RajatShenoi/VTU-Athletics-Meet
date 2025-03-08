from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    poc = db.Column(db.String(128), nullable=True)
    students = db.relationship('Student', backref='college', lazy=True)
    # Yet to arrive; Checked in; Checked out
    status = db.Column(db.String(20), nullable=False, default='Yet to arrive')

    def get_student_count(self):
        return len(self.students)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rooms = db.relationship('Room', backref='location', lazy=True)

    def get_room_count(self):
        return len(self.rooms)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    max_occupancy = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    students = db.relationship('Student', backref='room', lazy=True)

    def get_student_count(self, college_id=None):
        if college_id is None:
            return len(self.students)
        a = [student for student in self.students if student.college_id == int(college_id)]
        return len(a)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)