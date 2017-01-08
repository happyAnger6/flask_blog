from flask import Flask, redirect, url_for
from .config import DevConfig

from .models import db
from .controllers.blog import blog_blueprint

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

@app.route('/')
def index():
    print("here")
    return redirect(url_for('blog.home'))

app.register_blueprint(blog_blueprint)

if __name__ == "__main__":
    app.run(host='192.168.17.129')