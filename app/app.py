#! /usr/bin/env python
import views
from core.db import db
from core.settings import config
from errors import HttpError
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from models.models import User
from views import login


def create_app(db_url: str):

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["JWT_SECRET_KEY"] = "qwerty123"

    jwt = JWTManager(app)
    db.init_app(app)

    @app.errorhandler(HttpError)
    def error_handler(err: HttpError):
        json_response = jsonify({"error": err.error_message})
        json_response.status_code = err.status_code
        return json_response

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    user_view = views.UserView.as_view("user")
    adv_view = views.AdvertisementView.as_view("advertisement")
    app.add_url_rule("/users", view_func=user_view, methods=["POST"])
    app.add_url_rule("/advertisement", view_func=adv_view, methods=["POST"])
    app.add_url_rule(
        "/advertisement/<int:adv_id>",
        view_func=adv_view,
        methods=["PATCH", "DELETE", "GET"],
    )
    app.add_url_rule("/login", view_func=login, methods=["POST"])

    return app


if __name__ == "__main__":
    app = create_app(config.dsn)
    app.run(debug=True)
