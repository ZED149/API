

# importing some important libraries
from models import TagModel, StoreModel
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import TagSchema
from flask.views import MethodView

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