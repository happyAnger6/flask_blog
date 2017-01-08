from flask import Flask, redirect, url_for
from .config import DevConfig

from .models import db
from .controllers.blog import blog_blueprint

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))

    app.register_blueprint(blog_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()