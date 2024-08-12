#! /usr/bin/env python
from flask import Flask, jsonify

import views
from core.db import db
from core.settings import config
from errors import HttpError


def create_app(db_url: str):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    db.init_app(app)

    @app.errorhandler(HttpError)
    def error_handler(err: HttpError):
        json_response = jsonify({"error": err.error_message})
        json_response.status_code = err.status_code
        return json_response
    
    user_view = views.UserView.as_view("user")
    adv_view = views.AdvertisementView.as_view("advertisement")
    app.add_url_rule(
        "/users", view_func=user_view, methods=["POST"]
    )
    app.add_url_rule(
        "/advertisement", view_func=adv_view, methods=["POST"]
    )
    app.add_url_rule(
        "/advertisement/<int:adv_id>", view_func=adv_view, methods=["PATCH", "DELETE", "GET"])

    return app


if __name__ == "__main__":
    app = create_app(config.dsn)
    app.run(debug=True)
