from flask import Flask, redirect, url_for
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_login import current_user
from .config import DevConfig
from .extensions import bcrypt, login_manager, principals

from .models import db, mongo
from .controllers.blog import blog_blueprint
from .controllers.main import main_blueprint
from .controllers.admin import admin_blueprint

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)

    def convert_objectId(objectId):
        return str(objectId)

    app.jinja_env.filters['convert_objectId'] = convert_objectId
    @identity_loaded.connect_via(app)
    def on_identify_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()