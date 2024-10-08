

# importing some important libraries
from db import db


class TagModel(db.Model):
    # defining table for our tags
    __tablename__ = "tags"

    # defining cols for our tags
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False, unique=False)
    
    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")