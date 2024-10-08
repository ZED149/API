


# importing some important files
from db import db


class ItemTags(db.Model):
    # defining table name for our model
    __tablename__ = "items_tags"

    # defining columns for our tables
    id = db.Column(db.Integer, unique=True, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

