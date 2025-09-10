from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    uid = db.Column(db.Integer, primary_key=True)
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
    
    def get_id(self):
        return str(self.uid)


class Profile(db.Model):
    __tablename__ = "profiles"
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False, unique=True, index=True)
    
    name = db.Column(db.String(150))
    title = db.Column(db.String(150))
    institution = db.Column(db.String(150))
    department = db.Column(db.String(150))
    bio = db.Column(db.Text)
    pfp = db.Column(db.String(255))  # profile picture URL
    location = db.Column(db.String(150))
    
    user = db.relationship('User', backref=db.backref('profile'))

    # collections
    educations = db.relationship("Education", back_populates="profile", cascade="all, delete-orphan", passive_deletes=True)
    experiences = db.relationship("Experience", back_populates="profile", cascade="all, delete-orphan", passive_deletes=True)
    publications = db.relationship("Publication", back_populates="profile", cascade="all, delete-orphan", passive_deletes=True)
    files = db.relationship("File", back_populates="profile", cascade="all, delete-orphan", passive_deletes=True)
    photos = db.relationship("Photo", back_populates="profile", cascade="all, delete-orphan", passive_deletes=True)
    socials = db.relationship("Social", back_populates="profile", cascade="all, delete-orphan", passive_deletes=True)


class Education(db.Model):
    eid = db.Column(db.Integer, primary_key=True)  # EducationID
    pid = db.Column(db.Integer, db.ForeignKey("profiles.pid", ondelete="CASCADE"), nullable=False, index=True)

    degree = db.Column(db.String(150), nullable=False)
    institution = db.Column(db.String(150), nullable=False)
    start_year = db.Column(db.Integer, nullable=True)
    end_year = db.Column(db.Integer, nullable=True)

    profile = db.relationship("Profile", back_populates="educations")


class Experience(db.Model):
    exid = db.Column(db.Integer, primary_key=True)  # ExperienceID
    pid = db.Column(db.Integer, db.ForeignKey("profiles.pid", ondelete="CASCADE"), nullable=False, index=True)

    role = db.Column(db.String(150), nullable=False)
    institution = db.Column(db.String(150), nullable=False)
    start_year = db.Column(db.Integer, nullable=True)
    end_year = db.Column(db.Integer, nullable=True)

    profile = db.relationship("Profile", back_populates="experiences")


class File(db.Model):
    __tablename__ = "files"

    fid = db.Column(db.Integer, primary_key=True)  # FileID
    pid = db.Column(db.Integer, db.ForeignKey("profiles.pid", ondelete="CASCADE"), nullable=False, index=True)

    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))          # e.g., 'pdf', 'png'
    file_size = db.Column(db.Integer)             # bytes
    file_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    profile = db.relationship("Profile", back_populates="files")
    # reverse link from Publication via publication.file_id


class Photo(db.Model):
    __tablename__ = "photos"

    photoid = db.Column(db.Integer, primary_key=True)  # PhotoID
    pid = db.Column(db.Integer, db.ForeignKey("profiles.pid", ondelete="CASCADE"), nullable=False, index=True)

    file_path = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    profile = db.relationship("Profile", back_populates="photos")


class Social(db.Model):
    __tablename__ = "socials"

    sid = db.Column(db.Integer, primary_key=True)  # SocialID
    pid = db.Column(db.Integer, db.ForeignKey("profiles.pid", ondelete="CASCADE"), nullable=False, index=True)

    platform = db.Column(db.String(50), nullable=False)  # 'LinkedIn', 'Twitter', etc.
    url = db.Column(db.String(500), nullable=False)

    profile = db.relationship("Profile", back_populates="socials")


class Publication(db.Model):
    __tablename__ = "publications"

    pubid = db.Column(db.Integer, primary_key=True)  # PublicationID
    pid = db.Column(db.Integer, db.ForeignKey("profiles.pid", ondelete="CASCADE"), nullable=False, index=True)

    title = db.Column(db.String(300), nullable=False)
    journal = db.Column(db.String(200))
    year = db.Column(db.Integer)
    doi = db.Column(db.String(120), index=True)
    url = db.Column(db.String(500))

    # Optional link to a stored File (e.g., the uploaded PDF)
    fid = db.Column(db.Integer, db.ForeignKey("files.fid", ondelete="SET NULL"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    profile = db.relationship("Profile", back_populates="publications")
    file = db.relationship("File", foreign_keys=[fid])