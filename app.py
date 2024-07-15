from config.Config import Config
from controllers.Client import clients_bp
from flask import Flask

from flask_cors import CORS

from flask_migrate import Migrate
from models.Models import db
from controllers.Rol import initialize
from controllers.Login import login_bp, jwt
from controllers.Assessment import assessment_bp
from controllers.Volumetry import volumetry_bp
from controllers.Skinfold import skinfold_bp
from controllers.Uploads import uploads_bp

# Iniciar App
app = Flask(__name__)

# Importar Conexion a bd
app.config.from_object(Config)
# Cors
CORS(app)
# Iniciar OrM
db.init_app(app)

migrate = Migrate(app, db)

# Iniciar JWTManager
jwt.init_app(app)

# Rutas Controladores
app.register_blueprint(clients_bp)
app.register_blueprint(login_bp)
app.register_blueprint(assessment_bp)
app.register_blueprint(volumetry_bp)
app.register_blueprint(skinfold_bp)
app.register_blueprint(uploads_bp)

with app.app_context():
    db.create_all()
    initialize()
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
