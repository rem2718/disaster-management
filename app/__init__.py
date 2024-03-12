from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask

from app.utils.extensions import db, bcrypt, jwt
from app.routes.user_routes import user as user_routes
from app.config import Config

swagger_ui_blueprint = get_swaggerui_blueprint(
    "/swagger", "/static/swagger.json", config={"app_name": "Access API"}
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

app.register_blueprint(swagger_ui_blueprint, url_prefix="/swagger")
app.register_blueprint(user_routes)
