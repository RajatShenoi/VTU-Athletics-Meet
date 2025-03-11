import io
import os

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash



from models import Location, Room, db, Student, College, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

@jwt.unauthorized_loader
def custom_unauthorized_response(callback):
    return jsonify({
        "error": "Authentication required. Please log in to access this resource."
    }), 401

@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        required_fields = ["username", "password"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400

        user = User.query.filter_by(username=data["username"]).first()
        if not user or not check_password_hash(user.password, data["password"]):
            return jsonify({"error": "Invalid username or password"}), 401

        access_token = create_access_token(identity=str(user.id))
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/college/create", methods=["POST"])
@jwt_required()
def create_college():
    try:
        data = request.get_json()
        required_fields = ["name", "code"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400
        
        if data.get("poc") and (not data["poc"].isdigit() or len(data["poc"]) != 10):
            return jsonify({"error": "Contact Number must be numeric and exactly 10 digits"}), 400
        
        college = College(
            name=data["name"].strip().title(),
            code=data["code"].strip().upper(),
        )

        if data.get('poc'):
            college.poc = data['poc']

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

@app.route("/api/college/update", methods=["PUT"])
@jwt_required()
def update_college():
    try:
        data = request.get_json()
        required_fields = ["id"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400

        college = db.session.get(College, data["id"])
        if not college:
            return jsonify({"error": "College not found"}), 404

        if data.get("name"):
            college.name = data["name"].strip().title()
        if data.get("code"):
            college.code = data["code"].strip().upper()
        
        college.poc = data["poc"]

        db.session.commit()
        return jsonify({
            "message": "College updated successfully",
            "college": {
                "id": college.id,
                "code": college.code,
                "name": college.name,
                "poc": college.poc
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/student/create", methods=["POST"])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
            number=int(data["number"]),
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
@jwt_required()
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
                    "num_occupants": college.get_student_count(),
                    "status": college.status
                } for college in colleges
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/location/list", methods=["GET"])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
                "num_occupants": college.get_student_count(),
                "status": college.status
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/api/student/checkin", methods=["POST"])
@jwt_required()
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
            college = College.query.filter_by(code=data["college_id"].strip().upper()).first()
        if not college:
            return jsonify({"error": "College not found"}), 404

        room = db.session.get(Room, data["room_id"])
        if not room:
            return jsonify({"error": "Room not found"}), 404

        if room.get_student_count() >= room.max_occupancy:
            return jsonify({"error": "Room is full"}), 400

        college_id = college.id

        student = Student(
            college_id=college_id,
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
@jwt_required()
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
@jwt_required()
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

@app.route("/api/college/report", methods=["GET"])
@jwt_required()
def college_report():
    try:
        report = []
        college_code = request.args.get("code")
        if college_code:
            colleges = College.query.filter_by(code=college_code.strip().upper()).all()
        else:
            colleges = College.query.all()
        for college in colleges:
            rooms_data = (
                db.session.query(Student.room_id, db.func.count(Student.id))
                .filter(Student.college_id == college.id, Student.room_id.isnot(None))
                .group_by(Student.room_id)
                .all()
            )
            room_details = []
            for room_id, count in rooms_data:
                room = db.session.get(Room, room_id)
                if room:
                    room_details.append({
                        "room_id": room.id,
                        "number": room.number,
                        "location": room.location.name,
                        "max_occupancy": room.max_occupancy,
                        "occupied_by_college_count": count
                    })
            room_details.sort(key=lambda r: (r["location"], r["number"]))
            report.append({
                "college_id": college.id,
                "college_code": college.code,
                "college_name": college.name,
                "college_count": college.get_student_count(),
                "poc": college.poc,
                "rooms": room_details
            })
        report.sort(key=lambda r: r["college_code"])
        return jsonify({"report": report}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/api/location/report", methods=["GET"])
@jwt_required()
def location_report():
    try:
        report = []
        location_name = request.args.get("location_name")
        if location_name:
            locations = Location.query.filter(Location.name.ilike(f"%{location_name.strip().title()}%")).all()
        else:
            locations = Location.query.all()
        for location in locations:
            rooms = Room.query.filter_by(location_id=location.id).all()
            total_students = sum(room.get_student_count() for room in rooms)
            room_details = [{
                "room_id": room.id,
                "number": room.number,
                "max_occupancy": room.max_occupancy,
                "num_students": room.get_student_count(),
                "college_counts": {
                    college_code: count
                    for college_code, count in db.session.query(
                        College.code, db.func.count(Student.id)
                    ).join(
                        Student, Student.college_id == College.id
                    ).filter(
                        Student.room_id == room.id
                    ).group_by(
                        College.code
                    ).all()
                }
            } for room in rooms]
            room_details.sort(key=lambda r: r["number"])
            report.append({
                "location_id": location.id,
                "location_name": location.name,
                "num_rooms": len(rooms),
                "total_students": total_students,
                "rooms": room_details
            })
        report.sort(key=lambda r: r["location_name"])
        return jsonify({"report": report}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/college/status", methods=["POST"])
@jwt_required()
def update_college_status():
    try:
        data = request.get_json()
        required_fields = ["college_id", "status"]
        missing = [field for field in required_fields if field not in data]
        if not data or missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400

        college = db.session.get(College, data["college_id"])
        if not college:
            return jsonify({"error": "College not found"}), 404
        
        accepted_values = ["Yet to arrive", "Checked in", "Checked out"]
        if data["status"] not in accepted_values:
            return jsonify({"error": f"Invalid status. Accepted values are: {', '.join(accepted_values)}"}), 400

        college.status = data["status"]
        db.session.commit()

        return jsonify({
            "message": "College status updated successfully",
            "college": {
                "id": college.id,
                "code": college.code,
                "name": college.name,
                "poc": college.poc,
                "status": college.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/college/report/pdf", methods=["GET"])
@jwt_required()
def generate_college_pdf_report():
    try:
        report_response = college_report()
        report_data = report_response[0].get_json()["report"]

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Normal'],
            fontSize=12,
            leading=14,
            alignment=0,  # Left align
            spaceAfter=10
        )

        for college in report_data:
            college_info = f"Code: {college['college_code']}; {college['college_name']}; POC: {college.get('poc', 'N/A')}"
            elements.append(Paragraph(college_info, title_style))
            data = [["Location", "Room Number", "Max Occupancy", f"Occupied by {college['college_code']}"]]
            for room in college["rooms"]:
                data.append([room["location"], str(room["number"]), str(room["max_occupancy"]), str(room["occupied_by_college_count"])])

            table = Table(data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch, 2 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="college_report.pdf", mimetype='application/pdf')
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/location/report/pdf", methods=["GET"])
@jwt_required()
def generate_location_pdf_report():
    try:
        report_response = location_report()
        report_data = report_response[0].get_json()["report"]

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        normal_style = styles['Normal']

        for location in report_data:
            elements.append(Paragraph(f"Location: {location['location_name']}; Total Students: {location['total_students']}", styles['Title']))
            data = [["Room Number", "Max Occupancy", "Current Count", "Colleges"]]
            for room in location["rooms"]:
                colleges = ", ".join([f"{college_code}: {count}" for college_code, count in room["college_counts"].items()])
                data.append([str(room["number"]), str(room["max_occupancy"]), str(room["num_students"]), Paragraph(colleges, normal_style)])

            table = Table(data, colWidths=[1.5 * inch, 1.5 * inch, 1.5 * inch, 3 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('WORDWRAP', (3, 1), (3, -1), 'CJK')
            ]))

            elements.append(table)
            elements.append(PageBreak())

        doc.build(elements)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="location_report.pdf", mimetype='application/pdf')
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def create_default_admin():
    default_admin = User.query.filter_by(username='admin').first()
    if not default_admin:
        default_admin = User(username='admin', password=generate_password_hash(os.getenv('PASSWORD')))
        db.session.add(default_admin)
        db.session.commit()
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_admin()
    app.run(debug=True)