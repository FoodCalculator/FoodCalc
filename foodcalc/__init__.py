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
        "DATABASE_URL", "sqlite:///dev.sqlite")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get(
        'SECRET_KEY',
        b'\xe5\xd7\xa1\x13\x13\xc2\x851]m\x06\xa29x\xff(2\xf4\xc5\xc0')
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
        'SALT',
        b'X\xd9\n\xefj\xbe\xfcpL.\xc9\xe8\xb2\xe2\xfb%K\xa7\xbb ')
    app.config["SECURITY_REGISTERABLE"] = True
    app.config["SECURITY_TRACKABLE"] = True
    app.config["SECURITY_FLASH_MESSAGES"] = True
    app.config["SECURITY_CHANGEABLE"] = True
    app.config["SECURITY_TWO_FACTOR"] = True
    app.config["SECURITY_TWO_FACTOR_ENABLED_METHODS"] = ['authenticator']
    app.config["SECURITY_TOTP_SECRETS"] = os.environ.get('TOTP_SECRETS', {
        1: 'O229mrlQXalFv9BfmCGsrGB9u4TGBg3CCfOxUl61KIC'
    })
    app.config["SECURITY_TOTP_ISSUER"] = "Food Calc"
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False

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
