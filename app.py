import io
import smtplib
from datetime import datetime

from config import ApplicationConfig
from flask import Flask, jsonify, request, send_file, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
from flask_session import Session
from models import Patient, PhysicianNotes, User, Vitals, db
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({"id": user.id, "email": user.email})


@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, name=name)
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    return jsonify({"id": new_user.id, "email": new_user.email})


@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.id

    return jsonify({"id": user.id, "email": user.email})


@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"


@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()  # Query all users
    result = [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "specialization": u.specialization,
            "contact_number": u.contact_number,
        }
        for u in users
    ]
    return jsonify(result), 200


# ------------------ CRUD for Patients ------------------ #


@app.route("/patients", methods=["GET"])
def get_all_patients():
    patients = Patient.query.all()
    result = [
        {
            "id": p.id,
            "name": p.name,
            "email": p.email,
            "dob": p.date_of_birth,
            "gender": p.gender,
            "contact": p.contact_number,
        }
        for p in patients
    ]
    return jsonify(result), 200


@app.route("/patients/<id>", methods=["GET"])
def get_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    if patient is None:
        return jsonify({"error": "Patient not found"}), 404

    return (
        jsonify(
            {
                "id": patient.id,
                "name": patient.name,
                "email": patient.email,
                "dob": patient.date_of_birth,
                "gender": patient.gender,
                "contact": patient.contact_number,
            }
        ),
        200,
    )


@app.route("/patients", methods=["POST"])
def create_patient():
    data = request.json
    date_of_birth = datetime.strptime(data["dob"], "%Y-%m-%d").date()
    new_patient = Patient(
        name=data["name"],
        email=data["email"],
        date_of_birth=date_of_birth,
        gender=data["gender"],
        contact_number=data["contact"],
    )
    db.session.add(new_patient)
    db.session.commit()
    return (
        jsonify({"id": new_patient.id, "message": "Patient created successfully"}),
        201,
    )


@app.route("/patients/<id>", methods=["PUT"])
def update_patient(id):
    data = request.json
    patient = Patient.query.filter_by(id=id).first()
    if patient is None:
        return jsonify({"error": "Patient not found"}), 404

    patient.name = data.get("name", patient.name)
    patient.email = data.get("email", patient.email)
    patient.date_of_birth = data.get("dob", patient.date_of_birth)
    patient.gender = data.get("gender", patient.gender)
    patient.contact_number = data.get("contact", patient.contact_number)
    db.session.commit()

    return jsonify({"message": "Patient updated successfully"}), 200


