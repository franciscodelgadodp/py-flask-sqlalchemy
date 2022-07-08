from crypt import methods
from flask import Blueprint, jsonify
from http import HTTPStatus
from py_challenge_flask.models.merchant import Merchant
from py_challenge_flask.utils.db_config import db


merchants_api = Blueprint("merchants_api", __name__)


@merchants_api.route("/", methods=["GET"])
def list_merchants():
    merchants = db.session.query(Merchant).all()
    result = [
        {"id": merchant.id, "name": merchant.name, "category": merchant.category}
        for merchant in merchants
    ]

    return jsonify(result), HTTPStatus.OK
