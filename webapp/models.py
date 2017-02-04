import datetime

from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin

from webapp.extensions import bcrypt

db = SQLAlchemy()
mongo = MongoEngine()

available_roles = ('admin', 'poster', 'default')

class User(mongo.Document):
    username = mongo.StringField(require=True)
    password = mongo.StringField(require=True)
    roles = mongo.ListField(
        mongo.StringField(choices=available_roles)
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Comment(mongo.EmbeddedDocument):
    name = mongo.StringField(required=True)
    text = mongo.StringField(required=True)
    date = mongo.DateTimeField(
        default=datetime.datetime.now()
    )

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

class Post(mongo.Document):
    title = mongo.StringField(required=True)
    publish_date = mongo.DateTimeField(
        default=datetime.datetime.now()
    )
    user = mongo.ReferenceField(User)
    comments = mongo.ListField(
        mongo.EmbeddedDocumentField(Comment)
    )
    tags = mongo.ListField(mongo.StringField())

    meta = {
        'allow_inheritance': True
    }
    def __repr__(self):
        return "<Post '{}'>".format(self.title)

class BlogPost(Post):
    text = mongo.StringField(required=True)

    @property
    def type(self):
        return "blog"

class VideoPost(Post):
    url = mongo.StringField(required=True)

    @property
    def type(self):
        return "video"

class ImagePost(Post):
    image_url = mongo.StringField(required=True)

    @property
    def type(self):
        return "image"

class QuotePost(Post):
    quote = mongo.StringField(required=True)
    author = mongo.StringField(required=True)

    @property
    def type(self):
        return "quote"