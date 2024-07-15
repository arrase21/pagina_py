from flask import Blueprint, jsonify, request
from models.Models import Assessment, Clients, db

assessment_bp = Blueprint("assessment", __name__)


@assessment_bp.route("/assessment/<int:client_id>/", methods=["GET"])
def get_assessment(client_id):
    client = Clients.query.get_or_404(client_id)
    assessments = Assessment.query.filter_by(client_id=client.id).all()
    return jsonify(
        {"Assessment": [assessment.to_json() for assessment in assessments]}
    ), 200


@assessment_bp.route("/assessment/add/", methods=["POST"])
def add_assessment():
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    data = request.get_json()
    required_fields = [
        "id_clients",
        "assessment_date",
        "height_cm",
        "height_mts",
        "weight",
        "humerus_diameter",
        "femur_diameter",
    ]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required field(s)"}), 400

    clients = Clients.query.get_or_404(data["id_clients"])

    new_assessment = Assessment(
        assessment_date=data["assessment_date"],
        height_cm=data["height_cm"],
        height_mts=data["height_mts"],
        weight=data["weight"],
        humerus_diameter=data["humerus_diameter"],
        femur_diameter=data["femur_diameter"],
        id_clients=clients.id_clients,  # Asegúrate de usar el ID del cliente
    )

    try:
        db.session.add(new_assessment)
        db.session.commit()
        return jsonify({"message": "Assessment added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@assessment_bp.route("/assessment/client/<int:id_clients>/", methods=["GET"])
def get_assessments_by_client(id_clients):
    client = Clients.query.get_or_404(id_clients)
    assessments = Assessment.query.filter_by(id_clients=client.id_clients).all()
    assessments_list = [assessment.to_json() for assessment in assessments]
    return jsonify(assessments_list), 200


@assessment_bp.route("/assessment/update/<int:id>/", methods=["PATCH"])
def update_assessment(id):
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    assessment = Assessment.query.get_or_404(id)

    data = request.get_json()
    assessment.assessment_date = data.get("assessment_date", assessment.assessment_date)
    assessment.height_cm = data.get("height_cm", assessment.height_cm)
    assessment.height_mts = data.get("height_mts", assessment.height_mts)
    assessment.weight = data.get("weight", assessment.weight)
    assessment.humerus_diameter = data.get(
        "humerus_diameter", assessment.humerus_diameter
    )
    assessment.femur_diameter = data.get("femur_diameter", assessment.femur_diameter)

    try:
        db.session.commit()
        return jsonify({"message": "Assessment updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
