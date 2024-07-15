from decouple import config


class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv(config("DATABASE_URL"))
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "your_jwt_secret_key"
