from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"  # The table name for physicians
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    specialization = db.Column(db.String(100), nullable=True)
    contact_number = db.Column(db.String(15), nullable=True)
    notes = db.relationship("PhysicianNotes", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.name}, Email: {self.email}>"

class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(345), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    vitals = db.relationship("Vitals", backref="patient", lazy=True)
    notes = db.relationship("PhysicianNotes", backref="patient", lazy=True)

    def __repr__(self):
        return f"<Patient {self.name}, Email: {self.email}>"

class Vitals(db.Model):
    __tablename__ = "vitals"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    patient_id = db.Column(db.String(32), db.ForeignKey("patients.id"), nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    blood_pressure = db.Column(db.String(10), nullable=False)
    respiration_rate = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    measurement_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Vitals Patient ID: {self.patient_id}, Temp: {self.temperature}>"

class PhysicianNotes(db.Model):
    __tablename__ = "physician_notes"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    patient_id = db.Column(db.String(32), db.ForeignKey("patients.id"), nullable=False)
    physician_id = db.Column(db.String(32), db.ForeignKey("users.id"), nullable=False)  # Corrected the foreign key reference
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<PhysicianNote ID: {self.id}, Patient ID: {self.patient_id}>"
