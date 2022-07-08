import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from py_challenge_flask.models.merchant import Merchant

from py_challenge_flask.models.transaction import Transaction


# try:
engine = create_engine("sqlite:///src/py_challenge_flask/db.sqlite")

Session = sessionmaker(bind=engine)

Transaction.__table__.create(bind=engine, checkfirst=True)
Merchant.__table__.create(bind=engine, checkfirst=True)

session = Session()


def prepare_transaction(row):
    row["is_card"] = True if row["is_card"] == "True" else False
    row["date"] = datetime.strptime(row["date"], "%Y-%m-%d")
    return Transaction(**row)


with open(
    "src/py_challenge_flask/utils/merchants_2022_02_09.csv",
    encoding="utf-8",
    newline="",
) as csv_file:
    csvreader = csv.DictReader(csv_file, quotechar='"')
    merchants = [Merchant(**row) for row in csvreader]

    try:
        session.add_all(merchants)
        session.commit()
    except:
        print("Merchants exist already in DB")

with open(
    "src/py_challenge_flask/utils/transactions_2022_02_09.csv",
    encoding="utf-8",
    newline="",
) as csv_file:
    csvreader = csv.DictReader(csv_file, quotechar='"')
    transactions = [prepare_transaction(row) for row in csvreader]

    try:
        session.add_all(transactions)
        session.commit()
    except:
        print("Transactions exist already in DB")

session.close()

# except:
#     print("DB Connection error")
