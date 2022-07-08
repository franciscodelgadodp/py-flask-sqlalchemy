from crypt import methods
from flask import Blueprint, jsonify, request
from http import HTTPStatus
from datetime import datetime, timedelta
from py_challenge_flask.models.transaction import Transaction
from py_challenge_flask.utils.db_config import db
import uuid


transactions_api = Blueprint("transactions_api", __name__)


@transactions_api.route("/", methods=["POST"])
def create_transaction():
    content = request.json

    id = str(uuid.uuid4())

    if "date" in content:
        date = datetime.strptime(content["date"], "%Y-%m-%d")
    else:
        date = datetime.today()

    transaction = Transaction(
        id=id,
        customer_id=content["customer_id"],
        merchant_id=content["merchant_id"],
        amount_cents=content["amount_cents"],
        is_card=content["is_card"],
        date=date,
    )

    db.session.add(transaction)
    db.session.commit()

    result = {
        "id": id,
        "customer_id": content["customer_id"],
        "merchant_id": content["merchant_id"],
        "amount_cents": content["amount_cents"],
        "is_card": content["is_card"],
        "date": date,
    }

    return jsonify(result), HTTPStatus.CREATED
