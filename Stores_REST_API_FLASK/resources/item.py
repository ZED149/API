

# importing some important libraries
from flask import Flask, request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError


# store blueprint
blp = Blueprint("items", __name__, description="Operations on items")


# Store class
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # get 1 item present in the database
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    # delete an item from the database
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    # updates an existing item in the database, if item is not present, it creates it
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        return item



@blp.route('/item')
class ItemList(MethodView):
    # get all items
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    # create an item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, data): 
        item = ItemModel(**data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item into the database.")
        return item
    
