from flask import Blueprint, jsonify, request
from http import HTTPStatus
from datetime import datetime, timedelta
from py_challenge_flask.models.merchant import Merchant
from py_challenge_flask.models.transaction import Transaction
from py_challenge_flask.utils.db_config import db
from sqlalchemy import func


insights_api = Blueprint("insights_api", __name__)


@insights_api.route("/", methods=["POST"])
def get_insights():
    content = request.json

    if "customer_id" not in content:
        return "no customer was indicated", HTTPStatus.BAD_REQUEST

    today = datetime.today()

    if "days_ago" in content:
        limit_date = today - timedelta(int(content["days_ago"]))

        if "top_n" in content:
            insights_fetched = (
                db.session.query(Merchant.category, func.sum(Transaction.amount_cents))
                .join(Merchant)
                .filter(
                    Transaction.is_card == True,
                    Transaction.customer_id == content["customer_id"],
                    Transaction.date <= today,
                    Transaction.date >= limit_date,
                )
                .group_by(Merchant.category)
                .order_by(func.sum(Transaction.amount_cents).desc())
                .limit(content["top_n"])
                .all()
            )
        else:
            insights_fetched = (
                db.session.query(Merchant.category, func.sum(Transaction.amount_cents))
                .join(Merchant)
                .filter(
                    Transaction.is_card == True,
                    Transaction.customer_id == content["customer_id"],
                    Transaction.date <= today,
                    Transaction.date >= limit_date,
                )
                .group_by(Merchant.category)
                .order_by(func.sum(Transaction.amount_cents).desc())
                .all()
            )

    elif "top_n" in content:
        insights_fetched = (
            db.session.query(Merchant.category, func.sum(Transaction.amount_cents))
            .join(Merchant)
            .filter(
                Transaction.is_card == True,
                Transaction.customer_id == content["customer_id"],
                Transaction.date <= today,
            )
            .group_by(Merchant.category)
            .order_by(func.sum(Transaction.amount_cents).desc())
            .limit(content["top_n"])
            .all()
        )
    else:
        insights_fetched = (
            db.session.query(Merchant.category, func.sum(Transaction.amount_cents))
            .join(Merchant)
            .filter(
                Transaction.is_card == True,
                Transaction.customer_id == content["customer_id"],
                Transaction.date <= today,
            )
            .group_by(Merchant.category)
            .order_by(func.sum(Transaction.amount_cents).desc())
            .all()
        )

    result = [
        {"category": insight[0], "amount": insight[1]} for insight in insights_fetched
    ]

    return jsonify(result), HTTPStatus.OK
