from flask import Flask
from py_challenge_flask.utils import db_config
from py_challenge_flask.handlers.merchants import merchants_api
from py_challenge_flask.handlers.insights import insights_api
from py_challenge_flask.handlers.transactions import transactions_api


def create_app():
    _app = Flask(__name__)
    db_config.config_db(app=_app)
    _app.register_blueprint(merchants_api, url_prefix="/merchants")
    _app.register_blueprint(insights_api, url_prefix="/insights")
    _app.register_blueprint(transactions_api, url_prefix="/transactions")

    return _app


if __name__ == "__main__":
    app = create_app()
    app.run()
