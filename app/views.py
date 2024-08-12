from crud import add_data, delete_item, get_data, update_data
from flask import jsonify, request
from flask.views import MethodView
from models.models import Advertisement, User
from schema import (
    CreateAdvertisement,
    CreateUser,
    ResponseAdvertisement,
    ResponseUser,
    UpdateAdvertisement,
)
from security import hash_password
from validate import validate


class UserView(MethodView):
    def post(self):
        validate_data = validate(CreateUser, request.data).model_dump()
        validate_data["password"] = hash_password(validate_data["password"])
        user = add_data(User, validate_data)
        user = ResponseUser(**user.json)
        return jsonify(user.model_dump())


class AdvertisementView(MethodView):
    def post(self):
        validate_data = validate(CreateAdvertisement, request.data).model_dump()
        get_data(validate_data["user_id"], User)
        advertisement = add_data(Advertisement, validate_data)
        advertisement = ResponseAdvertisement(**advertisement.json)
        return jsonify(advertisement.model_dump())

    def patch(self, adv_id):
        validate_data = validate(UpdateAdvertisement, request.data).model_dump(
            exclude_unset=True
        )
        validate_data["id"] = adv_id
        advertisement = update_data(Advertisement, validate_data)
        advertisement = ResponseAdvertisement(**advertisement.json)
        return jsonify(advertisement.model_dump())

    def delete(self, adv_id):
        delete_item(Advertisement, adv_id)
        return jsonify({"status": "deleted"})

    def get(self, adv_id):
        advertisement = get_data(adv_id, Advertisement)
        return jsonify(advertisement.json)
