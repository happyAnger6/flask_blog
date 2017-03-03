import datetime
import json
from bson import ObjectId
from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin

from webapp.extensions import bcrypt

db = SQLAlchemy()
mongo = MongoEngine()

available_roles = ('admin', 'poster', 'default')

class User(mongo.Document):
    username = mongo.StringField(require=True)
    password = mongo.DynamicField(require=True)
    roles = mongo.ListField(
        mongo.StringField(choices=available_roles)
    )

    def __repr__(self):
        return "<User `{}`>".format(self.username)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)

class Tag(mongo.Document):
    title = mongo.StringField(required=True)
    alias = mongo.IntField(required=True)
    father = mongo.StringField(required=True)
    children = mongo.ListField(
        mongo.StringField()
    )

    def __repr__(self):
        return "<Tag '{}'>".format(self.title)

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
    text = mongo.StringField()
    publish_date = mongo.DateTimeField(
        default=datetime.datetime.now()
    )
    user = mongo.ReferenceField(User)
    comments = mongo.ListField(
        mongo.EmbeddedDocumentField(Comment)
    )
    tags = mongo.ListField(mongo.ReferenceField(Tag))

    meta = {
        'allow_inheritance': True,
        'ordering': ['-publish_date']
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