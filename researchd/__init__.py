from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "supersecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///researchd.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .routes import auth, main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
