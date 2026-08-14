import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY","abdelfatah_secret_key")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads" )
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER ="smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD= os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER= MAIL_USERNAME