

# importing some important librarires
from db import db


class UserModel(db.Model):
    # defining our table name
    __tablename__ = "users"

    # defining our columns for the users
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
