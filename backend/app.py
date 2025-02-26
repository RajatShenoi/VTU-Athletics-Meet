from flask import Flask,request, jsonify

from models import Hostel, Room, db, Student, College

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route("/api/college/create", methods=["POST"])
def create_college():
    try:
        data = request.get_json()
        required_fields = ["name"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400

        college = College(
            name=data["name"]
        )
        db.session.add(college)
        db.session.commit()
        return jsonify({
            "message": "College created successfully",
            "college": {
                "id": college.id,
                "name": college.name
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/student/create", methods=["POST"])
def create_student():
    try:
        data = request.get_json()
        required_fields = ["name", "phone", "college_id"]
        missing = [field for field in required_fields if field not in data]

        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400
        
        if len(data["phone"]) != 10 or not data["phone"].isdigit():
            return jsonify({"error": "Phone number must be exactly 10 numeric characters long"}), 400
        
        college = db.session.get(College, data["college_id"])
        if not college:
            return jsonify({"error": "Invalid college_id provided"}), 400

        student = Student(
            name=data["name"],
            phone=data["phone"],
            college_id=data["college_id"],
            room_id=data.get("room_id")
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({
            "message": "Student created successfully",
            "student": {
                "id": student.id,
                "name": student.name,
                "phone": student.phone,
                "college_id": student.college_id,
                "room_id": student.room_id
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/api/hostel/create", methods=["POST"])
def create_hostel():
    try:
        data = request.get_json()
        required_fields = ["name"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400

        hostel = Hostel(
            name=data["name"]
        )
        db.session.add(hostel)
        db.session.commit()
        return jsonify({
            "message": "Hostel created successfully",
            "hostel": {
                "id": hostel.id,
                "name": hostel.name
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/api/room/create", methods=["POST"])
def create_room():
    try:
        data = request.get_json()
        required_fields = ["max_occupancy", "number", "hostel_id"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({"error": f"Missing required field(s): {', '.join(missing)}"}), 400

        try:
            max_occupancy = int(data["max_occupancy"])
        except ValueError:
            return jsonify({"error": "Max occupancy must be an integer"}), 400

        hostel = db.session.get(Hostel, data["hostel_id"])
        if not hostel:
            return jsonify({"error": "Invalid hostel_id provided"}), 400

        room = Room(
            max_occupancy=max_occupancy,
            number=data["number"],
            hostel_id=data["hostel_id"]
        )
        db.session.add(room)
        db.session.commit()
        return jsonify({
            "message": "Room created successfully",
            "room": {
                "id": room.id,
                "max_occupancy": room.max_occupancy,
                "number": room.number,
                "hostel_id": room.hostel_id
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)