from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default = True)
    created_at = db.Column(db. DateTime, default = datetime.utcnow)

    # profile fields
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    profile_pic_url = db.Column(db.String(255), nullable=True)
    institution = db.Column(db.String(150), nullable=True)
    position = db.Column(db.String(100), nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Publications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    journal = db.Column(db.String(255), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    doi = db.Column(db.String(100), unique=True, nullable=True)
    url = db.Column(db.String(255), nullable=True)
    file_id = db.Column(db.Integer, db.ForeignKey('Files.id'), nullable=True)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(150), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=True)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(150), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=True)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # e.g., 'dataset', 'code', 'paper'
    file_size = db.Column(db.Integer, nullable=False)  # size in bytes
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Socials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    platform = db.Column(db.String(100), nullable=False)  # e.g., 'LinkedIn', 'ResearchGate'
    url = db.Column(db.String(255), nullable=False)

