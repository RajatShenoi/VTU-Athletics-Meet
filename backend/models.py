from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    poc = db.Column(db.String(100), nullable=False)
    students = db.relationship('Student', backref='college', lazy=True)

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
    number = db.Column(db.String(10), nullable=False)
    max_occupancy = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    students = db.relationship('Student', backref='room', lazy=True)

    def get_student_count(self):
        return len(self.students)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(10), nullable=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=True)