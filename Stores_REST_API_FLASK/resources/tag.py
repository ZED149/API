

# importing some important libraries
from models import TagModel, StoreModel, ItemModel
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import TagSchema
from flask.views import MethodView
from schemas import TagsandItemsSchema

# creating blueprint for our tags
blp = Blueprint("tags", __name__, description="Operations on Tags")


# Tag class
@blp.route("/store/<string:store_id>/tag")
class Tag(MethodView):
    # get all tags
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
        
    # creates a tag
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, data, store_id):
        tag = TagModel(**data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, 
                  message=str(e))
        return tag
    

@blp.route("/tag/<string:tag_id>")
class TagList(MethodView):
    # get 1 tag
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    # delete 1 tag
    @blp.response(202, description="Delete a tag if no item is tagged with it.",
                  example={"message": "Tag delted."})
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(400,
                      description="Returned if tag is assigned to one or more items. In this case, the tag is not deleted.")
    def delele(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag Deleted."}
        # if items are present in the tags
        abort(400, message="Could not delete tag. Make sure tag is not associated with any items, then try again.")


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class TagsandItems(MethodView):
    # link a tag to an item
    @blp.response(200, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort(401, message="Could not associate item with tag. Different Store ID's")

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting an item into tag.")
        
        return tag

    # unlink a tag to an item
    @blp.response(200, TagsandItemsSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while removing an item from the tag.")
        
        return {
            "message": "Item removed from the tag.",
            "item": item,
            "tag": tag
        }
    
