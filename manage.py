import os

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from webapp import create_app
from webapp.models import db, User, Post, Tag, Comment

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig'%env.capitalize())

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server(host='192.168.17.129'))
manager.add_command("db", MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Tag=Tag, Comment=Comment)

if __name__ == "__main__":
    manager.run()
