from flask_bcrypt import Bcrypt
from flask_login import LoginManager

bcrypt = Bcrypt()

login_manager = LoginManager()

login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(userid)