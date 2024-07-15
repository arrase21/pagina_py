from flask import Blueprint, request, jsonify
from models.Models import Skinfold, Clients, db


skinfold_bp = Blueprint("skinfold", __name__)


@skinfold_bp.route("/skinfold/<int:id_clients>/", methods=["GET"])
def get_skinfolds(id_clients):
    client = Clients.query.get_or_404(id_clients)
    skinfolds = Skinfold.query.filter_by(id_clients=client.id_clients).all()
    return jsonify({"Skinfold": [skinfold.to_json() for skinfold in skinfolds]}), 200


@skinfold_bp.route("/skinfold/add/", methods=["POST"])
def add_skinfold():
    if not request.is_json:
        return jsonify({"Message": "Request must be JSON"}), 400
    data = request.get_json()
    required_files = [
        "id_clients",
        "sf_tricipital",
        "sf_subscapular",
        "sf_suprailiac",
        "sf_abdominal",
        "sf_thigh",
        "sf_leg",
    ]

    if not all(field in data for field in required_files):
        return jsonify({"Message": "Missing required files"}), 400

    clients = Clients.query.get_or_404(data["id_clients"])

    new_skinfold = Skinfold(
        sf_tricipital=data["sf_tricipital"],
        sf_subscapular=data["sf_subscapular"],
        sf_suprailiac=data["sf_suprailiac"],
        sf_abdominal=data["sf_abdominal"],
        sf_thigh=data["sf_thigh"],
        sf_leg=data["sf_leg"],
        id_clients=clients.id_clients,
    )
    try:
        db.session.add(new_skinfold)
        db.session.commit()
        return jsonify({"Message": "Skinfold added successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 400


@skinfold_bp.route("/skinfold/update/<int:id_skinfold>/", methods=["PATCH"])
def update_skinfold(id_skinfold):
    if not request.is_json:
        return jsonify({"Message": "Request must be JSON"}), 400

    skinfold = Skinfold.query.get_or_404(id_skinfold)
    data = request.get_json()
    skinfold.sf_tricipital = data.get("sf_tricipital", skinfold.sf_tricipital)
    skinfold.sf_subscapular = data.get(
        "sf_subscapular", skinfold.sf_subscapular)
    skinfold.sf_suprailiac = data.get("sf_suprailiac", skinfold.sf_suprailiac)
    skinfold.sf_abdominal = data.get("sf_abdominal", skinfold.sf_abdominal)
    skinfold.sf_thigh = data.get("sf_thigh", skinfold.sf_thigh)
    skinfold.sf_leg = data.get("sf_leg", skinfold.sf_leg)

    try:
        db.session.commit()
        return jsonify({"Message": "Skinfold updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": str(e)}), 400
