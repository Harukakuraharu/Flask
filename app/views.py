import flask_bcrypt
import pydantic
from flask import Response, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from app import get_app
from models import MODEL, Advertisement, Session, User
from schema import CreateAdvertisement, CreateUser, Schema, UpdateAdvertisement

app = get_app()

bcrypt = flask_bcrypt.Bcrypt(app)


def hash_password(password: str) -> str:
    password = password.encode()
    password = bcrypt.generate_password_hash(password)
    password = password.decode()
    return password


def check_password(hashed_password: str, password: str) -> bool:
    hashed_password = hashed_password.encode()
    password = password.encode()
    return bcrypt.check_password_hash(hashed_password, password)


class HttpError(Exception):

    def __init__(self, status_code: int, error_message: str | dict):
        self.status_code = status_code
        self.error_message = error_message


def validate(schema_cls: Schema, json_data: dict):
    try:
        return schema_cls(**json_data).model_dump(exclude_unset=True)
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise HttpError(409, error)


@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    json_response = jsonify({"error": err.error_message})
    json_response.status_code = err.status_code
    return json_response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: Response):
    request.session.close()
    return response


def get_data(item_id: int, model: MODEL):
    item_id = request.session.get(model, item_id)
    if item_id is None:
        if model.__name__ == "User":
            raise HttpError(404, "User not found")
        raise HttpError(404, "Advertisement not found")
    return item_id


def add_data(model: MODEL):
    request.session.add(model)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, f"{model.__class__.__name__} already exists")
    return model


class UserView(MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def post(self):
        json_data = validate(CreateUser, request.json)
        json_data["password"] = hash_password(json_data["password"])
        user = add_data(User(**json_data))
        return jsonify(user.json)


class AdvertisementView(MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, adv_id):
        advertisement = get_data(adv_id, Advertisement)
        return jsonify(advertisement.json)

    def post(self):
        json_data = validate(CreateAdvertisement, request.json)
        get_data(json_data["user_id"], User)
        advertisement = add_data(Advertisement(**json_data))
        return jsonify(advertisement.json)

    def patch(self, adv_id):
        json_data = validate(UpdateAdvertisement, request.json)
        advertisement = get_data(adv_id, Advertisement)
        for field, value in json_data.items():
            setattr(advertisement, field, value)
        advertisement = add_data(advertisement)
        return jsonify(advertisement.json)

    def delete(self, adv_id):
        advertisement = get_data(adv_id, Advertisement)
        self.session.delete(advertisement)
        self.session.commit()
        return jsonify({"status": "Advertisement deleted"})


user_view = UserView.as_view("user")
advertisement_view = AdvertisementView.as_view("advertisement")

app.add_url_rule("/user/", view_func=user_view, methods=["POST"])
app.add_url_rule("/advertisement/", view_func=advertisement_view, methods=["POST"])
app.add_url_rule(
    "/advertisement/<int:adv_id>/",
    view_func=advertisement_view,
    methods=["GET", "PATCH", "DELETE"],
)

if __name__ == "__main__":
    app.run()
