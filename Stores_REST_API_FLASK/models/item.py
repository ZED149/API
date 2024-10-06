

# importing some important libraries
from db import db


class ItemModel(db.Model):
    # defining our table name
    __tablename__ = "items"

    # defining our cols
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False, unique=False)
    store = db.relationship("StoreModel", back_populates="items")