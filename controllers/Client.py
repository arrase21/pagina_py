from flask import Blueprint, jsonify, request
from models.Models import Clients, db
from flask_jwt_extended import jwt_required

# Blueprint
clients_bp = Blueprint("clients", __name__)


# Mostrar todos loa clientes
@clients_bp.route("/clients/", methods=["GET"])
@jwt_required()
def get_clients():
    clients = Clients.query.all()
    json_client = list(map(lambda x: x.to_json(), clients))
    return jsonify({"Clients": json_client}), 200


# Mostrat un cliente por el id
@clients_bp.route("/client/<int:id_clients>/", methods=["GET"])
def get_client(id_clients):
    client = Clients.query.get_or_404(id_clients)
    if not client:
        return jsonify({"Message": "Client not found"}), 404
    return jsonify({"Client": client.to_json()}), 200


# Agregar un cliente
@clients_bp.route("/client/add/", methods=["POST"])
@jwt_required()
def add_client():
    if request.json is None:
        return jsonify({"Message": "Not valid request"}), 404

    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    dni = data.get("dni")
    email = data.get("email")
    celphone = data.get("celphone")
    gender = data.get("gender")
    birth_date = data.get("birth_date")
    password = data.get("password")
    id_rol = data.get("id_rol")

    if None in (
        first_name,
        last_name,
        dni,
        email,
        celphone,
        gender,
        birth_date,
        password,
        id_rol,
    ):
        return jsonify({"Error": "Valued field is required"})

    new_client = Clients(
        first_name=first_name,
        last_name=last_name,
        dni=dni,
        email=email,
        celphone=celphone,
        gender=gender,
        birth_date=birth_date,
        password=password,
        id_rol=id_rol,
    )
    new_client.set_password(password)

    try:
        db.session.add(new_client)
        db.session.commit()
        return jsonify({"Message": "Add client"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": "Unknow error" + str(e)}), 404


# Actualizar client
@clients_bp.route("/client/update/<int:id>", methods=["PATCH"])
def update_client(id):
    if request.json is None:
        return jsonify({"Error": "Not valid request"})
    client = Clients.query.get(id)
    if not client:
        return jsonify({"Error": "client not found"}), 404

    data = request.json
    client.first_name = data.get("first_name", client.first_name)
    client.last_name = data.get("last_name", client.last_name)
    client.email = data.get("email", client.email)
    client.celphone = data.get("celphone", client.celphone)
    client.password = data.get("password", client.password)

    db.session.commit()
    return jsonify({"Message": "Succesfull update"}), 200


# Eliminar Cliente
@clients_bp.route("/client/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_client(id):
    client = Clients.query.get(id)
    if not client:
        return jsonify({"Error": "client not fount"})
    db.session.delete(client)
    db.session.commit()
    return jsonify({"Message": "Client delete Succesfull"})
