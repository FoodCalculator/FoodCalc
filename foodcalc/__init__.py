import os

from flask import Flask

from foodcalc import main
from foodcalc.models import db


def create_app():
    # Configure app
    app = Flask(__name__)

    # Ensure app reloads on templates changes
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///foodcalc.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Ensure responses aren't cached
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = ("no-cache, "
                                             "no-store, must-revalidate")
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    app.register_blueprint(main.bp)
    return app


if __name__ == '__main__':
    create_app().run()
