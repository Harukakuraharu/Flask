import sqlalchemy as sa
from core.db import db
from crud import add_data, delete_item, get_data, update_data
from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required
from models.models import Advertisement, User
from schema import (
    CreateAdvertisement,
    CreateUser,
    ResponseAdvertisement,
    ResponseUser,
    UpdateAdvertisement,
)
from security import check_owner, check_password, hash_password
from validate import validate


class UserView(MethodView):
    def post(self) -> dict:
        validate_data = validate(CreateUser, request.data).model_dump()
        validate_data["password"] = hash_password(validate_data["password"])
        user = add_data(User, validate_data)
        user = ResponseUser(**user.json)
        return jsonify(user.model_dump())


class AdvertisementView(MethodView):
    @jwt_required()
    def post(self) -> dict:
        validate_data = validate(CreateAdvertisement, request.data).model_dump()
        get_data(validate_data["user_id"], User)
        advertisement = add_data(Advertisement, validate_data)
        advertisement = ResponseAdvertisement(**advertisement.json)
        return jsonify(advertisement.model_dump())

    @jwt_required()
    def patch(self, adv_id: int) -> dict:
        check_owner(Advertisement, adv_id)
        validate_data = validate(UpdateAdvertisement, request.data).model_dump(
            exclude_unset=True
        )
        validate_data["id"] = adv_id
        advertisement = update_data(Advertisement, validate_data)
        advertisement = ResponseAdvertisement(**advertisement.json)
        return jsonify(advertisement.model_dump())

    @jwt_required()
    def delete(self, adv_id: int) -> dict:
        check_owner(Advertisement, adv_id)
        delete_item(Advertisement, adv_id)
        return jsonify({"text": "Successfully deleted"}), 204

    @jwt_required()
    def get(self, adv_id: int) -> dict:
        check_owner(Advertisement, adv_id)
        advertisement = get_data(adv_id, Advertisement)
        return jsonify(advertisement.json)


def login() -> dict:
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    stmt = sa.select(User).where(User.email == email)
    user = db.session.scalar(stmt)
    if user is None or (user.password and not check_password(user.password, password)):
        return jsonify({"text": "Incorrect email or password"}), 401
    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)
