from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from sqlalchemy import inspect
from flask_login import current_user

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "devkey")
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "researchd.sqlite")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True

    db.init_app(app)

    # CSRF Protection setup
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route("/debug-auth")
    def debug_auth():
        return f"Authenticated: {current_user.is_authenticated}"

    # Register blueprints
    from .routes import auth, main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        inspector = inspect(db.engine)
        print("Tables created:", inspector.get_table_names())

    return app
