from flask import Flask, request, jsonify
from flask_cors import CORS

from models import Location, Room, db, Student, College

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

@app.route("/api/college/create", methods=["POST"])
def create_college():
    try:
        data = request.get_json()
        required_fields = ["name", "code", "poc"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400
        
        if not data["poc"].isdigit() or len(data["poc"]) != 10:
            return jsonify({"error": "Contact Number must be numeric and exactly 10 digits"}), 400

        college = College(
            name=data["name"].strip().title(),
            code=data["code"].strip().upper(),
            poc=data["poc"].strip()
        )
        
        db.session.add(college)
        db.session.commit()
        return jsonify({
            "message": "College created successfully",
            "college": {
                "id": college.id,
                "code": college.code,
                "name": college.name,
                "poc": college.poc
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/student/create", methods=["POST"])
def create_student():
    try:
        data = request.get_json()
        required_fields = ["college_id"]
        missing = [field for field in required_fields if field not in data]

        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400
        
        college = db.session.get(College, data["college_id"])
        if not college:
            return jsonify({"error": "Invalid college_id provided"}), 400

        student = Student(
            name=data.get("name"),
            phone=data.get("phone"),
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

@app.route("/api/location/create", methods=["POST"])
def create_location():
    try:
        data = request.get_json()
        required_fields = ["name"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400

        location = Location(
            name=data["name"].strip().title()
        )
        db.session.add(location)
        db.session.commit()
        return jsonify({
            "message": "Hostel created successfully",
            "hostel": {
                "id": location.id,
                "name": location.name
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/room/create", methods=["POST"])
def create_room():
    try:
        data = request.get_json()
        required_fields = ["max_occupancy", "number", "location_id"]
        for field in required_fields:
            if not data.get(field) or not str(data.get(field)).strip():
                return jsonify({"error": f"Field {field} cannot be blank"}), 400
            
        try:
            max_occupancy = int(data["max_occupancy"])
        except ValueError:
            return jsonify({"error": "Max occupancy must be an integer"}), 400

        hostel = db.session.get(Location, data["location_id"])
        if not hostel:
            return jsonify({"error": "Invalid location_id provided"}), 400

        existing_room = Room.query.filter_by(number=data["number"], location_id=data["location_id"]).first()
        if existing_room:
            return jsonify({"error": "Room with the same number in this location already exists"}), 400

        room = Room(
            max_occupancy=max_occupancy,
            number=data["number"],
            location_id=data["location_id"]
        )
        db.session.add(room)
        db.session.commit()
        return jsonify({
            "message": "Room created successfully",
            "room": {
                "id": room.id,
                "max_occupancy": room.max_occupancy,
                "number": room.number,
                "location_id": room.location_id
            }
        }), 201
    except ValueError as ve:
        db.session.rollback()
        return jsonify({"error": f"Value error: {str(ve)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/college/list", methods=["GET"])
def get_colleges():
    try:
        colleges = College.query.all()
        colleges.sort(key=lambda c: c.code)
        return jsonify({
            "colleges": [
                {
                    "id": college.id,
                    "name": college.name,
                    "code": college.code,
                    "poc": college.poc,
                    "num_occupants": college.get_student_count()
                } for college in colleges
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/location/list", methods=["GET"])
def get_locations():
    try:
        locations = Location.query.all()
        return jsonify({
            "locations": [
                {
                    "id": location.id,
                    "name": location.name,
                    "num_rooms": location.get_room_count()
                } for location in locations]
        }), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/room/list", methods=["GET"])
def get_rooms():
    try:
        rooms = Room.query.all()
        rooms.sort(key=lambda r: (r.location.name, r.number))
        return jsonify({
                    "rooms": [
                        {
                            "id": room.id,
                            "max_occupancy": room.max_occupancy,
                            "number": room.number,
                            "location": room.location.name,
                            "num_students": room.get_student_count()
                        } for room in rooms
                    ]
                }), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/api/room/available", methods=["GET"])
def get_available_rooms():
    try:
        rooms = Room.query.all()
        available_rooms = []

        if not request.args.get("college_id"):
            return jsonify({"error": "college_id parameter is required"}), 400

        for room in rooms:
            if room.get_student_count() < room.max_occupancy:
                available_rooms.append({
                    "id": room.id,
                    "max_occupancy": room.max_occupancy,
                    "number": room.number,
                    "location": room.location.name,
                    "num_students": room.get_student_count(),
                    "same_college_students": room.get_student_count(college_id=request.args.get("college_id")),
                    "available_slots": room.max_occupancy - room.get_student_count()
                })
        available_rooms.sort(key=lambda r: (-r["same_college_students"], r["location"], r["number"]))
        return jsonify({"available_rooms": available_rooms}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/college/fromcode", methods=["GET"])
def get_college_by_code():
    try:
        college_code = request.args.get("code")
        if not college_code:
            return jsonify({"error": "Parameter 'code' is required"}), 400

        college = College.query.filter_by(code=college_code.strip().upper()).first()
        if not college:
            return jsonify({"error": "College not found"}), 404

        return jsonify({
            "college": {
                "id": college.id,
                "code": college.code,
                "name": college.name,
                "poc": college.poc,
                "num_occupants": college.get_student_count()
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/api/student/checkin", methods=["POST"])
def student_checkin():
    try:
        data = request.get_json()
        required_fields = ["college_id", "room_id"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400

        college = db.session.get(College, data["college_id"])
        if not college:
            return jsonify({"error": "College not found"}), 404

        room = db.session.get(Room, data["room_id"])
        if not room:
            return jsonify({"error": "Room not found"}), 404

        if room.get_student_count() >= room.max_occupancy:
            return jsonify({"error": "Room is full"}), 400

        student = Student(
            college_id=data["college_id"],
            room_id=data["room_id"]
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({
            "message": "Student checked in successfully",
            "student": {
                "id": student.id,
                "college_id": student.college_id,
                "room_id": student.room_id
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/student/checkout", methods=["POST"])
def student_checkout():
    try:
        data = request.get_json()
        required_fields = ["room_id", "college_id"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400

        student = Student.query.filter_by(college_id=data["college_id"], room_id=data["room_id"]).first()
        if not student:
            return jsonify({"error": "Student not found from this college."}), 404

        db.session.delete(student)
        db.session.commit()

        return jsonify({"message": "Student checked out successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/api/college/occupied_rooms", methods=["GET"])
def get_occupied_rooms_by_college():
    try:
        college_id = request.args.get("college_id")
        if not college_id:
            return jsonify({"error": "college_id parameter is required"}), 400

        college = db.session.get(College, college_id)
        if not college:
            return jsonify({"error": "College not found"}), 404

        student_rooms = Student.query.filter(
            Student.college_id == college_id,
            Student.room_id.isnot(None)
        ).with_entities(Student.room_id).distinct().all()

        room_ids = [room_id for (room_id,) in student_rooms]
        rooms = Room.query.filter(Room.id.in_(room_ids)).all()

        result = []
        for room in rooms:
            count = Student.query.filter(
                Student.college_id == college_id,
                Student.room_id == room.id
            ).count()
            result.append({
                "id": room.id,
                "max_occupancy": room.max_occupancy,
                "num_students": room.get_student_count(),
                "same_college_students": room.get_student_count(college_id),
                "number": room.number,
                "location": room.location.name,
                "occupied_by_college": count
            })
        result.sort(key=lambda r: (r["location"], r["number"]))
        return jsonify({"rooms": result}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)