@app.route("/patients/<id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    if patient is None:
        return jsonify({"error": "Patient not found"}), 404

    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully"}), 200


# ------------------ CRUD for Vitals ------------------ #


@app.route("/vitals", methods=["GET"])
def get_all_vitals():
    vitals = Vitals.query.all()
    result = [
        {
            "id": v.id,
            "patient_id": v.patient_id,
            "heart_rate": v.heart_rate,
            "blood_pressure": v.blood_pressure,
            "respiration_rate": v.respiration_rate,
            "temperature": v.temperature,
            "measurement_time": v.measurement_time,
        }
        for v in vitals
    ]
    return jsonify(result), 200


from flask import jsonify, request


@app.route("/vitals/<id>", methods=["GET"])
def get_vitals(id):
    start_date_str = request.args.get(
        "start_date"
    )  # Get the start date from query parameters

    start_date = None
    if start_date_str:
        start_date = datetime.fromisoformat(
            start_date_str[:-1]
        )  # Convert string to datetime

    # Filter query
    if start_date:
        vitals = Vitals.query.filter(
            Vitals.patient_id == id, Vitals.measurement_time >= start_date
        ).all()
    else:
        vitals = Vitals.query.filter_by(patient_id=id).all()

    if not vitals:  # Check if the list is empty
        return jsonify({"error": "Vitals not found"}), 404

    # Create a list to hold all vital records
    vitals_list = [
        {
            "id": vital.id,
            "patient_id": vital.patient_id,
            "heart_rate": vital.heart_rate,
            "blood_pressure": vital.blood_pressure,
            "respiration_rate": vital.respiration_rate,
            "temperature": vital.temperature,
            "measurement_time": vital.measurement_time,
        }
        for vital in vitals
    ]

    return jsonify(vitals_list), 200


@app.route("/vitals", methods=["POST"])
def create_vitals():
    data = request.json
    new_vitals = Vitals(
        patient_id=data["patient_id"],
        heart_rate=data["heart_rate"],
        blood_pressure=data["blood_pressure"],
        respiration_rate=data["respiration_rate"],
        temperature=data["temperature"],
    )
    db.session.add(new_vitals)
    db.session.commit()
    return jsonify({"id": new_vitals.id, "message": "Vitals created successfully"}), 201


@app.route("/vitals/<id>", methods=["PUT"])
def update_vitals(id):
    data = request.json
    vitals = Vitals.query.filter_by(id=id).first()
    if vitals is None:
        return jsonify({"error": "Vitals not found"}), 404

    vitals.heart_rate = data.get("heart_rate", vitals.heart_rate)
    vitals.blood_pressure = data.get("blood_pressure", vitals.blood_pressure)
    vitals.respiration_rate = data.get("respiration_rate", vitals.respiration_rate)
    vitals.temperature = data.get("temperature", vitals.temperature)
    db.session.commit()

    return jsonify({"message": "Vitals updated successfully"}), 200


@app.route("/vitals/<id>", methods=["DELETE"])
def delete_vitals(id):
    vitals = Vitals.query.filter_by(id=id).first()
    if vitals is None:
        return jsonify({"error": "Vitals not found"}), 404

    db.session.delete(vitals)
    db.session.commit()
    return jsonify({"message": "Vitals deleted successfully"}), 200


# ------------------ CRUD for PhysicianNotes ------------------ #


@app.route("/physician_notes", methods=["GET"])
def get_all_physician_notes():
    notes = PhysicianNotes.query.all()
    result = [
        {
            "id": n.id,
            "patient_id": n.patient_id,
            "physician_id": n.physician_id,
            "note": n.note,
            "created_at": n.created_at,
        }
        for n in notes
    ]
    return jsonify(result), 200


from datetime import datetime

from flask import request


@app.route("/physician_notes/<id>", methods=["GET"])
def get_physician_notes(id):
    # Get the start_date query parameter from the request
    start_date_str = request.args.get("start_date")
    start_date = None

    # Convert start_date to datetime if provided
    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str)
        except ValueError:
            return jsonify({"error": "Invalid start date format"}), 400

    # Query for physician notes, optionally filtering by start_date
    query = PhysicianNotes.query.filter_by(patient_id=id)

    # Filter notes by start_date if provided
    if start_date:
        query = query.filter(PhysicianNotes.created_at >= start_date)

    notes = query.all()  # Use .all() to get multiple notes

    if not notes:
        return jsonify({"error": "No notes found"}), 404

    return (
        jsonify(
            [
                {
                    "id": note.id,
                    "patient_id": note.patient_id,
                    "physician_id": note.physician_id,
                    "note": note.note,
                    "created_at": note.created_at.isoformat(),  # Convert to ISO format for JSON serialization
                }
                for note in notes
            ]
        ),
        200,
    )


@app.route("/physician_notes", methods=["POST"])
def create_physician_note():
    data = request.json
    new_note = PhysicianNotes(
        patient_id=data["patient_id"],
        physician_id=data["physician_id"],
        note=data["note"],
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"id": new_note.id, "message": "Note created successfully"}), 201


@app.route("/physician_notes/<id>", methods=["PUT"])
def update_physician_note(id):
    data = request.json
    note = PhysicianNotes.query.filter_by(id=id).first()
    if note is None:
        return jsonify({"error": "Note not found"}), 404

    note.note = data.get("note", note.note)
    db.session.commit()

    return jsonify({"message": "Note updated successfully"}), 200


@app.route("/physician_notes/<id>", methods=["DELETE"])
def delete_physician_note(id):
    note = PhysicianNotes.query.filter_by(id=id).first()
    if note is None:
        return jsonify({"error": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
