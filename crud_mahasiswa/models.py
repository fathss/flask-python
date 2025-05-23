from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID (INTEGER, PRIMRAY KEY)
    nama = db.Column(db.String(100), nullable=False) # NAMA (STRING, NOT NULL)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID (INTEGER, PRIMRAY KEY)
    username = db.Column(db.String(100), unique=True, nullable=False) # USERNAME (STRING, UNIQUE, NOT NULL)
    password_hash = db.Column(db.String(200), nullable=False) # PASSWORD yang terhash (STRING, NOT NULL)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) # Men-hash password dari parameter yang diberikan lalu ditampung di variabel password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # Cek apakah password_hash sama dengan parameter password