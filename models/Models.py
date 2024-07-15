from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Rol(db.Model):
    __tablename__ = "tbl_rol"
    id_rol = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10), unique=True, nullable=False)
    clients = db.relationship("Clients", back_populates="rol")


class Clients(db.Model):
    __tablename__ = "tbl_clients"
    id_clients = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    dni = db.Column(db.BigInteger, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    celphone = db.Column(db.BigInteger, unique=True, nullable=False)
    gender = db.Column(db.String(10), unique=False, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(300), unique=False, nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey(
        "tbl_rol.id_rol"), nullable=False)
    rol = db.relationship("Rol", back_populates="clients")
    assessment = db.relationship("Assessment", back_populates="clients")
    volumetry = db.relationship("Volumetry", back_populates="clients")
    skinfold = db.relationship("Skinfold", back_populates="clients")
    fileupload = db.relationship("fileUpload", back_populates="clients")
    failed_attempts = db.Column(db.Integer, default=0, nullable=False)
    lockout_until = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "id_clients": self.id_clients,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dni": self.dni,
            "email": self.email,
            "celphone": self.celphone,
            "birth_date": self.birth_date,
        }

    def is_locked_out(self):
        if self.lockout_until and datetime.utcnow() < self.lockout_until:
            return True
        return False

    def increment_failed_attempts(self):
        self.failed_attempts += 1
        if self.failed_attempts >= 5:
            self.lockout_until = datetime.utcnow() + timedelta(minutes=15)
            self.failed_attempts = 0  # reset after lockout
        db.session.commit()

    def reset_failed_attempts(self):
        self.failed_attempts = 0
        self.lockout_until = None
        db.session.commit()


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"<Token {self.jti}>"

    def save(self):
        db.session.add(self)
        db.session.commit()


class Assessment(db.Model):
    __tablename__ = "tbl_assessment"
    id_assessment = db.Column(db.Integer, primary_key=True)
    assessment_date = db.Column(db.Date, nullable=False)
    height_cm = db.Column(db.Integer, nullable=False)
    height_mts = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    humerus_diameter = db.Column(db.Float, nullable=False)
    femur_diameter = db.Column(db.Float, nullable=False)
    id_clients = db.Column(
        db.Integer, db.ForeignKey("tbl_clients.id_clients"), nullable=False
    )
    clients = db.relationship("Clients", back_populates="assessment")

    def to_json(self):
        return {
            "id_assessment": self.id_assessment,
            "assessment_date": self.assessment_date,
            "height_cm": self.height_cm,
            "height_mts": self.height_mts,
            "weight": self.weight,
            "humerus_diameter": self.humerus_diameter,
            "femur_diameter": self.femur_diameter,
            "id_clients": self.id_clients,
        }


class Volumetry(db.Model):
    __tablename__ = "tbl_volumetry"
    id_volumetry = db.Column(db.Integer, primary_key=True)
    v_neck = db.Column(db.Float, nullable=False)
    v_shoulder = db.Column(db.Float, nullable=False)
    v_torax = db.Column(db.Float, nullable=False)
    v_abdomen = db.Column(db.Float, nullable=False)
    v_bitrochanteric = db.Column(db.Float, nullable=False)
    v_thig = db.Column(db.Float, nullable=False)
    v_leg = db.Column(db.Float, nullable=False)
    v_biceps = db.Column(db.Float, nullable=False)
    id_clients = db.Column(
        db.Integer, db.ForeignKey("tbl_clients.id_clients"), nullable=False
    )
    clients = db.relationship("Clients", back_populates="volumetry")

    def to_json(self):
        return {
            "id_volumetry": self.id_volumetry,
            "v_neck": self.v_neck,
            "v_shoulder": self.v_shoulder,
            "v_torax": self.v_torax,
            "v_abdomen": self.v_abdomen,
            "v_bitrochanteric": self.v_bitrochanteric,
            "v_thig": self.v_thig,
            "v_leg": self.v_leg,
            "v_biceps": self.v_biceps,
            "id_clients": self.id_clients,
        }


class Skinfold(db.Model):
    __tablename__ = "tbl_skinfold"
    id_skinfold = db.Column(db.Integer, primary_key=True)
    sf_tricipital = db.Column(db.Float, nullable=False)
    sf_subscapular = db.Column(db.Float, nullable=False)
    sf_suprailiac = db.Column(db.Float, nullable=False)
    sf_abdominal = db.Column(db.Float, nullable=False)
    sf_thigh = db.Column(db.Float, nullable=False)
    sf_leg = db.Column(db.Float, nullable=False)
    id_clients = db.Column(
        db.Integer, db.ForeignKey("tbl_clients.id_clients"), nullable=False
    )
    clients = db.relationship("Clients", back_populates="skinfold")

    def to_json(self):
        return {
            "id_skinfold": self.id_skinfold,
            "sf_tricipital": self.sf_tricipital,
            "sf_subscapular": self.sf_subscapular,
            "sf_suprailiac": self.sf_suprailiac,
            "sf_abdominal": self.sf_abdominal,
            "sf_thigh": self.sf_thigh,
            "sf_leg": self.sf_leg,
            "id_clients": self.id_clients,
        }


class fileUpload(db.Model):
    __tablename__ = "tbl_fileupload"
    id_file = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(500), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    upload_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    id_clients = db.Column(
        db.Integer, db.ForeignKey("tbl_clients.id_clients"), nullable=False
    )
    clients = db.relationship("Clients", back_populates="fileupload")

    # def to_json(self):
    #     return {
    #         "id_file": self.id_file,
    #         "filename": self.filename,
    #         "filepath": self.filepath,
    #         "id_clients": self.id_clients,
    #     }
