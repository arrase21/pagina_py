from flask import Blueprint, request, jsonify
from models.Models import Clients, fileUpload, db
from werkzeug.utils import secure_filename
import os
import uuid

uploads_bp = Blueprint("blueprint_bp", __name__)

UPLOAD_FOLDER = "upload/"  # Cambia esto a la ruta de tu carpeta de subida
ALLOWED_EXTENSIONS = {
    "txt",
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "gif",
}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@uploads_bp.route("/upload/<int:id_client>/", methods=["POST"])
def upload_file(id_client):
    client = Clients.query.get_or_404(id_client)
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        clien_folder = os.path.join(UPLOAD_FOLDER, str(client.id_clients))
        os.makedirs(clien_folder, exist_ok=True)
        filepath = os.path.join(clien_folder, unique_filename)
        file.save(filepath)

        new_file = fileUpload(
            filename=unique_filename, filepath=filepath, id_clients=client.id_clients
        )

        try:
            db.session.add(new_file)
            db.session.commit()
            return jsonify({"success": True, "filename": unique_filename}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": False, "error": "File type not allowed"}), 400
