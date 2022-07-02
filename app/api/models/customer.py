from typing import List
from uuid import uuid4

from core.db import db


def _get_uuid():
    return uuid4().hex


class CustomerModel(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.String, primary_key=True, default=_get_uuid)
    customer_number = db.Column(db.Integer, nullable=False, unique=True)
    company = db.Column(db.String, nullable=False, unique=True)
    street = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    zip = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=True)
    mail = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)

    @classmethod
    def find_by_customer_number(cls, customer_number: int) -> "CustomerModel":
        return cls.query.filter_by(customer_number=customer_number).first()

    @classmethod
    def find_all(cls) -> List["CustomerModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
