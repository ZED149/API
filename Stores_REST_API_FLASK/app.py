

# importing some important libraries
from flask import Flask, jsonify
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBluePrint
from resources.user import blp as UserBlueprint
from db import db
import models
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from blocklist import BlockList


# loading our enviournmental variables into our scope
load_dotenv()


def create_app(db_url=None):    
    # initializing Flask app object
    app = Flask(__name__)

    # CONFIGURATIONS
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "Stores REST API"
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config['OPENAPI_URL_PREFIX'] = "/"
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv("DATABASE_URI", "sqlite:///data.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initializing our databse with our flask app
    db.init_app(app)

    # creating tables 
    with app.app_context():
        db.create_all()
    
    # initializing our API
    api=Api(app)

    # configuring a secret key for jwt token
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    # initializing our JWT object
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BlockList
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "description": "The token has been revoked",
                "error": "token_revoked"
            }), 401
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        pass

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.",
                     "error": "token_expired"}), 401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "message": "Signature verficiation failed.",
                "error": "invalid token"
            }), 401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "description": "Reuqest doesn't contain an access token.",
                "error": "authorization required"
            })
        )

    # registering our blueprints
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBlueprint)


    # Return
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()