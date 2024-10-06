

# importing some important libraries
from flask import Flask, request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from models import StoreModel
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db


# store blueprint
blp = Blueprint("stores", __name__, description="Operations on stores")


# Store class
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    # return 1 store
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    # delete a store from the database
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}



@blp.route('/store')
class StoreList(MethodView):
    # get all stores
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    # create a store
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, data):
        new_store = StoreModel(**data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists."
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating a new store.")
        return new_store
    
