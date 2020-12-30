"""A food calculator."""

import os

from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore

from foodcalc import main
from foodcalc.models import db, User, Role


security = Security()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app():
    """Instantiate and configure the app object."""
    # Configure app
    app = Flask(__name__)

    # Ensure app reloads on templates changes
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///foodcalc.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'dev')
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get('SALT', 'dev')

    db.init_app(app)
    security.init_app(app, user_datastore)

    def init_db():
        db.create_all()

    # Ensure responses aren't cached
    def after_request(response):
        response.headers["Cache-Control"] = ("no-cache, "
                                             "no-store, must-revalidate")
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    app.after_request(after_request)
    app.before_first_request(init_db)
    app.register_blueprint(main.bp)

    return app
