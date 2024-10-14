

# importing some important libraries
from flask.views import MethodView
from schemas import UserSchema, DeleteUserSchema, UserLoginSchema
from flask_smorest import Blueprint
from models import UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from blocklist import BlockList


blp = Blueprint("users", __name__, description="Operations on users.")


@blp.route("/register/")
class User(MethodView):
    # create user
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema, description="Creates a user in the database.")    
    @blp.alt_response(500, description="Error Occurred.")
    @blp.alt_response(501, description="User already present.")
    def post(self, user_data):
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting user into database.")
        except IntegrityError:
            abort(501, message="Username already exists.")
        return {
            "message": "User Created.",
            "username": user.username
            }


@blp.route("/users/")
class User(MethodView):
    # get all users
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users
    
    

@blp.route("/user/<string:user_id>")
class User(MethodView):
    # delete a user
    @blp.arguments(DeleteUserSchema)
    @blp.response(200, DeleteUserSchema, description="User Deleted.")
    def delete(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Cannot delete user from database")
        return {
            "message": "User Deleted.",
            "user": user
        }
    

# user login resource
@blp.route("/user/login/")
class UserLogin(MethodView):
    # user login
    @blp.arguments(UserLoginSchema)
    def get(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and user.password == user_data['password']:
            # creating access token for the user
            access_token = create_access_token(identity=user.id, fresh=True)    # used for destructive tasks
            # used for non-destructive tasks and for generating new non-fresh token
            # after a certain amount of time with out notifyig the user
            refresh_token = create_refresh_token(identity=user.id)      
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        else:
            abort(401, message="Invalid Credentials.")


@blp.route("/user/logout/")
class UserLogout(MethodView):
    @jwt_required()
    def get(self):
        jti = get_jwt()['jti']
        BlockList.add(jti)
        return {
            "message": "Successfully logged out."
        }
    

@blp.route("/user/refresh")
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {
            "access token": new_token
        }