from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from py_challenge_flask.models import Base
from py_challenge_flask.models.transaction import Transaction


class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)
    transactions = relationship(Transaction)
