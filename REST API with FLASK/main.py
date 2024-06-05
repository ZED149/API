

# importing packages and modules
from flask import (
    Flask,
    request,
    abort
)
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


video_args = reqparse.RequestParser()
# defining criteria for our video arguments
# likes
video_args.add_argument("likes", type=int, help="Likes count of the video is required", location="form", required=True)
# name
video_args.add_argument("name", type=str, help='Name of the video is required', location="form", required=True)
# views
video_args.add_argument("views", type=int, help="Views count of the video is required", location="form", required=True)


# video update parser
video_update_parser = reqparse.RequestParser()
# defining criteria for our video arguments
# likes
video_update_parser.add_argument("likes", type=int, help="Likes count of the video is required", location="form")
# name
video_update_parser.add_argument("name", type=str, help='Name of the video is required', location="form")
# views
video_update_parser.add_argument("views", type=int, help="Views count of the video is required", location="form")


VIDEO = {
    3: {
        "likes": 213,
        "name": "Sanso Ki Malaa by NFAK OSA Studios",
        "views": 2112312312342
    },
    4: {
        "likes": 674,
        "name": "Legends Never Die",
        "views": 879812
    }
}


# check_video_id
def check_video_id(video_id):
    if video_id not in VIDEO:
        abort(404, "Video ID is not valid...")
    return True


# initialing our Flask object
app = Flask(__name__)

# initializing our API
api = Api(app=app)

# initializing our DB
db = SQLAlchemy()
# setting up URI for the DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"


#   VideoModel
class VideoModel(db.Model):
    # data members
    id = db.Column(db.Integer, primary_key=True)            # PK of the table/model
    name = db.Column(db.String(1000), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # __repr__
    def __repr__(self) -> str:
        return f"Video(name = {name}, views = {views}, likes = {likes})"
    

# initializing our DB
db.init_app(app=app)
# creating Database with context of our app
with app.app_context():
    db.create_all()
    print("DATABSE CREATED.")


# HOW to return data if queried from database
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.String,
    'likes': fields.String
}


#   Video API
class Video(Resource):
    # GET
    # gets a video details based on video_id
    @marshal_with(resource_fields)
    def get(self, video_id):
        # querying database for the video
        result = VideoModel.query.filter_by(id=video_id).first()
        # checking if id is not valid
        if not result:
            abort(404, "Video ID is not valid...")
        return result
    
    # PUT
    # creates a new video
    @marshal_with(resource_fields)
    def put(self, video_id):
        # fetching arguments from video_args
        args = video_args.parse_args()
        # checking if video with this id already exists or not
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            # it means we have found a video
            abort(409, "Video ID taken...")
        # creating a VideoModel instance to be committed to the DB
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        # adding video to the DB session
        db.session.add(video)
        # commiting video to the DB permanentaly
        db.session.commit()
        # RETURN
        return video, 201

    # patch
    # updates an existing video
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_parser.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, "Video ID is not valid..., Cannot Update.")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result

    # DELETE
    # deletes a video
    def delete(self, video_id):
        # checking if video exists or not
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, "Video ID is not valid...")

        db.session.delete(result)
        db.session.commit()
        return "", 204


# binding the resource
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
