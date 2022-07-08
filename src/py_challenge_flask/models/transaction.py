from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from py_challenge_flask.models import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True)
    customer_id = Column(String)
    merchant_id = Column(String, ForeignKey("merchants.id"))
    amount_cents = Column(Integer)
    is_card = Column(Boolean)
    date = Column(Date)
