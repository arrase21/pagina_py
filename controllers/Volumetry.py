from flask import Blueprint, request, jsonify
from models.Models import Volumetry, Clients, db

volumetry_bp = Blueprint("volumetry", __name__)


@volumetry_bp.route("/volumetry/<int:client_id>/", methods=["GET"])
def get_volumetry(client_id):
    client = Clients.query.get_or_404(client_id)
    volumetries = Volumetry.query.filter_by(id_clients=client.id_clients).all()
    return jsonify(
        {"Volumetries": [volumetry.to_json() for volumetry in volumetries]}
    ), 200


@volumetry_bp.route("/volumetry/add/", methods=["POST"])
def add_volumetry():
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    data = request.get_json()
    required_fields = [
        "id_clients",
        "v_neck",
        "v_shoulder",
        "v_torax",
        "v_abdomen",
        "v_bitrochanteric",
        "v_thig",
        "v_leg",
        "v_biceps",
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    clients = Clients.query.get_or_404(data["id_clients"])

    new_volumetry = Volumetry(
        v_neck=data["v_neck"],
        v_shoulder=data["v_shoulder"],
        v_torax=data["v_torax"],
        v_abdomen=data["v_abdomen"],
        v_bitrochanteric=data["v_bitrochanteric"],
        v_thig=data["v_thig"],
        v_leg=data["v_leg"],
        v_biceps=data["v_biceps"],
        id_clients=clients.id_clients,
    )

    try:
        db.session.add(new_volumetry)
        db.session.commit()
        return jsonify({"message": "Volumetry added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
