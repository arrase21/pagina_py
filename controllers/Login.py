from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    current_user,
    get_jwt_identity,
    get_jwt,
)


from flask import Blueprint, request, jsonify
from datetime import timedelta
from models.Models import Clients

jwt = JWTManager()
login_bp = Blueprint("login", __name__)


@login_bp.route("/login/", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    client = Clients.query.filter_by(email=email).first()

    if client is None:
        return jsonify({"msg": "Wrong credentials"}), 401

    if client.is_locked_out():
        return jsonify({"msg": "Account is locked. Try again later."}), 403

    if client.check_password(password):
        client.reset_failed_attempts()
        access_token = create_access_token(
            identity=client.id_clients, expires_delta=timedelta(minutes=3)
        )
        refresh_token = create_refresh_token(identity=client.id_clients)
        return jsonify(
            {
                "Message": "Login success",
                "token": {"Access": access_token, "refresh": refresh_token},
            }
        )
    else:
        client.increment_failed_attempts()
        return jsonify({"msg": "Wrong credentials"}), 401


@login_bp.route("/whoami/", methods=["GET"])
@jwt_required()
def whoami():
    return jsonify(
        {
            "message": "message",
            "user_details": {
                "email": current_user.email,
            },
        }
    )


@login_bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"access_token": new_access_token})


@login_bp.route("/logout/", methods=["GET"])
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()

    jti = jwt["jti"]
    token_type = jwt["type"]

    token_b = TokenBlocklist(jti=jti)

    token_b.save()

    return jsonify({"message": f"{token_type} token revoked successfully"}), 200
