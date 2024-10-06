

# importing some important libraries
from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBluePrint
from db import db
import models
import os
from dotenv import load_dotenv


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

    # registering our blueprints
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBluePrint)

    # Return
    return app
